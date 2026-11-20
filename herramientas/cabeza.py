#!/usr/bin/env python3
"""Dónde está la cabeza del presentador en cada cuadro (Vision de macOS, local y gratis).

Regla dura: NUNCA cortarle la cabeza. La gorra o el pelo queda ≥ 30 px lejos de cualquier panel o tarjeta,
en TODOS los cuadros (cuando alguien se estira, la cabeza sube ~60 px: por eso se mide todo, no un cuadro).

  tope de la cabeza ≈ y de la cara − 0,45 × alto de la cara   (conservador, también con gorra)

Qué imprime:
  - por ventanas de 10 s: el tope de cabeza más alto y la barbilla más baja (px del video)
  - con --panel 990 --tramos "4.8-18.7,…": cuántos px hay que BAJAR el video en cada tramo de pantalla
    partida para que la cabeza quede ≥ --margen px debajo del borde del panel

Salida: <nombre>.cabeza.json  {"fps", "ancho", "alto", "cuadros": [[t, tope, barbilla, cx] | null]}

Uso:
  herramientas/cabeza.py videos/reel.mp4
  herramientas/cabeza.py videos/reel.mp4 --panel 990 --tramos "4.8-18.7,101.8-120.7" --margen 34
"""
import argparse
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import binario, correr, falla, guardar_json, info, rangos  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--fps", type=float, default=5)
    ap.add_argument("--panel", type=float, help="alto del panel de la pantalla partida, en px del video (ej. 990)")
    ap.add_argument("--tramos", default="", help='tramos con pantalla partida, "a-b,c-d"')
    ap.add_argument("--margen", type=float, default=30)
    ap.add_argument("--ventana", type=float, default=10)
    a = ap.parse_args()
    if not os.path.isfile(a.video):
        falla(f"no existe {a.video}")
    inf = info(a.video)
    W, H = inf["ancho"], inf["alto"]
    caras = binario("caras")
    tmp = tempfile.mkdtemp()
    try:
        ew = 540 if W <= H else 960
        correr(["ffmpeg", "-v", "error", "-i", a.video, "-vf", f"fps={a.fps},scale={ew}:-2", os.path.join(tmp, "f%06d.png")])
        out = os.path.join(tmp, "caras.json")
        correr([caras, tmp, out])
        datos = json.load(open(out))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    cuadros = []
    for k, f in enumerate(datos):
        t = round(k / a.fps, 3)
        caras_ok = [c for c in f["faces"] if c[4] > 0.5]
        if not caras_ok:
            cuadros.append(None)
            continue
        x, y, w, h = max(caras_ok, key=lambda c: c[2] * c[3])[:4]   # la cara más grande
        tope = (y - 0.45 * h) * H
        barbilla = (y + h) * H
        cuadros.append([t, round(tope, 1), round(barbilla, 1), round((x + w / 2) * W, 1)])
    base = os.path.splitext(a.video)[0]
    guardar_json({"fps": a.fps, "ancho": W, "alto": H, "cuadros": cuadros}, f"{base}.cabeza.json")

    vistos = [c for c in cuadros if c]
    sin = len(cuadros) - len(vistos)
    print(f"{len(cuadros)} cuadros medidos · {sin} sin cara{' (revisa esos tramos a ojo)' if sin else ''}")
    if not vistos:
        return
    print(f"\nVentanas de {a.ventana:.0f} s (px del video {W}×{H}):")
    dur = vistos[-1][0]
    for i in range(math.ceil((dur + 0.001) / a.ventana)):
        v = [c for c in vistos if i * a.ventana <= c[0] < (i + 1) * a.ventana]
        if v:
            print(f"  {i * a.ventana:6.1f}–{(i + 1) * a.ventana:6.1f} s  tope de cabeza ≥ {min(c[1] for c in v):6.0f}  ·  barbilla ≤ {max(c[2] for c in v):6.0f}")
    if a.panel and a.tramos:
        print(f"\nPantalla partida con panel de {a.panel:.0f} px y margen de {a.margen:.0f} px:")
        for ta, tb in rangos(a.tramos):
            v = [c for c in vistos if ta - 0.6 <= c[0] <= tb + 0.6]   # incluye la transición de 0,5 s
            if not v:
                print(f"  {ta}-{tb}: sin cara medida")
                continue
            tope = min(c[1] for c in v)
            bajar = max(0, math.ceil(a.panel + a.margen - tope))
            print(f"  {ta:7.2f}–{tb:7.2f} s  tope mínimo {tope:5.0f} → bajar el video {bajar} px  (barbilla queda en ≤ {max(c[2] for c in v) + bajar:.0f})")


if __name__ == "__main__":
    main()
