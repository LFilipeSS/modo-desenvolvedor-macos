#!/usr/bin/env python3
"""Click the installed status button and verify its own report and independent AX measurements."""
from pathlib import Path
import json
import subprocess
import time

root = Path(__file__).resolve().parents[1]
evidence = root / "validation/1.2.0"
evidence.mkdir(parents=True, exist_ok=True)
logs = Path.home() / "Library/Logs/ModoDesenvolvedor"
report = logs / "ultima-execucao.json"
before = report.stat().st_mtime_ns if report.exists() else 0
log_before = (logs / "modo-desenvolvedor.log").stat().st_size
def run(args):
    return subprocess.run([str(x) for x in args], cwd=root, check=True, text=True, capture_output=True).stdout
run(["shasum", "-a", "256", "-c", evidence / "installed-sha256.txt"])
clicked = run(["swift", "Tests/ButtonProbe.swift", "--click"])
(evidence / "installed-button.txt").write_text(clicked)
assert "DIRECT BUTTON AXPress: 0" in clicked
end = time.monotonic() + 55
while time.monotonic() < end:
    if report.exists() and report.stat().st_mtime_ns > before:
        result = json.loads(report.read_text())
        assert result["passed"], result
        (evidence / "installed-app-report.json").write_text(json.dumps(result, indent=2))
        independent = run(["build/independent-verifier"])
        (evidence / "installed-independent.json").write_text(independent)
        assert json.loads(independent)["passed"]
        assert json.loads(independent)["dockAutoHidden"]
        with (logs / "modo-desenvolvedor.log").open("rb") as file:
            file.seek(log_before)
            trace = file.read().decode()
        (evidence / "installed-action.log").write_text(trace)
        assert trace.index("DOCK: ocultação confirmada") < trace.index("INÍCIO tela=")
        assert trace.index("INÍCIO tela=") < trace.index("LOCALIZAÇÃO") if "LOCALIZAÇÃO" in trace else True
        if "ABERTURA" in trace:
            assert trace.index("DOCK: ocultação confirmada") < trace.index("ABERTURA")
        run(["shasum", "-a", "256", "-c", evidence / "installed-sha256.txt"])
        print("PASS: botão real, Dock oculto antes dos aplicativos, três posições AX, barra e assinatura")
        break
    time.sleep(0.2)
else:
    raise RuntimeError("A instância instalada não concluiu o layout; consulte a permissão/log")
