#!/usr/bin/env python3
"""Exercise the real installed menu, then independently read AX geometry."""
from pathlib import Path
import json
import subprocess
import time
import sys

root = Path(__file__).resolve().parents[1]
app = Path.home() / "Applications/Modo Desenvolvedor.app/Contents/MacOS/ModoDesenvolvedor"
report = Path.home() / "Library/Logs/ModoDesenvolvedor/ultima-execucao.json"
evidence = root / "validation"

def run(args, *, check=True):
    return subprocess.run([str(x) for x in args], cwd=root, text=True, capture_output=True, check=check)

def activate(name):
    previous = report.stat().st_mtime_ns if report.exists() else 0
    opened = run(["swift", "Tests/MenuProbe.swift", "--open"])
    clicked = run(["swift", "Tests/MenuProbe.swift", "--activate"])
    assert "ACTIVATE real NSMenuItem AXPress: 0" in clicked.stdout, clicked.stdout
    (evidence / f"{name}-menu.txt").write_text(opened.stdout + clicked.stdout)
    deadline = time.monotonic() + 55
    while time.monotonic() < deadline:
        if report.exists() and report.stat().st_mtime_ns > previous:
            data = json.loads(report.read_text())
            (evidence / f"{name}-app-report.json").write_text(json.dumps(data, indent=2))
            assert data["passed"], data
            independent = run(["build/independent-verifier"])
            (evidence / f"{name}-independent.json").write_text(independent.stdout)
            assert json.loads(independent.stdout)["passed"]
            print(f"PASS: {name}; menu real, AX independente, barra visível e sem Dock", flush=True)
            return
        time.sleep(0.2)
    raise RuntimeError("The installed application did not complete its menu command")

if "--closed-only" not in sys.argv:
    activate("20-repeat-open-apps")
    run([app, "--prepare-minimized"])
    before = run([app, "--inspect"], check=False)
    (evidence / "21-minimized-before.json").write_text(before.stdout)
    assert json.loads(before.stdout)["windows"][0]["minimized"]
    activate("22-minimized")
quit_result = run(["swift", "Tests/QuitChrome.swift"])
print(quit_result.stdout.strip(), flush=True)
before = run([app, "--inspect"], check=False)
(evidence / "23-closed-chrome-before.json").write_text(before.stdout)
assert not json.loads(before.stdout)["windows"][0]["running"]
activate("24-closed-chrome")
diagnostics = run([app, "--diagnose"])
(evidence / "25-final-diagnostics.json").write_text(diagnostics.stdout)
assert json.loads(diagnostics.stdout)["loginStatus"] == 1
run(["shasum", "-a", "256", "-c", "validation/final-binary-sha256.txt"])
print("PASS: início automático habilitado e binário final intacto", flush=True)
