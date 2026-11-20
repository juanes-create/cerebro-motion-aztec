#!/usr/bin/env python3
"""Encuentra las pantallas negras de un video largo (donde va el motion) y, opcional, la burbuja de cámara.

Flujo de YouTube: el editor deja en negro los tramos donde quiere motion, con la burbuja de cámara encima.
  1. Decodifica SOLO los keyframes (2 h 35 min en ~2,5 min) a 96×54 en gris: luminancia media < --umbral = negro.
  2. Afina cada borde cuadro a cuadro.
  3. Con --burbuja, guarda la caja de la burbuja en CADA cuadro de cada tramo (no es fija: salta y hace zooms).

Salida: <nombre>.negros.json  {"fps", "tramos": [{"a", "b", "a_cuadro", "b_cuadro"}], "burbuja": {cuadro: [x, y, w, h]}}

Uso:
  herramientas/negros.py videos/clase.mp4
  herramientas/negros.py videos/clase.mp4 --zona 0,0,0.6,1 --burbuja
  (--zona x,y,w,h normalizada: dónde mirar el negro, fuera de la burbuja; por defecto la mitad izquierda)
"""
import argparse
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import falla, guardar_json, info  # noqa: E402


def lumas(video, ss=None, t=None, zona=(0, 0, 0.5, 1), w=96, h=54, solo_clave=False):
    # showinfo escribe el tiempo de cada keyframe a nivel «info»: con -v error no saldría nada
    args = ["ffmpeg", "-hide_banner", "-nostats", "-v", "info" if solo_clave else "error"]
    if solo_clave:
        args += ["-skip_frame", "nokey"]
    if ss is not None:
        args += ["-ss", f"{ss:.3f}"]
    if t is not None:
        args += ["-t", f"{t:.3f}"]
    args += ["-i", video, "-vf", f"scale={w}:{h},format=gray", "-fps_mode", "passthrough", "-f", "rawvideo", "-"]
    if solo_clave:
        args[args.index("-vf") + 1] = f"scale={w}:{h},format=gray,showinfo"
    r = subprocess.run(args, capture_output=True)
    fr = np.frombuffer(r.stdout, np.uint8).reshape(-1, h, w).astype(np.float32)
    x0, y0, zw, zh = zona
    sub = fr[:, int(y0 * h): int((y0 + zh) * h), int(x0 * w): int((x0 + zw) * w)]
    pts = []
    if solo_clave:
        for line in r.stderr.decode("utf-8", "replace").splitlines():
            if "pts_time:" in line:
                pts.append(float(line.split("pts_time:")[1].split()[0]))
    return sub.mean((1, 2)), pts, fr


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--umbral", type=float, default=20)
    ap.add_argument("--zona", default="0,0,0.5,1")
    ap.add_argument("--burbuja", action="store_true")
    ap.add_argument("--minimo", type=float, default=1.0, help="tramos negros más cortos que esto se ignoran")
    a = ap.parse_args()
    if not os.path.isfile(a.video):
        falla(f"no existe {a.video}")
    inf = info(a.video)
    fps = inf["fps"]
    zona = tuple(float(v) for v in a.zona.split(","))

    y, pts, _ = lumas(a.video, zona=zona, solo_clave=True)
    n = min(len(y), len(pts))
    negro = y[:n] < a.umbral
    print(f"{n} keyframes revisados")
    # (keyframe anterior, primer keyframe negro, último keyframe negro, keyframe siguiente)
    gruesos, s = [], None
    for k in range(n):
        if negro[k] and s is None:
            s = k
        if (not negro[k] or k == n - 1) and s is not None:
            u = k - 1 if not negro[k] else k
            gruesos.append((pts[s - 1] if s > 0 else 0.0, pts[s], pts[u], pts[u + 1] if u + 1 < n else inf["duracion"]))
            s = None

    def borde(t0, t1, entra):
        """primer cuadro negro (entra) o primer cuadro NO negro después del tramo (sale), cuadro a cuadro"""
        yy, _, _ = lumas(a.video, ss=max(0, t0), t=t1 - t0 + 0.1, zona=zona)
        idx = np.nonzero(yy < a.umbral)[0]
        if len(idx) == 0:
            return None
        k = idx[0] if entra else idx[-1] + 1
        return round(max(0, t0) * fps) + int(k)

    tramos = []
    for k_ant, k_ini, k_fin, k_sig in gruesos:
        ca = borde(k_ant, k_ini, True)
        cb = borde(k_fin, k_sig, False)
        if ca is None or cb is None or (cb - ca) / fps < a.minimo:
            continue
        tramos.append({"a": round(ca / fps, 3), "b": round(cb / fps, 3), "a_cuadro": ca, "b_cuadro": cb})
    for t in tramos:
        print(f"  negro {t['a']:9.3f} – {t['b']:9.3f} s   (cuadros {t['a_cuadro']}–{t['b_cuadro']}, {t['b'] - t['a']:.1f} s)")

    res = {"fps": fps, "tramos": tramos}
    if a.burbuja and tramos:
        W, H = inf["ancho"], inf["alto"]
        caja = {}
        for t in tramos:
            # media resolución: píxeles > 30 (la burbuja es lo único que no es negro)
            ww, hh = W // 2, H // 2
            _, _, fr = lumas(a.video, ss=t["a"], t=t["b"] - t["a"], zona=(0, 0, 1, 1), w=ww, h=hh)
            for k, f in enumerate(fr):
                m = f > 30
                ys, xs = np.nonzero(m)
                if len(xs) < 50:
                    continue
                caja[t["a_cuadro"] + k] = [int(xs.min()) * 2, int(ys.min()) * 2, int(xs.max() - xs.min() + 1) * 2, int(ys.max() - ys.min() + 1) * 2]
        res["burbuja"] = caja
        print(f"  burbuja medida en {len(caja)} cuadros")
    guardar_json(res, f"{os.path.splitext(a.video)[0]}.negros.json")
    print(f"✓ {len(tramos)} tramos → {os.path.splitext(a.video)[0]}.negros.json")


if __name__ == "__main__":
    main()
