#!/bin/zsh
# Render completo del reel en H.264 y SIN audio (el audio lo pone ./montar.sh: si va dentro del render, la voz se corre ~43 ms).
# Lánzalo en segundo plano en renders largos: nohup ./render.sh > out/render.log 2>&1 &
set -e
cd "${0:h}"
mkdir -p out
FREE=$(df -g . | awk 'NR==2{print $4}')
[ "${FREE}" -lt 5 ] && echo "⚠ quedan ${FREE} GB libres: Remotion escribe cada cuadro en TMPDIR; libera espacio o pon TMPDIR en otro disco (ruta absoluta)"
rm -rf build && npx remotion bundle src/index.ts --out-dir build --log=error >/dev/null
npx remotion render build Reel out/reel-sin-audio.mp4 --codec=h264 --crf=15 --muted --concurrency=${CONC:-6} --log=error
ffprobe -v error -count_packets -show_entries stream=nb_read_packets,width,height -of csv=p=0 out/reel-sin-audio.mp4
echo "✓ out/reel-sin-audio.mp4 → ahora ./montar.sh"
