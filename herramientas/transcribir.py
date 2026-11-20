#!/usr/bin/env python3
"""Transcribe un video o audio con tiempos POR PALABRA (Whisper local, gratis y sin subir nada).

Por qué así:
  - Sobre audios largos, Whisper redondea los tiempos y fusiona frases. Aquí el audio se parte en ventanas
    de ~9 s, cada corte en el punto de menor energía (nunca a mitad de palabra), y se transcribe cada una sola.
  - `--prompt` de Whisper corre los tiempos: no se usa.

Salidas (en --carpeta, por defecto junto al video):
  <nombre>.palabras.json   [{"w": "hola", "t0": 1.23, "t1": 1.51}, ...]   (segundos del video original)
  <nombre>.frases.txt      una frase por línea con su segundo de inicio y fin (para leerlo rápido)

Uso:
  herramientas/transcribir.py videos/mi-reel.mp4
  herramientas/transcribir.py videos/largo.mp4 --desde 60 --hasta 180 --idioma es
"""
import argparse
import csv
import os
import subprocess
import sys
import tempfile
import wave

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import correr, energia_db, falla, guardar_json, info, leer_audio, modelo_whisper, whisper_cli  # noqa: E402

SR = 16000


def ventanas(x, largo=9.0, minimo=7.0, maximo=10.5):
    """Cortes cada ~9 s en el valle de energía entre 7 y 9,8 s."""
    db = energia_db(x, SR)
    T = len(x) / SR
    cortes = [0.0]
    while T - cortes[-1] > maximo:
        i0, i1 = int((cortes[-1] + minimo) * 100), int((cortes[-1] + largo + 0.8) * 100)
        i1 = min(i1, len(db))
        cortes.append((i0 + int(np.argmin(db[i0:i1]))) / 100)
    cortes.append(T)
    return cortes


def escribir_wav(ruta, x):
    with wave.open(ruta, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


def whisper(archivos, idioma, gpu=True):
    args = [whisper_cli(), "-m", modelo_whisper(), "-l", idioma, "-ml", "1", "-sow", "-ocsv", "-t", "8"]
    if not gpu:
        args.append("-ng")
    for f in archivos:
        args += ["-f", f]
    return subprocess.run(args, capture_output=True, text=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entrada")
    ap.add_argument("--desde", type=float, default=0.0)
    ap.add_argument("--hasta", type=float)
    ap.add_argument("--idioma", default="es")
    ap.add_argument("--carpeta")
    ap.add_argument("--pausa-frase", type=float, default=0.35, help="silencio que separa frases en el .txt")
    a = ap.parse_args()

    if not os.path.isfile(a.entrada):
        falla(f"no existe {a.entrada}")
    dur = info(a.entrada)["duracion"]
    hasta = min(a.hasta or dur, dur)
    x = leer_audio(a.entrada, SR, desde=a.desde, hasta=hasta)
    cortes = ventanas(x)
    base = os.path.splitext(os.path.basename(a.entrada))[0]
    carpeta = a.carpeta or os.path.dirname(os.path.abspath(a.entrada))

    with tempfile.TemporaryDirectory() as tmp:
        archivos = []
        for k in range(len(cortes) - 1):
            f = os.path.join(tmp, f"v{k:04d}.wav")
            escribir_wav(f, x[int(cortes[k] * SR): int(cortes[k + 1] * SR)])
            archivos.append(f)
        print(f"{len(archivos)} ventanas de ~9 s · {hasta - a.desde:.1f} s de audio")
        r = whisper(archivos, a.idioma, gpu=True)
        if not all(os.path.isfile(f[:-4] + ".csv") or os.path.isfile(f + ".csv") for f in archivos):
            print("· Whisper con GPU falló (pasa dentro de un sandbox); reintento sin GPU, es más lento…")
            r = whisper(archivos, a.idioma, gpu=False)
        palabras = []
        for k, f in enumerate(archivos):
            csvp = f + ".csv" if os.path.isfile(f + ".csv") else f[:-4] + ".csv"
            if not os.path.isfile(csvp):
                falla(f"Whisper no devolvió la ventana {k}: {r.stderr[-400:]}")
            off = a.desde + cortes[k]
            for row in csv.DictReader(open(csvp, encoding="utf-8", errors="replace")):
                w = row["text"].strip()
                if w and any(c.isalnum() for c in w):
                    palabras.append({"w": w, "t0": round(off + int(row["start"]) / 1000, 3),
                                     "t1": round(off + int(row["end"]) / 1000, 3)})

    j = os.path.join(carpeta, f"{base}.palabras.json")
    guardar_json(palabras, j)
    # frases: se parte donde hay una pausa larga o un punto
    lineas, actual = [], []
    for i, p in enumerate(palabras):
        actual.append(p)
        sig = palabras[i + 1] if i + 1 < len(palabras) else None
        if sig is None or sig["t0"] - p["t1"] > a.pausa_frase or p["w"][-1:] in ".?!":
            lineas.append(f"[{actual[0]['t0']:7.2f} – {actual[-1]['t1']:7.2f}]  " + " ".join(q["w"] for q in actual))
            actual = []
    t = os.path.join(carpeta, f"{base}.frases.txt")
    open(t, "w", encoding="utf-8").write("\n".join(lineas) + "\n")
    print(f"✓ {len(palabras)} palabras → {j}\n✓ {len(lineas)} frases → {t}")


if __name__ == "__main__":
    main()
