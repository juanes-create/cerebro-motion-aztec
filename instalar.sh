#!/bin/zsh
# Instala (o solo revisa) todo lo que necesita el cerebro de motion en una Mac.
#   ./instalar.sh            revisa y pregunta antes de instalar cada cosa que falte
#   ./instalar.sh --revisar  solo revisa y dice qué falta (no instala nada)
cd "${0:h}"
REVISAR=0; [ "$1" = "--revisar" ] && REVISAR=1
ok()   { print -P "%F{green}✓%f $1"; }
mal()  { print -P "%F{red}✗%f $1"; FALTA=1; }
aviso(){ print -P "%F{yellow}!%f $1"; }
pedir(){ [ $REVISAR = 1 ] && return 1; read -q "?$1 [s/N] " r; echo; [ "$r" = "s" ] || [ "$r" = "y" ]; }
FALTA=0

echo "── Sistema"
if [ "$(uname)" = "Darwin" ]; then
  V=$(sw_vers -productVersion); ok "macOS ${V}"
  [ "${V%%.*}" -ge 14 ] || aviso "las herramientas de Vision (caras, recortes) piden macOS 14 o más nuevo"
  [ "$(uname -m)" = "arm64" ] || aviso "Mac Intel: funciona, pero Whisper y los renders van más lentos"
else
  aviso "No es una Mac: Whisper, ffmpeg y Remotion funcionan, pero las herramientas de Vision (cabeza, hablante, OCR, recortes, QR) y hdr_a_sdr.sh no."
fi

echo "── Programas"
if ! command -v brew >/dev/null; then
  mal "falta Homebrew → instálalo desde https://brew.sh y vuelve a correr este script"
else
  for p in ffmpeg node whisper-cpp; do
    exe=$p; [ $p = whisper-cpp ] && exe=whisper-cli
    if command -v $exe >/dev/null; then ok "$p"
    elif pedir "Falta $p. ¿Lo instalo con brew?"; then brew install $p && ok "$p"
    else mal "falta $p (brew install $p)"; fi
  done
fi
if command -v node >/dev/null; then
  NV=$(node -v | tr -d v | cut -d. -f1)
  [ "$NV" -ge 22 ] && ok "Node $(node -v)" || aviso "Node $(node -v): Remotion pide ≥ 18 y HyperFrames ≥ 22 (brew upgrade node)"
fi
if python3 -c "import numpy" 2>/dev/null; then ok "python3 + numpy"
elif pedir "Falta numpy para python3. ¿Lo instalo (pip3 install --user numpy)?"; then pip3 install --user numpy && ok "numpy"
else mal "falta numpy (pip3 install --user numpy)"; fi

echo "── Modelo de Whisper (large-v3-turbo, 1,6 GB, se guarda en modelos/)"
# mismos lugares donde lo busca herramientas/comun.py; (N) = sin error si no hay coincidencias
M=""
[ -n "$WHISPER_MODEL" ] && [ -f "$WHISPER_MODEL" ] && M="$WHISPER_MODEL"
# se prefiere large-v3-turbo; los modelos «.en» solo entienden inglés y no sirven
[ -z "$M" ] && M=$(print -l modelos/ggml-*.bin(N) ~/.cache/whisper/ggml-*.bin(N) ~/Library/Application\ Support/*/models/ggml-*.bin(N) | grep -v '\.en\.bin$' | sort -t/ -k1,1 | awk '/large-v3-turbo/{print; f=1; exit} {a[NR]=$0} END{if(!f && NR) print a[1]}')
if [ -n "$M" ]; then ok "modelo: $M"
elif pedir "¿Descargo el modelo de Whisper (1,6 GB, de huggingface.co/ggerganov/whisper.cpp)?"; then
  mkdir -p modelos && curl -L --fail -o modelos/ggml-large-v3-turbo.bin.part \
    "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin" \
    && mv modelos/ggml-large-v3-turbo.bin.part modelos/ggml-large-v3-turbo.bin && ok "modelo descargado"
else mal "falta el modelo de Whisper (corre ./instalar.sh y acepta la descarga, o define WHISPER_MODEL)"; fi

echo "── Herramientas de Vision (Swift)"
if [ "$(uname)" = "Darwin" ]; then
  if ls herramientas/bin/caras herramientas/bin/bocas herramientas/bin/ocr herramientas/bin/quitar_fondo herramientas/bin/qr >/dev/null 2>&1; then ok "compiladas en herramientas/bin/"
  elif ! command -v swiftc >/dev/null; then mal "falta swiftc (xcode-select --install)"
  elif [ $REVISAR = 0 ]; then herramientas/swift/compilar.sh || mal "no compilaron las herramientas de Vision"
  else mal "sin compilar (herramientas/swift/compilar.sh)"; fi
fi

echo "── Skills de Claude Code"
for s in hyperframes remotion-best-practices; do
  if [ -e ~/.claude/skills/$s ] || [ -e ~/.agents/skills/$s ]; then ok "skill $s"
  else
    repo=heygen-com/hyperframes; [ $s = remotion-best-practices ] && repo=remotion-dev/skills
    if pedir "Falta la skill $s. ¿La instalo (npx skills add $repo -g)?"; then npx --yes skills add $repo -g && ok "skills de $repo"
    else mal "falta la skill $s (npx skills add $repo -g)"; fi
  fi
done

echo "── Marca"
if grep -q "^estado: sin-configurar" MARCA.md 2>/dev/null; then
  aviso "MARCA.md está con la marca Aztec de ejemplo: el agente te preguntará tus colores, letra y cuenta la primera vez"
else ok "MARCA.md configurada"; fi

echo
[ $FALTA = 0 ] && ok "Todo listo. Abre esta carpeta en Claude Code y pide: «edítame este reel: videos/mi-video.mp4»" \
              || aviso "Falta algo de lo de arriba. Corre ./instalar.sh (sin --revisar) para instalarlo."
exit $FALTA
