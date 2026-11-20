#!/usr/bin/env python3
"""Cortes «súper fluidos»: toda pausa de más de 0,3 s queda en 0,2 s, y se quitan los tramos que le digas.

La regla (estándar Aztec):
  - Pausa > --min (0,3 s)  → queda en --pausa (0,2 s): 0,1 s después de la última palabra + 0,1 s antes de la siguiente.
  - Las pausas más cortas NO se tocan (quitarles 1-3 cuadros solo deja un salto sin ganar tiempo).
  - Arranque: 0,08 s antes de la primera palabra. Final: 0,5 s después de la última (más si hay un remate visual).
  - El audio es el ORIGINAL del bruto, cortado por muestra, con un fundido de 10 ms en cada unión.
  - Silencio = energía (cada 10 ms) por debajo de max(−40 dBFS, piso + 8 dB). El piso es el percentil 10.

Tomas repetidas, arranques fallidos, charla fuera de cámara o instrucciones dichas a la IA: se quitan con
--quitar "a-b,c-d" (segundos del bruto). Para elegirlos, mira antes `islas.py` (cada isla de voz con su texto).

Salidas (junto al video, o donde diga --salida):
  <nombre>.cortado.mp4    video + audio original cortado (H.264, keyframe cada 15 cuadros: Remotion lo busca rápido)
  <nombre>.voz.wav        el audio cortado, para mezclar efectos después
  <nombre>.cortes.json    {"fps", "duracion", "tramos": [{"a", "b", "r"}]}  a-b en el bruto, r = dónde arranca en el corte
  <nombre>.palabras-corte.json   (si pasas --palabras) las palabras con los tiempos del video cortado

Uso:
  herramientas/cortar.py videos/bruto.mp4
  herramientas/cortar.py videos/bruto.mp4 --quitar "0-3.4,41.2-47.9" --cola 0.9 --palabras videos/bruto.palabras.json
  herramientas/cortar.py videos/bruto.mp4 --solo "2.9-19.6,21.3-30" --ancho 1080
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
import wave

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import correr, energia_db, falla, guardar_json, info, leer_audio, rangos, umbral_silencio  # noqa: E402

SR = 48000
PASO = 0.01


def restar(bloques, quitar):
    res = []
    for a, b in bloques:
        partes = [(a, b)]
        for qa, qb in quitar:
            nuevas = []
            for pa, pb in partes:
                if qb <= pa or qa >= pb:
                    nuevas.append((pa, pb))
                else:
                    if qa > pa:
                        nuevas.append((pa, qa))
                    if qb < pb:
                        nuevas.append((qb, pb))
            partes = nuevas
        res += [p for p in partes if p[1] - p[0] > 0.05]
    return res


def silencios(sil, a, b, minimo):
    """Tramos de silencio continuo de más de `minimo` segundos entre a y b."""
    res, i, i1 = [], int(a / PASO), min(int(b / PASO), len(sil))
    while i < i1:
        if sil[i]:
            j = i
            while j < i1 and sil[j]:
                j += 1
            if (j - i) * PASO > minimo:
                res.append((i * PASO, j * PASO))
            i = j
        else:
            i += 1
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--pausa", type=float, default=0.2, help="pausa que queda (0,2 s)")
    ap.add_argument("--min", type=float, default=0.3, help="solo se cortan las pausas más largas que esto")
    ap.add_argument("--quitar", default="", help='tramos del bruto que salen, "a-b,c-d"')
    ap.add_argument("--solo", default="", help='solo estos tramos del bruto, "a-b,c-d" (bloques de voz)')
    ap.add_argument("--inicio", type=float, default=0.08, help="aire antes de la primera palabra")
    ap.add_argument("--cola", type=float, default=0.5, help="aire después de la última palabra")
    ap.add_argument("--umbral", type=float, help="dBFS de silencio (por defecto, automático)")
    ap.add_argument("--fps", type=float, help="cuadros por segundo de salida (por defecto, los del bruto)")
    ap.add_argument("--ancho", type=int, help="escalar a este ancho (ej. 1080 para un bruto 4K)")
    ap.add_argument("--palabras", help="palabras.json de transcribir.py, para pasarlas al video cortado")
    ap.add_argument("--salida", help="ruta del .mp4 de salida")
    ap.add_argument("--sin-video", action="store_true", help="solo calcula los cortes y el audio")
    ap.add_argument("--forzar", action="store_true", help="cortar aunque el bruto sea HDR")
    a = ap.parse_args()

    if not os.path.isfile(a.video):
        falla(f"no existe {a.video}")
    inf = info(a.video)
    if not inf["audio"]:
        falla("el video no tiene audio: no hay voz que medir")
    if inf.get("transferencia") in ("arib-std-b67", "smpte2084") and not a.forzar:
        falla("el bruto es HDR (HLG/PQ): conviértelo antes con herramientas/hdr_a_sdr.sh o saldrá lavado. (--forzar para seguir igual)")
    fps = a.fps or round(inf["fps"]) or 30
    dur = inf["duracion"]
    base = os.path.splitext(a.salida or a.video)[0].removesuffix(".cortado")
    salida = a.salida or f"{base}.cortado.mp4"

    # ── energía y umbral
    mono = leer_audio(a.video, 16000)
    db = energia_db(mono, 16000, PASO)
    umbral, piso = (a.umbral, float(np.percentile(db, 10))) if a.umbral is not None else umbral_silencio(db)
    sil = db < umbral
    voz = ~sil
    print(f"piso {piso:.1f} dBFS · silencio bajo {umbral:.1f} dBFS")

    bloques = rangos(a.solo) or [(0.0, dur)]
    bloques = restar(bloques, rangos(a.quitar))
    aire = a.pausa / 2
    tramos = []
    for k, (ba, bb) in enumerate(bloques):
        i0, i1 = int(ba / PASO), min(int(bb / PASO), len(voz))
        idx = np.nonzero(voz[i0:i1])[0]
        if len(idx) == 0:
            continue
        v0, v1 = (i0 + idx[0]) * PASO, (i0 + idx[-1] + 1) * PASO
        ini = v0 - (a.inicio if not tramos else aire)
        ultimo = k == len(bloques) - 1
        fin = v1 + (a.cola if ultimo else aire)
        t0 = ini
        for s0, s1 in silencios(sil, v0, v1, a.min):
            tramos.append([t0, s0 + aire])
            t0 = s1 - aire
        tramos.append([t0, fin])

    # cuadros enteros, sin solapes, dentro del video
    q = lambda t: round(t * fps) / fps
    limpio = []
    for ta, tb in tramos:
        ta, tb = q(max(0.0, ta)), q(min(dur, tb))
        if limpio and ta < limpio[-1][1]:
            ta = limpio[-1][1]
        if tb - ta >= 1 / fps:
            limpio.append([ta, tb])
    out, acc = [], 0.0
    for ta, tb in limpio:
        out.append({"a": round(ta, 4), "b": round(tb, 4), "r": round(acc, 4)})
        acc += tb - ta
    if not out:
        falla("no encontré voz: revisa --umbral")
    guardar_json({"fps": fps, "duracion": round(acc, 4), "bruto": os.path.abspath(a.video), "tramos": out}, f"{base}.cortes.json")
    print(f"{dur:.2f} s → {acc:.2f} s · {len(out)} tramos · {len(out) - len(bloques)} pausas recortadas")

    # ── audio original, por muestra, con fundidos de 10 ms
    est = leer_audio(a.video, SR, mono=False)
    fade = int(0.010 * SR)
    rampa = np.linspace(0, 1, fade)[:, None]
    trozos = []
    for t in out:
        n = int(round((t["b"] - t["a"]) * SR))
        s = est[int(round(t["a"] * SR)): int(round(t["a"] * SR)) + n].copy()
        if len(s) < n:
            s = np.vstack([s, np.zeros((n - len(s), 2), np.float32)])
        s[:fade] *= rampa
        s[-fade:] *= rampa[::-1]
        trozos.append(s)
    y = np.concatenate(trozos)
    wav = f"{base}.voz.wav"
    with wave.open(wav, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(y, -1, 1) * 32767).astype("<i2").tobytes())

    # ── palabras al tiempo del corte
    if a.palabras:
        pal = json.load(open(a.palabras, encoding="utf-8"))
        nuevas = []
        for p in pal:
            for t in out:
                if t["a"] <= p["t0"] < t["b"]:
                    nuevas.append({"w": p["w"], "t0": round(t["r"] + p["t0"] - t["a"], 3),
                                   "t1": round(t["r"] + min(p["t1"], t["b"]) - t["a"], 3), "bruto": p["t0"]})
                    break
        guardar_json(nuevas, f"{base}.palabras-corte.json")
        print(f"✓ {len(nuevas)} de {len(pal)} palabras pasadas al corte")

    if a.sin_video:
        print(f"✓ {wav}")
        return

    # ── video: por bloques de 8 tramos (con muchos decodificadores 4K a la vez se acaba la RAM)
    escala = f",scale={a.ancho}:-2" if a.ancho else ""
    with tempfile.TemporaryDirectory() as tmp:
        partes = []
        for b0 in range(0, len(out), 8):
            grupo = out[b0:b0 + 8]
            S = q(max(0.0, grupo[0]["a"] - 1.0))
            k = len(grupo)
            # primero fps fijo y DESPUÉS el recorte por número de cuadro: así cada tramo dura exacto,
            # también con grabaciones de pantalla de cuadros irregulares
            g = f"[0:v]fps={fps}{escala},split={k}" + "".join(f"[s{i}]" for i in range(k)) + ";"
            g += ";".join(f"[s{i}]trim=start_frame={round((t['a'] - S) * fps)}:end_frame={round((t['b'] - S) * fps)},"
                          f"setpts=PTS-STARTPTS[v{i}]" for i, t in enumerate(grupo))
            g += ";" + "".join(f"[v{i}]" for i in range(k)) + f"concat=n={k}:v=1:a=0,format=yuv420p[v]"
            p = os.path.join(tmp, f"p{b0:05d}.mp4")
            correr(["ffmpeg", "-v", "error", "-y", "-ss", f"{S:.4f}", "-i", a.video, "-filter_complex", g, "-map", "[v]",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "14", "-g", "15", "-color_primaries", "bt709",
                    "-color_trc", "bt709", "-colorspace", "bt709", p])
            partes.append(p)
            print(f"  video {min(b0 + 8, len(out))}/{len(out)}", end="\r")
        lista = os.path.join(tmp, "lista.txt")
        open(lista, "w").write("".join(f"file '{p}'\n" for p in partes))
        correr(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lista, "-i", wav, "-map", "0:v", "-map", "1:a",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", salida])
    cuadros = correr(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v", "-show_entries", "stream=nb_read_packets",
                      "-of", "csv=p=0", salida]).strip()
    print(f"\n✓ {salida}  ({cuadros} cuadros; esperados {round(acc * fps)})\n✓ {wav}\n✓ {base}.cortes.json")


if __name__ == "__main__":
    main()
