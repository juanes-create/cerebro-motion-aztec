#!/bin/zsh
# Compila las herramientas de Vision (solo Mac, macOS 14 o más nuevo) en herramientas/bin/.
set -e
cd "${0:h}"
mkdir -p ../bin
for f in *.swift; do
  n="${f:r}"
  swiftc -O "$f" -o "../bin/${n}" 2>&1 | grep -v "^$" || true
  [ -x "../bin/${n}" ] && echo "✓ ${n}" || { echo "✗ no compiló ${n}"; exit 1; }
done
