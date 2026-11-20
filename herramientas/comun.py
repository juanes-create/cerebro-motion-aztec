"""Funciones que comparten todas las herramientas: leer audio, medir energía, encontrar Whisper y los binarios de Vision."""
import glob
import json
import os
import shutil
import subprocess
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
BIN = os.path.join(AQUI, "bin")


def falla(msg, codigo=1):
    print(f"✗ {msg}", file=sys.stderr)
    sys.exit(codigo)


def correr(args, **kw):
    """Corre un comando y devuelve su salida; si falla, muestra el error de forma legible."""
    r = subprocess.run(args, capture_output=True, text=kw.pop("text", True), **kw)
    if r.returncode != 0:
        err = r.stderr if isinstance(r.stderr, str) else r.stderr.decode("utf-8", "replace")
        falla(f"falló {os.path.basename(args[0])}: {err.strip()[-600:]}")
    return r.stdout


def info(video):
    """Duración, fps, ancho, alto y cuadros del primer stream de video (y si tiene audio)."""
    out = correr(["ffprobe", "-v", "error", "-show_entries",
                  "stream=codec_type,width,height,r_frame_rate,nb_frames,duration,color_transfer:format=duration",
                  "-of", "json", video])
    j = json.loads(out)
    v = next((s for s in j["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in j["streams"] if s["codec_type"] == "audio"), None)
    dur = float(j["format"].get("duration", 0) or 0)
    res = {"duracion": dur, "audio": a is not None}
    if v:
        n, d = v["r_frame_rate"].split("/")
        res.update(ancho=v.get("width"), alto=v.get("height"), fps=round(float(n) / float(d), 3),
                   cuadros=int(v["nb_frames"]) if v.get("nb_frames", "").isdigit() else None,
                   transferencia=v.get("color_transfer", ""))
    return res


def leer_audio(ruta, sr=16000, mono=True, desde=None, hasta=None):
    """Audio como float32 en [-1, 1]. Mono (n,) o estéreo (n, 2)."""
    args = ["ffmpeg", "-v", "error"]
    if desde is not None:
        args += ["-ss", f"{desde:.3f}"]
    if hasta is not None:
        args += ["-to" if desde is None else "-t", f"{(hasta - (desde or 0)):.3f}"]
    args += ["-i", ruta, "-vn", "-ac", "1" if mono else "2", "-ar", str(sr), "-f", "f32le", "-"]
    raw = correr(args, text=False)
    x = np.frombuffer(raw, dtype="<f4").astype(np.float32)
    return x if mono else x.reshape(-1, 2)


def energia_db(x, sr, paso=0.01, ventana=0.025):
    """Energía en dBFS cada `paso` segundos (por defecto cada 10 ms)."""
    hop, win = int(sr * paso), int(sr * ventana)
    n = max(0, (len(x) - win) // hop + 1)
    if n == 0:
        return np.array([-120.0])
    idx = np.arange(win)[None, :] + hop * np.arange(n)[:, None]
    rms = np.sqrt((x[idx] ** 2).mean(1) + 1e-12)
    return 20 * np.log10(rms + 1e-9)


def umbral_silencio(db, piso_extra=8.0, techo=-40.0):
    """Silencio = por debajo de max(techo, piso + piso_extra). El piso es el percentil 10 de la energía."""
    piso = float(np.percentile(db, 10))
    return max(techo, piso + piso_extra), piso


def modelo_whisper():
    """Busca el modelo GGML de Whisper: $WHISPER_MODEL, la carpeta del repo o las rutas habituales."""
    cand = [os.environ.get("WHISPER_MODEL", "")]
    cand += glob.glob(os.path.join(RAIZ, "modelos", "ggml-*.bin"))
    cand += glob.glob(os.path.expanduser("~/.cache/whisper/ggml-*.bin"))
    cand += glob.glob(os.path.expanduser("~/Library/Application Support/*/models/ggml-*.bin"))
    # los modelos «.en» solo entienden inglés: no sirven para videos en español
    cand = [c for c in cand if c and os.path.isfile(c) and os.path.getsize(c) > 50_000_000 and not c.endswith(".en.bin")]
    if not cand:
        falla("no encontré el modelo de Whisper. Corre ./instalar.sh o define WHISPER_MODEL=/ruta/ggml-large-v3-turbo.bin")
    turbo = [c for c in cand if "large-v3-turbo" in c]
    return (turbo or cand)[0]


def whisper_cli():
    exe = shutil.which("whisper-cli") or shutil.which("whisper-cpp")
    if not exe:
        falla("falta whisper-cli (brew install whisper-cpp)")
    return exe


def binario(nombre):
    """Binarios de Vision compilados por herramientas/swift/compilar.sh."""
    p = os.path.join(BIN, nombre)
    if not os.path.isfile(p):
        falla(f"falta el binario '{nombre}'. Compílalo con: herramientas/swift/compilar.sh (solo Mac)")
    return p


def guardar_json(obj, ruta):
    os.makedirs(os.path.dirname(os.path.abspath(ruta)), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)


def rangos(txt):
    """'12.5-18,40-52.3' → [(12.5, 18.0), (40.0, 52.3)]"""
    if not txt:
        return []
    res = []
    for parte in txt.replace(" ", "").split(","):
        if parte:
            a, b = parte.split("-")
            res.append((float(a), float(b)))
    return res
