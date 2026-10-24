#!/bin/zsh
set -euo pipefail
cd "${0:A:h}"
if [[ -e "$HOME/Applications/Modo Desenvolvedor.app" && "${1:-}" != "--allow-rebuild" ]]; then
  print -u2 'Aplicativo já instalado. Não recompilar após conceder Acessibilidade. Use --allow-rebuild apenas para uma atualização deliberada.'
  exit 1
fi
mkdir -p build/'Modo Desenvolvedor.app'/Contents/MacOS
swiftc -O -parse-as-library -target arm64-apple-macosx13.0 Geometry.swift DeveloperMode.swift -o build/'Modo Desenvolvedor.app'/Contents/MacOS/ModoDesenvolvedor -framework AppKit -framework ApplicationServices -framework ServiceManagement
cp Info.plist build/'Modo Desenvolvedor.app'/Contents/Info.plist
codesign --force --sign - --identifier br.com.luizfilipe.modo-desenvolvedor build/'Modo Desenvolvedor.app'
codesign --verify --deep --strict --verbose=2 build/'Modo Desenvolvedor.app'
