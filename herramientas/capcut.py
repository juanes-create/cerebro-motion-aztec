#!/usr/bin/env python3
"""Lee un proyecto de CapCut (draft_info.json, es JSON legible) y lo resume: qué tramos del bruto usó, a qué
velocidad, qué sonidos con qué volumen y en qué segundo, y qué textos o stickers puso.

Para qué:
  - «Ponle mis efectos» / «como yo lo edité»: la receta exacta (archivo, volumen, segundo) está aquí. No se adivina.
  - Editar ENCIMA de una base que ya cortaste en CapCut: con --palabras, las palabras del bruto pasan a la línea
    de tiempo de la base sin transcribirla (y sin las voces de los memes o la música).
  - No tapar lo que ya pusiste: los textos y stickers salen con su tiempo.

Dónde está el proyecto (Mac):
  ~/Movies/CapCut/User Data/Projects/com.lveditor.draft/<proyecto>/draft_info.json
  (o …/<proyecto>/Timelines/*/draft_info.json). CapCut nombra los sonidos de su caché con el MD5 del archivo.

Uso:
  herramientas/capcut.py "<proyecto>"                      # resumen
  herramientas/capcut.py "<proyecto>" --json resumen.json
  herramientas/capcut.py "<proyecto>" --palabras videos/bruto.palabras.json --clip IMG_1234 --salida base.palabras.json
"""
import argparse
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import falla, guardar_json  # noqa: E402

PROYECTOS = os.path.expanduser("~/Movies/CapCut/User Data/Projects/com.lveditor.draft")


def encontrar(p):
    if os.path.isfile(p):
        return p
    for c in [os.path.join(p, "draft_info.json"), os.path.join(PROYECTOS, p, "draft_info.json")] + \
             sorted(glob.glob(os.path.join(PROYECTOS, p, "Timelines", "*", "draft_info.json"))):
        if os.path.isfile(c):
            return c
    falla(f"no encontré draft_info.json para '{p}'. Proyectos: {', '.join(sorted(os.listdir(PROYECTOS))[:20]) if os.path.isdir(PROYECTOS) else '(no hay carpeta de CapCut)'}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("proyecto")
    ap.add_argument("--json")
    ap.add_argument("--palabras")
    ap.add_argument("--clip", help="nombre (o parte) del archivo del bruto en el proyecto")
    ap.add_argument("--salida")
    a = ap.parse_args()
    dj = json.load(open(encontrar(a.proyecto), encoding="utf-8"))
    mats = {}
    for k, v in dj.get("materials", {}).items():
        if isinstance(v, list):
            for m in v:
                if isinstance(m, dict) and "id" in m:
                    mats[m["id"]] = (k, m)
    vel = {m["id"]: m.get("speed", 1.0) for m in dj.get("materials", {}).get("speeds", [])}
    us = 1e6
    res = {"video": [], "audio": [], "texto": [], "sticker": [], "otros": []}
    for tr in dj.get("tracks", []):
        for s in tr.get("segments", []):
            k, m = mats.get(s.get("material_id"), ("?", {}))
            tt = s.get("target_timerange") or {}
            st = s.get("source_timerange") or {}
            sp = next((vel[r] for r in s.get("extra_material_refs", []) if r in vel), 1.0)
            fila = {"pista": tr.get("type"), "en": round(tt.get("start", 0) / us, 3), "dura": round(tt.get("duration", 0) / us, 3)}
            if tr.get("type") == "video":
                fila.update(archivo=os.path.basename(m.get("path", "")), desde=round(st.get("start", 0) / us, 3),
                            velocidad=sp, volumen=s.get("volume", 1.0))
                res["video"].append(fila)
            elif tr.get("type") == "audio":
                fila.update(archivo=os.path.basename(m.get("path", "")), nombre=m.get("name", ""), volumen=round(s.get("volume", 1.0), 3),
                            desde=round(st.get("start", 0) / us, 3))
                res["audio"].append(fila)
            elif tr.get("type") == "text":
                txt = m.get("content", "")
                try:
                    txt = json.loads(txt).get("text", txt)
                except Exception:
                    pass
                fila.update(texto=txt)
                res["texto"].append(fila)
            elif tr.get("type") == "sticker":
                c = s.get("clip") or {}
                fila.update(nombre=m.get("name", ""), escala=(c.get("scale") or {}).get("x"), pos=c.get("transform"))
                res["sticker"].append(fila)
            else:
                fila.update(tipo=k, nombre=m.get("name", "") or m.get("effect_name", ""))
                res["otros"].append(fila)

    print(f"VIDEO ({len(res['video'])} tramos)")
    for f in res["video"][:80]:
        print(f"  {f['en']:8.2f} s +{f['dura']:6.2f}  ← {f['archivo']} desde {f['desde']:.2f} s  ×{f['velocidad']}")
    print(f"\nSONIDOS ({len(res['audio'])})  — volumen de CapCut = ganancia lineal sobre el archivo")
    for f in res["audio"]:
        print(f"  {f['en']:8.2f} s  vol {f['volumen']:.2f}  {f['nombre'] or f['archivo']}")
    print(f"\nTEXTOS ({len(res['texto'])})")
    for f in res["texto"]:
        print(f"  {f['en']:8.2f}–{f['en'] + f['dura']:.2f} s  {str(f['texto'])[:70]}")
    if res["sticker"]:
        print(f"\nSTICKERS ({len(res['sticker'])})")
        for f in res["sticker"]:
            print(f"  {f['en']:8.2f}–{f['en'] + f['dura']:.2f} s  {f['nombre']}")
    if a.json:
        guardar_json(res, a.json)
        print(f"\n✓ {a.json}")

    if a.palabras:
        if not a.clip:
            falla("con --palabras hace falta --clip (el nombre del bruto en el proyecto)")
        pal = json.load(open(a.palabras, encoding="utf-8"))
        tramos = [f for f in res["video"] if a.clip in f["archivo"]]
        nuevas = []
        for p in pal:
            for f in tramos:
                fin_src = f["desde"] + f["dura"] * f["velocidad"]
                if f["desde"] <= p["t0"] < fin_src:
                    t0 = f["en"] + (p["t0"] - f["desde"]) / f["velocidad"]
                    t1 = f["en"] + (min(p["t1"], fin_src) - f["desde"]) / f["velocidad"]
                    nuevas.append({"w": p["w"], "t0": round(t0, 3), "t1": round(t1, 3)})
                    break
        nuevas.sort(key=lambda w: w["t0"])
        guardar_json(nuevas, a.salida or "base.palabras.json")
        print(f"✓ {len(nuevas)} de {len(pal)} palabras pasadas a la base → {a.salida or 'base.palabras.json'}")


if __name__ == "__main__":
    main()
