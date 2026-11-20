# Cerebro de motion · Aztec Lab

**Edita tus reels, anuncios y videos de YouTube con IA y el mismo estilo que usamos en [Aztec Lab](https://azteclab.co).**

Esto no es un programa con botones: es el «cerebro» que le das a tu agente de IA (Claude Code, Codex o Gemini CLI)
para que edite como nosotros. Trae tres cosas:

1. **`CEREBRO.md`** — nuestro estilo de edición escrito como reglas: qué funciona, qué se rechazó y por qué, recetas
   para cada tipo de video y las trampas técnicas que ya nos costaron horas.
2. **`herramientas/`** — scripts que miden el video en vez de adivinar: transcripción por palabra (Whisper local),
   cortes fluidos de 0,2 s, detección de la cabeza para no cortarla nunca, sincronía por audio, pantallas negras,
   mezcla de efectos debajo de la voz y verificación final.
3. **`plantillas/`** — un proyecto de reel listo (Remotion) con gancho desde el cuadro 0, pantalla partida con demo,
   tarjetas, cursor con clics y CTA, más un prompt para motion de producto (HyperFrames).

Todo corre **en tu computadora**: tus videos no se suben a ningún lado y no necesitas pagar APIs.

---

## Qué necesitas

- Una **Mac** (Apple Silicon recomendado, macOS 14 o más nuevo). En Windows/Linux funciona la parte de cortes,
  transcripción y render, pero no las herramientas de Vision (cabeza, OCR, recortes).
- **Claude Code** (o Codex / Gemini CLI). [Cómo instalar Claude Code](https://docs.anthropic.com/en/docs/claude-code).
- ~3 GB libres (el modelo de Whisper pesa 1,6 GB) y más espacio para tus renders.

## Instalación (10 minutos)

```bash
git clone https://github.com/juanes-create/cerebro-motion-aztec.git
cd cerebro-motion-aztec
./instalar.sh
```

`instalar.sh` revisa y te pregunta antes de instalar cada cosa: ffmpeg, Node, whisper-cpp (con Homebrew), numpy,
el modelo de Whisper large-v3-turbo, las herramientas de Vision y las skills de HyperFrames y Remotion para Claude Code.
Para solo revisar qué falta: `./instalar.sh --revisar`.

## Cómo se usa

1. Abre la carpeta en Claude Code:
   ```bash
   cd cerebro-motion-aztec
   claude
   ```
2. La primera vez te preguntará tu marca (cuenta, colores, palabra del CTA). Si quieres el look de Aztec, dilo.
3. Pon tu video en `videos/` (o pásale la ruta) y pídele algo como:
   - «Edítame este reel: `videos/mi-reel.mp4`. Cortes fluidos y motion de lo que digo.»
   - «Este bruto tiene tomas repetidas, déjame solo las buenas y córtalo súper fluido.»
   - «En el segundo 12 al 25 hablo de Gmail: muéstralo con la interfaz real en pantalla partida.»
   - «Hazlo igualito a este reel: <link>» (desglosa la referencia cuadro a cuadro).
   - «Tengo la grabación de pantalla de lo que hice mientras hablaba: sincronízala y úsala.»

   Más ejemplos en [`ejemplos/pedidos.md`](ejemplos/pedidos.md).
4. El agente mide, arma, te muestra cuadros de prueba, renderiza, verifica y te entrega un `… EDITADO.mp4` nuevo
   (nunca sobrescribe tu video).

## Qué esperar (y qué no)

- **Sí:** cortes de pausas exactos, motion sincronizado con tus palabras, demos con interfaces reales, tarjetas que no
  tapan tu cara, CTA, efectos sutiles, verificación de sincronía y volumen.
- **No:** subtítulos por defecto (la mayoría los pone en CapCut; si los quieres, pídelos), música, ni voces generadas.
- **Depende de ti:** el gusto. Cuando algo no te guste, díselo: el agente lo anota en `CLAUDE.md` y `MARCA.md` y lo
  recuerda en el siguiente video.

## Estructura

```
CLAUDE.md / AGENTS.md / GEMINI.md   instrucciones del agente (idénticas)
CEREBRO.md                          el estilo y las recetas
MARCA.md                            tu marca (colores, letra, cuenta, CTA)
instalar.sh                         instalador / revisión
herramientas/                       medir, cortar, sincronizar, mezclar, verificar
plantillas/reel-remotion/           proyecto base de reel 1080×1920
plantillas/motion-viaje/PROMPT.md   motion de producto o viaje con tus fotos (HyperFrames)
ejemplos/pedidos.md                 cómo pedirle cosas al agente
videos/  proyectos/  modelos/       tus archivos (no se suben a git)
```

## Créditos y licencia

Hecho por el equipo de [Aztec Lab](https://azteclab.co) · Instagram [@aztec.lab](https://instagram.com/aztec.lab) ·
YouTube [@azteclabco](https://youtube.com/@azteclabco).

Código y documentos con licencia MIT (ver `LICENSE`). Las fuentes se cargan de Google Fonts (licencia OFL). Este
repositorio no incluye videos, sonidos ni imágenes de terceros: los efectos salen de la librería que instala
HyperFrames o del paquete gratis de Adobe Audition, que descargas tú.
