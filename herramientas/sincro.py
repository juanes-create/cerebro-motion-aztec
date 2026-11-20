#!/usr/bin/env python3
"""Sincroniza dos grabaciones por su AUDIO (cámara y grabación de pantalla, dos cámaras, un bruto y su versión editada).

Si el presentador grabó la pantalla mientras hablaba, el micrófono de esa grabación oye lo mismo que la cámara:
la correlación del audio da el desfase exacto. Con una base YA cortada, el desfase cambia en cada corte: --fino
lo mide cada 0,1 s y devuelve los tramos de desfase constante (para cortar la pantalla con esos mismos tramos).

  desfase = segundo en B − segundo en A   →   lo que pasa en A en t, pasa en B en t + desfase

Uso:
  herramientas/sincro.py camara.mp4 pantalla.mov                     # un solo desfase
  herramientas/sincro.py base-cortada.mp4 pantalla.mov --fino --desde 10 --hasta 60
Salida con --fino: <A>.sincro.json  [{"a", "b", "desfase", "n"}]  (segundos de A)

Ojo con las grabaciones de pantalla de macOS: llegan a una carpeta temporal NSIRD_screencaptureui_* que se borra
sola; cópiala YA con comodín (…/NSIRD_screencaptureui_xxx/*.mov): la ruta escrita a mano falla por las tildes.
"""
import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import falla, guardar_json, leer_audio  # noqa: E402

SR = 8000


def blanco(x):
    return np.diff(x, prepend=0).astype(np.float64)   # resalta transitorios: correlación más nítida


def global_(a, b):
    n = 1 << int(np.ceil(np.log2(len(a) + len(b))))
    c = np.fft.irfft(np.fft.rfft(b, n) * np.conj(np.fft.rfft(a, n)), n)
    k = int(np.argmax(c))
    if k > n // 2:
        k -= n
    calidad = float(c.max() / (np.sqrt((a ** 2).sum() * (b ** 2).sum()) + 1e-9))
    return k / SR, calidad


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("A")
    ap.add_argument("B")
    ap.add_argument("--fino", action="store_true")
    ap.add_argument("--desde", type=float, default=0)
    ap.add_argument("--hasta", type=float)
    ap.add_argument("--paso", type=float, default=0.1)
    ap.add_argument("--ventana", type=float, default=1.2)
    a = ap.parse_args()
    for p in (a.A, a.B):
        if not os.path.isfile(p):
            falla(f"no existe {p}")
    xa, xb = blanco(leer_audio(a.A, SR)), blanco(leer_audio(a.B, SR))

    if not a.fino:
        d, q = global_(xa, xb)
        print(f"desfase = {d:+.3f} s  (calidad {q:.2f}; > 0,2 es confiable)")
        print(f"→ lo que pasa en A en t, pasa en B en t {'+' if d >= 0 else '−'} {abs(d):.3f} s")
        return

    L = int(a.ventana * SR)
    N = 1 << int(np.ceil(np.log2(len(xb) + 2 * L)))
    PB = np.fft.rfft(xb, N)
    acum = np.concatenate([[0], np.cumsum(xb ** 2)])
    hasta = a.hasta or len(xa) / SR - a.ventana
    puntos = []
    for t in np.arange(a.desde, hasta, a.paso):
        i = int(t * SR)
        seg = xa[i:i + L]
        if len(seg) < L or np.sqrt((seg ** 2).mean()) < 2e-3:
            continue   # silencio: no hay nada que correlacionar
        c = np.fft.irfft(np.fft.rfft(seg[::-1], N) * PB, N)[L - 1:L - 1 + len(xb) - L]
        en = np.sqrt(acum[L:L + len(c)] - acum[:len(c)]) * np.sqrt((seg ** 2).sum()) + 1e-9
        nc = c / en
        j = int(np.argmax(nc))
        if nc[j] > 0.45:
            puntos.append((round(t + a.ventana / 2, 2), j / SR - t))
    tramos = []
    for t, d in puntos:
        if tramos and abs(d - tramos[-1]["ds"][-1]) < 0.05:
            tramos[-1]["b"] = t
            tramos[-1]["ds"].append(d)
        else:
            tramos.append({"a": t, "b": t, "ds": [d]})
    tramos = [{"a": round(x["a"] - a.ventana / 2, 2), "b": round(x["b"] + a.ventana / 2, 2),
               "desfase": round(float(np.median(x["ds"])), 3), "n": len(x["ds"])} for x in tramos if len(x["ds"]) >= 3]
    for x in tramos:
        print(f"  {x['a']:8.2f}–{x['b']:8.2f} s de A  →  desfase {x['desfase']:+.3f} s  ({x['n']} medidas)")
    guardar_json(tramos, f"{os.path.splitext(a.A)[0]}.sincro.json")
    print(f"✓ {len(tramos)} tramos → {os.path.splitext(a.A)[0]}.sincro.json")


if __name__ == "__main__":
    main()
