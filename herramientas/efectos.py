#!/usr/bin/env python3
"""Mezcla efectos de sonido DEBAJO de la voz, sin tocar la voz, y deja un .m4a listo para unir con -c copy.

Reglas de audio (estilo Aztec):
  - La voz no se toca: va tal cual (nada de EQ, compresor ni loudnorm encima de ella).
  - `amix normalize=0` siempre: si no, ffmpeg baja la voz.
  - Efectos casi imperceptibles: whoosh a −35 dBFS solo en los barridos que cambian de color, clics a −21,
    golpes graves a −37. Nunca «tling», ping ni sonidos de aprobación.
  - Cada efecto se coloca por su PICO, no por el inicio del archivo («alinear": "pico").
  - Nunca metas el audio en el render de Remotion (corre la voz ~43 ms): render --muted y luego esto.

efectos.json:
  {"cues": [
     {"t": 4.85, "sonido": "whoosh-short", "pico": -35, "filtro": "highpass=f=220,lowpass=f=7500", "alinear": "pico"},
     {"t": 6.50, "sonido": "click-soft",   "pico": -21, "filtro": "highpass=f=500,lowpass=f=7000"},
     {"t": 9.00, "sonido": "efectos/mi-golpe.wav", "pico": -37}
  ]}
  "sonido" es una ruta, o el nombre de un efecto de la librería que trae HyperFrames
  (~/.claude/skills/media-use/audio/assets/sfx/: whoosh, whoosh-short, pop, click-soft, …).
  También acepta los clics de un cursor.json: --cursor src/cursor.json (usa click-soft a −21 dBFS).

Uso:
  herramientas/efectos.py --voz videos/reel.cortado.mp4 --cues efectos.json --salida out/mezcla.m4a
  ffmpeg -i out/reel-sin-audio.mp4 -i out/mezcla.m4a -map 0:v -map 1:a -c copy -movflags +faststart "Reel EDITADO.mp4"
"""
import argparse
import glob
import json
import os
import sys
import tempfile
import wave

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import correr, falla, info, leer_audio  # noqa: E402

SR = 48000
LIBRERIAS = [os.path.expanduser("~/.claude/skills/media-use/audio/assets/sfx"),
             os.path.expanduser("~/.agents/skills/media-use/audio/assets/sfx")]


def buscar(nombre, raiz):
    if os.path.isfile(nombre):
        return nombre
    if os.path.isfile(os.path.join(raiz, nombre)):
        return os.path.join(raiz, nombre)
    for lib in LIBRERIAS:
        m = glob.glob(os.path.join(lib, nombre + ".*")) or glob.glob(os.path.join(lib, nombre))
        if m:
            return m[0]
    falla(f"no encontré el sonido '{nombre}' (ni como ruta ni en la librería de HyperFrames: instala sus skills)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--voz", required=True, help="video o audio con la voz (va intacta)")
    ap.add_argument("--cues", help="efectos.json")
    ap.add_argument("--cursor", help="cursor.json: un clic suave en cada clic")
    ap.add_argument("--salida", required=True)
    ap.add_argument("--semilla", type=int, default=3)
    a = ap.parse_args()
    cues = []
    if a.cues:
        cues += json.load(open(a.cues, encoding="utf-8"))["cues"]
    if a.cursor:
        for t in json.load(open(a.cursor, encoding="utf-8")).get("clics", {}).values():
            cues.append({"t": t, "sonido": "click-soft", "pico": -21, "filtro": "highpass=f=500,lowpass=f=7000", "variar": 2.5})
    if not cues:
        falla("no hay efectos: pasa --cues o --cursor")
    raiz = os.path.dirname(os.path.abspath(a.cues or a.cursor))
    dur = info(a.voz)["duracion"]
    pista = np.zeros((int((dur + 2) * SR), 2), np.float64)
    rng = np.random.default_rng(a.semilla)
    cache = {}
    for c in sorted(cues, key=lambda c: c["t"]):
        clave = (c["sonido"], c.get("filtro", ""))
        if clave not in cache:
            ruta = buscar(c["sonido"], raiz)
            args = ["ffmpeg", "-v", "error", "-i", ruta]
            if c.get("filtro"):
                args += ["-af", c["filtro"]]
            args += ["-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
            s = np.frombuffer(correr(args, text=False), "<f4").reshape(-1, 2).astype(np.float64)
            cache[clave] = s
        s = cache[clave]
        pk = np.abs(s).max() + 1e-9
        pico = c.get("pico", -30) - (rng.uniform(0, c["variar"]) if c.get("variar") else 0)   # clics: cada uno un poco distinto
        g = 10 ** (pico / 20) / pk
        corr = int(np.argmax(np.abs(s).max(1))) if c.get("alinear") == "pico" else 0
        i = int(c["t"] * SR) - corr
        j0 = max(0, -i)
        i = max(0, i)
        seg = s[j0:j0 + len(pista) - i] * g
        pista[i:i + len(seg)] += seg
    with tempfile.TemporaryDirectory() as tmp:
        wav = os.path.join(tmp, "fx.wav")
        with wave.open(wav, "wb") as w:
            w.setnchannels(2)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((np.clip(pista, -1, 1) * 32767).astype("<i2").tobytes())
        g = ("[0:a]aformat=sample_rates=48000:channel_layouts=stereo[voz];"
             "[1:a]aformat=sample_rates=48000:channel_layouts=stereo[fx];"
             "[voz][fx]amix=inputs=2:normalize=0:duration=first[out]")
        os.makedirs(os.path.dirname(os.path.abspath(a.salida)), exist_ok=True)
        correr(["ffmpeg", "-v", "error", "-y", "-i", a.voz, "-i", wav, "-filter_complex", g, "-map", "[out]",
                "-c:a", "aac", "-b:a", "256k", a.salida])
    print(f"✓ {len(cues)} efectos → {a.salida}")


if __name__ == "__main__":
    main()
