#!/usr/bin/env python3
"""Limpia la voz de un bruto sin que se note el filtro.

Pensado para los reels grabados con audífonos/micro de escritorio que llegan
opacos (energía amontonada en 150-500 Hz, casi nada arriba de 7 kHz) y bajos.
No hace reducción de ruido por defecto: esos brutos suelen venir ya con gate
(silencios en -100 dB) y un denoiser encima solo mete artefactos.

Cadena (suave a propósito):
  1. highpass 75 Hz          → quita retumbe y golpes de mesa
  2. -3 dB en 300 Hz (Q 1.1) → quita el "barro"/caja
  3. +2.5 dB en 3.2 kHz      → presencia, que se entiendan las consonantes
  4. +1.5 dB shelf 6.5 kHz   → un poco de aire (hasta donde da la fuente)
  5. compresor 2.5:1 lento   → nivela frases sin aplastar
  6. loudnorm -14 LUFS, TP -1.5 (dos pasadas) → nivel estándar de reels

Uso:
  python3 limpiar_voz.py ENTRADA SALIDA.wav [--denoise]
La salida es solo audio (WAV 48 kHz estéreo), para montarla sobre el video.
"""
import json
import subprocess
import sys

EQ = (
    "highpass=f=75:poles=2,"
    "equalizer=f=300:t=q:w=1.1:g=-3,"
    "equalizer=f=3200:t=q:w=1.0:g=2.5,"
    "treble=g=1.5:f=6500:t=q:w=0.7,"
    "acompressor=threshold=-24dB:ratio=2.5:attack=15:release=180:makeup=2"
)
TARGET = "I=-14:TP=-1.5:LRA=7"


def run(args):
    return subprocess.run(args, capture_output=True, text=True, check=True)


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    src, dst = sys.argv[1], sys.argv[2]
    chain = ("afftdn=nr=8:nf=-45," if "--denoise" in sys.argv else "") + EQ

    # Pasada 1: medir
    r = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", src, "-vn", "-af",
         f"{chain},loudnorm={TARGET}:print_format=json", "-f", "null", "-"],
        capture_output=True, text=True)
    m = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])

    # Pasada 2: aplicar con las medidas (lineal, sin bombeo)
    ln = (f"loudnorm={TARGET}:measured_I={m['input_i']}:measured_TP={m['input_tp']}"
          f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}"
          f":offset={m['target_offset']}:linear=true")
    run(["ffmpeg", "-y", "-hide_banner", "-v", "error", "-i", src, "-vn",
         "-af", f"{chain},{ln}", "-ar", "48000", "-ac", "2", dst])

    # Verificación
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", dst, "-af", "ebur128=peak=true",
                        "-f", "null", "-"], capture_output=True, text=True)
    tail = r.stderr[r.stderr.rindex("Summary:"):]
    print(f"entrada: {m['input_i']} LUFS, pico {m['input_tp']} dBTP")
    print("salida:", " ".join(l.strip() for l in tail.splitlines() if l.strip().startswith(("I:", "Peak:"))))


if __name__ == "__main__":
    main()
