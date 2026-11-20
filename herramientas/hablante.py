#!/usr/bin/env python3
"""¿Quién habla en cada isla? Separa al presentador de la gente que habla fuera de cámara (o a dos presentadores).

Dos señales, medidas por isla (sale de islas.py):
  - NIVEL de la voz: el presentador (micrófono cerca) está ~15-25 dB por encima de quien habla detrás de cámara.
  - BOCA en movimiento: desviación de la apertura de los labios (Vision, `innerLips`, 10 cuadros/s).
    Con dos personas en cuadro, gana la boca que más se mueve (izquierda o derecha).

Salida: <nombre>.hablante.json y una tabla: isla, nivel, boca izq/der y veredicto
  («presentador», «izquierda», «derecha» o «fuera de cámara»).

Uso: herramientas/hablante.py videos/bruto.mp4   (antes: herramientas/islas.py videos/bruto.mp4)
"""
import argparse
import json
import os
import shutil
import sys
import tempfile

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import binario, correr, energia_db, falla, guardar_json, leer_audio  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--islas", help="por defecto <nombre>.islas.json")
    ap.add_argument("--caida", type=float, default=12, help="dB bajo el nivel típico para llamarlo «fuera de cámara»")
    a = ap.parse_args()
    base = os.path.splitext(a.video)[0]
    ruta_islas = a.islas or f"{base}.islas.json"
    if not os.path.isfile(ruta_islas):
        falla(f"no existe {ruta_islas}: corre antes herramientas/islas.py {a.video}")
    islas = json.load(open(ruta_islas, encoding="utf-8"))

    x = leer_audio(a.video, 16000)
    db = energia_db(x, 16000)
    tmp = tempfile.mkdtemp()
    try:
        correr(["ffmpeg", "-v", "error", "-i", a.video, "-vf", "fps=10,scale=1080:-2", os.path.join(tmp, "f%06d.png")])
        out = os.path.join(tmp, "bocas.json")
        correr([binario("bocas"), tmp, out])
        bocas = json.load(open(out))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    L = np.full(len(bocas), np.nan)
    R = np.full(len(bocas), np.nan)
    for k, f in enumerate(bocas):
        for cx, cy, h, ap_ in f["faces"]:
            if ap_ < 0:
                continue
            if cx < 0.5:
                L[k] = ap_ / max(h, 1e-3)
            else:
                R[k] = ap_ / max(h, 1e-3)

    niveles = []
    for s in islas:
        seg = db[int(s["a"] * 100): int(s["b"] * 100) + 1]
        niveles.append(float(np.percentile(seg, 90)) if len(seg) else -120)
    tipico = float(np.median(sorted(niveles)[len(niveles) // 3:])) if niveles else -20
    res = []
    print(f"nivel típico del presentador: {tipico:.1f} dBFS\n")
    for s, nv in zip(islas, niveles):
        i0, i1 = int(s["a"] * 10), int(s["b"] * 10) + 1
        mov = lambda v: float(np.nanstd(np.diff(v[i0:i1]))) if i1 - i0 > 3 and np.isfinite(v[i0:i1]).sum() > 3 else 0.0
        ml, mr = mov(L), mov(R)
        dos = np.isfinite(L).mean() > 0.3 and np.isfinite(R).mean() > 0.3
        if nv < tipico - a.caida and max(ml, mr) < 0.02:
            quien = "fuera de cámara"
        elif dos:
            quien = "izquierda" if ml > mr * 1.25 else "derecha" if mr > ml * 1.25 else "?"
        else:
            quien = "presentador"
        res.append({"i": s["i"], "a": s["a"], "b": s["b"], "quien": quien, "nivel": round(nv, 1), "boca_izq": round(ml, 4), "boca_der": round(mr, 4)})
        print(f"#{s['i']:03d} {s['a']:7.2f}–{s['b']:7.2f}  {nv:6.1f} dB  boca {ml:.3f}/{mr:.3f}  {quien:16} {s['texto'][:60]}")
    guardar_json(res, f"{base}.hablante.json")
    print(f"\n✓ {base}.hablante.json   (revisa a oído las islas con «?»)")


if __name__ == "__main__":
    main()
