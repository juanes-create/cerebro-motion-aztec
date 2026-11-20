# Herramientas

Todas se corren desde la raíz del repositorio y traen su ayuda con `--help`. Escriben sus resultados junto al video
(`<nombre>.palabras.json`, `<nombre>.cortes.json`…). Las de Vision necesitan `herramientas/swift/compilar.sh` (Mac).

| Herramienta | Para qué | Ejemplo |
|---|---|---|
| `hoja.sh` | Hoja de contacto: ver encuadre, cortes y lo que ya viene quemado | `herramientas/hoja.sh videos/bruto.mp4 3` |
| `hdr_a_sdr.sh` | Convertir brutos HDR de iPhone (si no, salen lavados) | `herramientas/hdr_a_sdr.sh videos/IMG_1234.MOV` |
| `transcribir.py` | Transcripción con tiempos POR PALABRA (Whisper local) | `herramientas/transcribir.py videos/reel.mp4` |
| `islas.py` | Cada isla de voz con su texto: para ver las tomas repetidas | `herramientas/islas.py videos/bruto.mp4` |
| `hablante.py` | Quién habla en cada isla (presentador, fuera de cámara, izquierda/derecha) | `herramientas/hablante.py videos/bruto.mp4` |
| `cortar.py` | Cortes fluidos: pausas > 0,3 s → 0,2 s, y quitar tramos | `herramientas/cortar.py videos/bruto.mp4 --quitar "0-3.4"` |
| `cabeza.py` | Tope de la cabeza y barbilla por cuadro; cuánto bajar el video en la pantalla partida | `herramientas/cabeza.py videos/reel.mp4 --panel 990 --tramos "4-12"` |
| `sincro.py` | Desfase entre dos grabaciones por su audio (cámara ↔ pantalla) | `herramientas/sincro.py cam.mp4 pantalla.mov --fino` |
| `negros.py` | Pantallas negras de un video largo + caja de la burbuja de cámara | `herramientas/negros.py videos/clase.mp4 --burbuja` |
| `capcut.py` | Resumen de un proyecto de CapCut: tramos, sonidos con volumen, textos | `herramientas/capcut.py "Mi proyecto"` |
| `efectos.py` | Efectos debajo de la voz (intacta) → `.m4a` para unir con `-c copy` | `herramientas/efectos.py --voz v.mp4 --cues efectos.json --salida m.m4a` |
| `limpiar_voz.py` | Voz opaca y baja → clara a −14 LUFS (solo si la piden) | `herramientas/limpiar_voz.py v.mp4 voz.wav` |
| `verificar.py` | Streams, sincronía, PSNR, volumen, texto final, zonas, QR | `herramientas/verificar.py streams "Reel EDITADO.mp4"` |

Binarios de Vision (`herramientas/bin/`, se compilan de `herramientas/swift/`):

| Binario | Qué hace |
|---|---|
| `caras` | Caja de cada cara en una carpeta de PNG (lo usa `cabeza.py`) |
| `bocas` | Apertura de la boca por cara (lo usa `hablante.py`) |
| `ocr` | Texto con su caja: censurar datos, ubicar botones en una grabación de pantalla |
| `quitar_fondo` | PNG transparente de una persona u objeto (`--recortar` lo ajusta al borde) |
| `qr` | Desde qué segundo se puede escanear un QR (lo usa `verificar.py qr`) |

El modelo de Whisper se busca en: `$WHISPER_MODEL`, `modelos/`, `~/.cache/whisper/` o `~/Library/Application Support/*/models/`.
