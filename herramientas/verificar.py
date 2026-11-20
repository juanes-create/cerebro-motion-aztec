#!/usr/bin/env python3
"""Verificación antes de entregar. Nunca se entrega sin medir.

Subcomandos:
  streams  FINAL                 duración y cuadros de CADA stream (un audio cortado en silencio no da error)
  sincro   FINAL BASE            desfase del audio contra la base en 3 puntos (debe dar 0 ms; solo si la voz no se re-cortó)
  psnr     FINAL BASE a-b        lo que no se tocó sigue igual: PSNR ≥ ~42 dB fuera del motion
  volumen  FINAL [BASE]          loudness integrado (LUFS) y pico; con BASE, compara
  texto    FINAL                 transcribe el audio FINAL de corrido: léelo entero, ahí se ven las tomas que se colaron
  zonas    FINAL t1,t2,…         cuadros del entregable con las líneas de las zonas de peligro de un reel (y=270, y=1480, x=960)
  qr       FINAL                 lee el QR cada 0,1 s (Vision) y dice en qué segundos se puede escanear

Uso: herramientas/verificar.py streams "Reel EDITADO.mp4"
"""
import os
import re
import subprocess
import sys
import tempfile
import shutil

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import binario, correr, falla, info, leer_audio, rangos  # noqa: E402


def streams(f):
    print(correr(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name,duration,nb_frames,width,height",
                  "-of", "compact=p=0", f]).strip())
    d = [float(x) for x in re.findall(r"duration=([\d.]+)", correr(["ffprobe", "-v", "error", "-show_entries", "stream=duration", "-of", "compact=p=0", f]))]
    if len(d) >= 2 and abs(d[0] - d[1]) > 0.1:
        print(f"✗ los streams no duran lo mismo ({d[0]:.2f} vs {d[1]:.2f} s): revisa la mezcla")
    else:
        print("✓ streams del mismo largo")


def sincro(f, base):
    SR = 8000
    dur = min(info(f)["duracion"], info(base)["duracion"])
    for t in (dur * 0.15, dur * 0.5, dur * 0.85):
        a = leer_audio(f, SR, desde=t - 0.05, hasta=t + 8.05)
        b = leer_audio(base, SR, desde=t, hasta=t + 8)
        if len(a) < len(b) + 800 or np.abs(b).max() < 1e-4:
            continue
        c = np.correlate(a, b, "valid")
        lag = (int(np.argmax(c)) - 400) / SR * 1000
        print(f"  t={t:7.1f} s  desfase {lag:+.1f} ms")


def psnr(f, base, tramos):
    for ta, tb in rangos(tramos):
        r = subprocess.run(["ffmpeg", "-hide_banner", "-ss", str(ta), "-to", str(tb), "-i", f, "-ss", str(ta), "-to", str(tb), "-i", base,
                            "-lavfi", "[0:v][1:v]psnr", "-f", "null", "-"], capture_output=True, text=True)
        m = re.search(r"average:([\d.inf]+)", r.stderr)
        print(f"  {ta}-{tb} s  PSNR {m.group(1) if m else '?'} dB   (≥ 42 = igual)")


def volumen(f, base=None):
    for p in [f] + ([base] if base else []):
        r = subprocess.run(["ffmpeg", "-hide_banner", "-i", p, "-map", "0:a:0", "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
        tail = r.stderr[r.stderr.rfind("Summary:"):]
        i = re.search(r"I:\s+(-?[\d.]+) LUFS", tail)
        pk = re.search(r"Peak:\s+(-?[\d.]+) dBFS", tail)
        print(f"  {os.path.basename(p)}: {i.group(1) if i else '?'} LUFS · pico {pk.group(1) if pk else '?'} dBFS")


def texto(f):
    aqui = os.path.dirname(os.path.abspath(__file__))
    tmp = tempfile.mkdtemp()
    try:
        wav = os.path.join(tmp, "final.mp4")
        shutil.copy(f, wav)
        subprocess.run([sys.executable, os.path.join(aqui, "transcribir.py"), wav, "--carpeta", tmp], check=True)
        print("\n" + open(os.path.join(tmp, "final.frases.txt"), encoding="utf-8").read())
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def zonas(f, tiempos):
    inf = info(f)
    out = os.path.splitext(f)[0] + ".zonas.jpg"
    tmp = tempfile.mkdtemp()
    try:
        ts = [float(x) for x in tiempos.split(",")]
        for k, t in enumerate(ts):
            correr(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", f, "-frames:v", "1", "-vf",
                    "drawbox=y=270:w=iw:h=4:color=red@0.9:t=fill,drawbox=y=1480:w=iw:h=4:color=red@0.9:t=fill,"
                    "drawbox=x=960:w=4:h=ih:color=red@0.9:t=fill,scale=360:-2", os.path.join(tmp, f"z{k:03d}.png")])
        cols = min(6, len(ts))
        filas = -(-len(ts) // cols)
        correr(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(tmp, "z%03d.png"), "-vf", f"tile={cols}x{filas}", "-frames:v", "1", out])
        print(f"✓ {out}  (líneas rojas: arriba y=270, abajo y=1480, derecha x=960 · video {inf['ancho']}×{inf['alto']})")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def qr(f):
    tmp = tempfile.mkdtemp()
    try:
        correr(["ffmpeg", "-v", "error", "-i", f, "-vf", "fps=10", os.path.join(tmp, "q%06d.png")])
        print(correr([binario("qr"), tmp]).strip())
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cmd, args = sys.argv[1], sys.argv[2:]
    for p in args[:2]:
        if cmd in ("streams", "sincro", "psnr", "volumen", "texto", "zonas", "qr") and p is args[0] and not os.path.isfile(p):
            falla(f"no existe {p}")
    {"streams": lambda: streams(args[0]),
     "sincro": lambda: sincro(args[0], args[1]),
     "psnr": lambda: psnr(args[0], args[1], args[2]),
     "volumen": lambda: volumen(*args[:2]),
     "texto": lambda: texto(args[0]),
     "zonas": lambda: zonas(args[0], args[1]),
     "qr": lambda: qr(args[0])}.get(cmd, lambda: sys.exit(__doc__))()


if __name__ == "__main__":
    main()
