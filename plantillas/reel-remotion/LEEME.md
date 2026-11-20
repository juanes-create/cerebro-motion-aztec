# Plantilla: reel 1080×1920 con motion (Remotion)

```bash
cp -R plantillas/reel-remotion proyectos/mi-reel
cd proyectos/mi-reel
npm install                      # ~1 min, ~300 MB
./preparar.sh ../../videos/mi-reel.mp4
npm run dev                      # estudio de Remotion para ver y ajustar
./still.sh 0 1.5 6.4 12          # cuadros sueltos + mosaico con las zonas de peligro (ref/mosaico.jpg)
nohup ./render.sh > out/render.log 2>&1 &
./montar.sh "out/Mi reel EDITADO.mp4"
```

| Archivo | Qué es |
|---|---|
| `src/marca.ts` | Colores, letra, cuenta y palabra del CTA (sale de `MARCA.md`) |
| `src/kit.tsx` | `useT` (segundos), `Tramo`, `Pop`, `Typed`, `Pill`, `Caja`, `Check`, `golpe` |
| `src/ui.tsx` | Zonas de peligro, franjas libres (pared/piernas), pantalla partida con ola, cursor |
| `src/escenas.tsx` | Escenas de ejemplo: gancho desde el cuadro 0, demo en el panel, lista sobre las piernas, CTA |
| `src/datos/config.json` | fps, cuadros y si hay video (lo escribe `preparar.sh`) |
| `src/datos/partida.json` | Tramos con pantalla partida y cuánto baja el video (de `herramientas/cabeza.py`) |
| `src/datos/cursor.json` | Recorrido y clics del cursor: lo dibuja `ui.tsx` y lo suena `montar.sh` |
| `efectos.json` | Efectos de sonido con su segundo y nivel |

Sin video (`"video": false`) se ve un fondo de prueba, para ensayar el motion antes de tener la grabación.
Las escenas de ejemplo usan tiempos fijos (0-15 s): cámbialos por los segundos de TUS palabras (`src/datos/*.palabras.json`).
