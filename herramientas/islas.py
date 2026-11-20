#!/usr/bin/env python3
"""Parte un bruto en «islas» de voz (separadas por silencios) y transcribe cada isla SOLA.

Para qué: elegir qué toma queda. Si transcribes el bruto entero, Whisper fusiona las frases repetidas y la toma
fallida desaparece del texto. Isla por isla, cada repetición sale con su texto y su segundo.

Salidas (junto al video):
  <nombre>.islas.json  [{"i", "a", "b", "texto", "palabras": [{"w", "t0", "t1"}]}]
  <nombre>.islas.txt   una isla por línea: "#003  12.40–15.85  (3,4 s)  texto"   ← léelo y decide

Después, corta con: cortar.py VIDEO --quitar "a-b,..."  (o --solo con las islas buenas)

Uso: herramientas/islas.py videos/bruto.mp4 [--idioma es] [--hueco 0.28]
"""
import argparse
import json
import os
import sys
import tempfile

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import energia_db, falla, guardar_json, leer_audio  # noqa: E402
from transcribir import SR, escribir_wav, whisper  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--idioma", default="es")
    ap.add_argument("--hueco", type=float, default=0.28, help="silencios más cortos que esto no separan islas")
    ap.add_argument("--minima", type=float, default=0.15, help="islas más cortas que esto se descartan")
    a = ap.parse_args()
    if not os.path.isfile(a.video):
        falla(f"no existe {a.video}")

    x = leer_audio(a.video, SR)
    env = energia_db(x, SR)
    piso, alto = np.percentile(env, 10), np.percentile(env, 95)
    on = env > piso + max(8.0, 0.2 * (alto - piso))
    segs, s = [], None
    for k, v in enumerate(np.append(on, False)):
        if v and s is None:
            s = k
        if not v and s is not None:
            segs.append([s, k])
            s = None
    unidas = []
    for i0, i1 in segs:
        if unidas and (i0 - unidas[-1][1]) * 0.01 < a.hueco:
            unidas[-1][1] = i1
        else:
            unidas.append([i0, i1])
    islas = [(i0, i1) for i0, i1 in unidas if (i1 - i0) * 0.01 >= a.minima and env[i0:i1].max() > alto - 14]
    print(f"{len(islas)} islas de voz")

    res = []
    with tempfile.TemporaryDirectory() as tmp:
        archivos = []
        for n, (i0, i1) in enumerate(islas):
            s0, s1 = max(0, (i0 - 8) * SR // 100), min(len(x), (i1 + 8) * SR // 100)
            f = os.path.join(tmp, f"i{n:04d}.wav")
            escribir_wav(f, x[s0:s1])
            archivos.append((f, s0 / SR))
        r = whisper([f for f, _ in archivos], a.idioma)
        if not os.path.isfile(archivos[0][0] + ".csv"):
            r = whisper([f for f, _ in archivos], a.idioma, gpu=False)
        import csv
        for n, ((f, off), (i0, i1)) in enumerate(zip(archivos, islas)):
            pal = []
            if os.path.isfile(f + ".csv"):
                for row in csv.DictReader(open(f + ".csv", encoding="utf-8", errors="replace")):
                    w = row["text"].strip()
                    if w and any(c.isalnum() for c in w):
                        pal.append({"w": w, "t0": round(off + int(row["start"]) / 1000, 3), "t1": round(off + int(row["end"]) / 1000, 3)})
            res.append({"i": n, "a": round(i0 * 0.01, 2), "b": round(i1 * 0.01, 2), "texto": " ".join(p["w"] for p in pal), "palabras": pal})

    base = os.path.splitext(a.video)[0]
    guardar_json(res, f"{base}.islas.json")
    lineas = [f"#{s['i']:03d}  {s['a']:7.2f}–{s['b']:7.2f}  ({s['b'] - s['a']:4.1f} s)  {s['texto']}" for s in res]
    open(f"{base}.islas.txt", "w", encoding="utf-8").write("\n".join(lineas) + "\n")
    print("\n".join(lineas[:60]) + ("\n…" if len(lineas) > 60 else ""))
    print(f"✓ {base}.islas.json\n✓ {base}.islas.txt")


if __name__ == "__main__":
    main()
