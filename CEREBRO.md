# Cerebro de motion · estilo Aztec Lab

> Todo lo que aprendimos editando reels, anuncios y videos de YouTube con IA (sep-nov 2026): el gusto que funciona,
> el flujo de trabajo, las recetas técnicas y las trampas que ya nos costaron horas.
>
> **Para el agente que lee esto:**
> 1. Léelo completo antes de tocar un video.
> 2. Las reglas de la sección 1 no se discuten: cada una salió de un rechazo real o de un «me encantó».
> 3. Antes de escribir código, mira `herramientas/` y `plantillas/`: casi todo lo que necesitas ya existe.
> 4. Los colores, la letra, la cuenta y la palabra del CTA salen de `MARCA.md`, no de este archivo.

---

## 0. Cómo pensar este trabajo

- **El video manda.** Todo el motion se sincroniza con lo que dice el presentador, palabra por palabra. No se anima «encima»: se anima *lo que se está diciendo*.
- **Medir, no adivinar.** Los tiempos salen de Whisper, la cabeza sale de Vision, las pantallas negras salen de la luminancia, los volúmenes salen de `ebur128`. Un agente que «calcula a ojo» corta cabezas y desfasa sonidos.
- **El editor humano habla rápido** y muchas veces por voz: sus mensajes llegan transcritos con errores. Interpreta la intención («Móvelos de IA» era «Modelos de IA»). Si algo es ambiguo y caro, pregunta (sección 1, regla 30).
- **Barato primero, caro después.** Corrige en cuadros sueltos (`still.sh`, segundos), no en renders completos (minutos).

---

## 1. Reglas de estilo (las duras)

### Lo visual

1. **Visuales, no texto.** Texto mínimo, y todo sincronizado con la palabra que lo dispara. Un motion «solo texto» se rechaza.
2. **Interfaces y productos REALES.** Si se habla de Gmail, Calendar, Claude, ChatGPT o cualquier app, se recrea la interfaz real *de hoy* (textos, orden, grises, radios, letra) y se usan imágenes y logos oficiales. Nada genérico (sección 6).
3. **Editorial y tecnológico, nunca caricatura.** Los logos con cara (ojos, lágrimas, gafas de sol) se ven «infantiles y feos».
4. **Simétrico respecto al centro** (x = 540 ± algo en un reel). Los gráficos no se corren a un lado para esquivar la cara: van en las franjas libres (pared y piernas).
5. **Sin bordes ni texto con trazo.** Nada de `WebkitTextStroke` ni barras con contorno: degradado + sombra suave. La versión con contornos fue «horrible».
6. **Gráficos de calificación** (barras, puntajes): se mueven UNA sola vez, en la palabra del veredicto, y quedan quietos hasta el siguiente ítem.
7. **Solo se titula lo que el presentador anuncia.** Si no dice «caso de uso #1», el #1 no lleva título.
8. **Si el presentador se equivoca al hablar,** en pantalla va lo que quiso decir.
9. **Nunca inventar cifras.** Si dice «3 a 4 veces» y lo medido es 2,1×, en pantalla va lo medido, o nada. Sin fuente, los benchmarks van sin números.
10. **Las noticias se verifican en la fuente primaria** (keynote, página oficial, documento), no solo en prensa. Nada de referencias viejas aunque el presentador las mencione.
11. **Una noticia simulada con una marca real** va siempre con la etiqueta «SIMULACIÓN HECHA CON IA» y el contexto verificado ese mismo día.
12. **Los nombres de personas en pantalla se confirman** con el editor antes de renderizar (un apellido de oído es un error público).
13. **La tarjeta «versus» marca con ✗ al que pierde.** Para «hoy puede X / después podrá Y» no sirve (hace ver lo de hoy como malo): ahí va una lista de tareas.

### Reels (Instagram / TikTok, 1080×1920)

14. **Zonas de peligro siempre vacías:** los 270 px de arriba (interfaz de Instagram), la descripción abajo (y > ~1480) y la columna de botones a la derecha (x > ~960).
15. **NUNCA cortarle la cabeza al presentador.** La gorra o el pelo queda ≥ 30 px lejos de cualquier panel o tarjeta, en TODOS los cuadros. Se mide con `herramientas/cabeza.py`, no a ojo. Cuando alguien se estira, la cabeza sube ~60 px.
16. **Pantalla partida solo para demos** (apps, selectores, ejemplos). El resto del tiempo el presentador va completo y las tarjetas van en las franjas libres: la pared sobre la cabeza y las piernas.
17. **El gancho se anima desde el cuadro 0,** con el panel o el título ya puestos (el cuadro 0 es la portada). Si el editor ya quemó su propio gancho en el bruto, no se toca.
18. **Sin subtítulos ni efectos de sonido por defecto.** El editor pone sus subtítulos en su programa. Si el reel lleva etiquetas cortas (2-3 palabras en mayúscula), van SOLO en las animaciones a pantalla completa; en la pantalla partida, ahí van los subtítulos del editor.
19. **CTA final:** tarjeta con «1 Síguenos @cuenta [Seguir → Siguiendo]» (el cursor hace clic) y «2 Comenta **PALABRA**» (se escribe sola). Está en la plantilla.
20. **Respetar lo que ya viene quemado** en la base (gancho, fechas, «100% gratis»): mide cuándo entra y sale cada cosa y no pongas nada encima.

### Cortes y voz

21. **Cortes «súper fluidos» = 0,2 s.** Toda pausa de más de 0,3 s queda en 0,2 s (0,1 + 0,1), con fundidos de 10 ms en el audio. Las pausas más cortas no se tocan. Se quitan las tomas repetidas, los arranques fallidos, la charla fuera de cámara y lo que el presentador le dicta a la IA (sección 4). Se aplica sin preguntar.
22. **El audio va ORIGINAL.** Nada de «arreglar» la voz (EQ, aislamiento, loudnorm) si no lo piden. Si lo piden, se entregan las dos versiones.
23. **Las grabaciones de voz no se recortan por frases** para cumplir una duración. Se quitan silencios y ruidos, nunca frases sin preguntar.
24. **Instrucciones dichas a la IA dentro del bruto** («ponle esto en blanco y negro») se ejecutan y se cortan del video.

### Sonido

25. **Casi imperceptible, elegante y moderno.** Nunca «tling», ping, sparkle ni sonidos de aprobación.
26. **Barridos:** `whoosh-short` filtrado a −35 dBFS, solo en los barridos que cambian de color. Un aire sintetizado con ruido suena barato.
27. **Clics suaves** solo cuando un cursor hace clic (−21 dBFS). Contador sonoro solo en barras de puntaje.

### Forma de trabajar

28. **Cuando el editor dice «ya sabes qué hacer, hazlo»: hazlo.** No lo llenes de preguntas.
29. **«Réplica exacta» de un reel de referencia** = el mismo gancho, la misma estructura, las mismas animaciones y el mismo comportamiento del personaje (de frente o de espaldas, cuántos clics). Solo se cambia lo que no es cierto para tu marca, por algo real.
30. **Ante algo ambiguo y caro** (tono nuevo, audio, layout): preguntas PUNTUALES, con opciones concretas y el segundo exacto de cada escena. Para un tono nuevo, muestra 2-3 cuadros antes del render completo.
31. **Entregas:** el video COMPLETO montado en MP4, con nombre NUEVO (`… EDITADO.mp4`, `… v2.mp4`). Nunca sobrescribas la base ni una entrega anterior. Si piden borrar versiones viejas: a la Papelera, solo las tuyas, nunca las bases.
32. **Comparaciones en tarjetas,** no en tablas anchas: una tarjeta por opción con una frase de resultado; la tabla es el anexo.
33. **Varias bases con la misma duración ya vienen sincronizadas:** se usan tal cual en su segundo, cada una en su capa.
34. **Si existe la grabación de pantalla real, se usa** (sincronizada por audio, sección 5.F). Si no existe, se recrea la app con piezas reales y se avisa qué es recreado.

---

## 2. Flujo de trabajo (del pedido a la entrega)

1. **Encontrar el material** y hacer `ffprobe` (resolución, fps, duración, cuadros, `color_transfer`). Si es HDR (`arib-std-b67` o `smpte2084`): `herramientas/hdr_a_sdr.sh` ANTES de todo, o sale lavado.
2. **Hoja de contacto** de todo el bruto: `herramientas/hoja.sh VIDEO 3` (un cuadro cada 3 s). Ahí se ven el encuadre, los cortes y lo que ya viene quemado.
3. **Cortar** si es un bruto crudo: `islas.py` para ver las tomas y `cortar.py` con la regla de 0,2 s (sección 4).
4. **Transcribir** el video que se va a animar: `herramientas/transcribir.py VIDEO` → `palabras.json` + `frases.txt`.
5. **Medir:** la cabeza (`cabeza.py`), las pantallas negras (`negros.py`), lo que ya viene quemado (hojas de 10 cuadros/s alrededor), la sincronía con otras grabaciones (`sincro.py`).
6. **Investigar lo real:** abrir las apps en el navegador, leer sus estilos, bajar logos e imágenes oficiales, verificar nombres, fechas y cifras.
7. **Plan de escenas con su segundo exacto:** qué palabra dispara cada cosa, dónde va (pared, piernas o panel) y cuándo se parte la pantalla. Escríbelo antes de construir.
8. **Construir** copiando la plantilla: `cp -R plantillas/reel-remotion proyectos/<nombre>` → `npm install` → `./preparar.sh VIDEO`.
9. **Cuadros de prueba** con `./still.sh 0 1.5 6.4 …` (mosaico con las líneas de las zonas). Corregir aquí.
10. **Render completo** en segundo plano (`nohup ./render.sh > out/render.log 2>&1 &`).
11. **Audio aparte** y unión con `-c copy` (`./montar.sh "Nombre EDITADO.mp4"`).
12. **Verificar** (sección 9). Nunca entregues sin medir.
13. **Entregar:** nombre nuevo, mostrarlo en el Finder (`open -R`), y un mensaje corto con qué tiene por tramos, qué respetaste y cómo lo verificaste.
14. **Aprender:** si algo fue nuevo, súmalo a «Aprendizajes» en `CLAUDE.md`, `AGENTS.md` y `GEMINI.md` (idénticos).

---

## 3. Medir el bruto

### 3.1 Transcripción con tiempos por palabra (Whisper local)

`herramientas/transcribir.py VIDEO [--desde a --hasta b]`
- Parte el audio en ventanas de ~9 s, cada corte en el valle de energía, y corre `whisper-cli -ml 1 -sow` en cada una: tiempos limpios por palabra.
- Con GPU (Metal) va a ~10× tiempo real (40 s de audio en ~9 s). Dentro de un sandbox la GPU falla y la herramienta reintenta con `-ng` (unas 20 veces más lento).
- **Trampas de Whisper:** `--prompt` corre los tiempos; sobre audios largos de corrido redondea al segundo y fusiona frases repetidas; `-dtw` con `-ng` devuelve todo en 0; en videos ya editados puede correr las palabras ~0,3 s (ajusta los bordes con la energía).
- **Errores de oído:** «Cloud» = Claude, «plan E» = planear. Se corrigen en el plan, no en pantalla.

### 3.2 Cómo dicta tiempos un editor de CapCut

- **«6 con 4» = 6 s + 4 cuadros.** Busca el corte de escena más cercano y termina el gráfico justo ahí.
- **«del 0-1 al 1-18» = de 0:01 a 1:18.** «Los tramos en negro» son exactamente las pantallas negras: mídelas, no preguntes.

### 3.3 Cabeza del presentador (Vision, gratis y local)

`herramientas/cabeza.py VIDEO --panel 990 --tramos "4.8-18.7,…" --margen 30`
- Detecta la cara a 5 cuadros/s; **tope de la cabeza ≈ y de la cara − 0,45 × alto** (conservador, también con gorra). Ojo: la caja de Vision subestima una gorra alta: si hay gorra, confírmalo en un cuadro real.
- Imprime por ventanas de 10 s el tope más alto y la barbilla más baja, y cuánto BAJAR el video en cada tramo de pantalla partida.
- **Tarjetas sobre el cuerpo:** mide también la barbilla. En planos donde la cara queda baja (alguien en un sofá), una tarjeta a media altura le tapa la boca: bájala bajo el p90 de la barbilla.

### 3.4 Pantallas negras y burbuja de cámara (videos largos)

`herramientas/negros.py VIDEO --burbuja`
- Decodifica SOLO los keyframes (2 h 35 min en ~2,5 min) y luego afina cada borde cuadro a cuadro.
- **La burbuja de cámara no es fija** dentro de un tramo (salta y hace zooms lentos): se guarda su caja en CADA cuadro, y el motion lleva un HUECO exacto + un aro de acento que la sigue. Si la burbuja se anima (crece o se encoge), el hueco se abre cuando ya está quieta.

### 3.5 Lo que ya viene quemado

Hojas de 10 cuadros/s alrededor del texto quemado para saber su cuadro exacto de entrada y salida:
```bash
ffmpeg -ss 172.6 -i BASE.mp4 -t 1.6 -vf "fps=10,crop=1080:700:0:200,scale=216:140,tile=4x4" -frames:v 1 g.jpg
```
Si el texto tiene un color conocido, también se detecta midiendo ese color por franjas.

### 3.6 Cuando la base se vuelve a exportar

1. Compara las dos bases (a 2 cuadros/s y en los bordes de cada tramo) antes de rehacer nada.
2. Si todo quedó corrido un número exacto de cuadros, se reutiliza el motion con un desfase (`<Sequence from={DESFASE}>`).
3. Si solo cambió algo fuera de los tramos, los overlays sirven tal cual: re-monta con el audio de la base nueva (puede venir ~48 ms corrido: usa siempre el nuevo).

---

## 4. Cortes fluidos y tomas repetidas

**Herramientas:** `islas.py` (ver las tomas) → `cortar.py` (cortar) → `verificar.py texto` (leer el resultado).

1. **Islas de voz:** `islas.py BRUTO` parte el bruto por silencios y transcribe cada isla SOLA. Sobre el bruto entero, Whisper fusiona las tomas repetidas y la fallida desaparece del texto; isla por isla, cada repetición sale con su segundo.
2. **Decidir qué sale:** tomas repetidas (queda la última buena), arranques fallidos, charla fuera de cámara (`hablante.py`: el presentador está ~15-25 dB más fuerte y con la boca en movimiento), instrucciones a la IA.
3. **Cortar:** `cortar.py BRUTO --quitar "0-3.4,41.2-47.9" --palabras BRUTO.palabras.json`
   - toda pausa > 0,3 s queda en 0,2 s; arranque 0,08 s antes de la primera palabra; final 0,5 s después de la última (hasta ~0,9 s si hay un remate visual);
   - silencio = energía bajo max(−40 dBFS, piso + 8 dB);
   - video y audio salen de la MISMA lista (video por cuadro, audio por muestra con fundido de 10 ms): la sincronía es exacta por construcción;
   - el video se arma por bloques de 8 tramos (con decenas de decodificadores 4K a la vez se acaba la RAM).
4. **Una toma repetida dentro de la misma frase** («vamos a dar una clase… y por eso vamos a dar una clase en donde…»): se corta por palabra, con los tiempos de `palabras.json`.
5. **Si una frase sigue sin pausa,** es mejor conservarla completa que cortarla en medio del impulso.
6. **El motion sigue en segundos del BRUTO** si te conviene: `cortes.json` trae cada tramo (`a`, `b` en el bruto y `r` en el corte) para pasar tiempos de uno a otro sin re-temporizar nada.
7. **Subtítulos después de cortar:** transcribe de nuevo el video YA cortado (la alineación sobre el bruto se corre hasta 1 s en frases largas).
8. **Verificar:** `verificar.py texto FINAL` y leerlo de corrido. Una palabra corta que «dura» más de ~0,9 s esconde una corrección («este simple… este proceso simple»). Whisper alucina en pedazos de menos de 1 s: revisa la toma entera, no el pedacito.

---

## 5. Recetas por tipo de pieza

### 5.A Reel con presentador y motion (Instagram 1080×1920)

**Plantilla:** `plantillas/reel-remotion` (Remotion 4).

**Layout:**
- **Pared** (sobre la cabeza): de y ≈ 300 hasta el tope de la cabeza − 30. Ahí van títulos cortos, escaleras, mapas, píldoras.
- **Piernas:** y ≈ 1080-1470, x 120-960 (840 de ancho, simétrico y fuera de los botones). Ahí van las tarjetas.
- **Pantalla partida:** panel crema con cuadrícula de 0 a 990 px y borde inferior de ola (línea de acento de 10 px que ondula). El video baja lo justo para que la cabeza quede ≥ 30 px bajo la ola (lo dice `cabeza.py`). Panel y video se mueven con la MISMA curva (`Easing.inOut(cubic)`, 0,5 s): `ui.tsx → partida(t)` y `bajada(t)`, con los tramos en `src/datos/partida.json`.

**Todo el motion en segundos** (`useT() = frame / fps`), copiados de `palabras.json`. Componentes base (`kit.tsx`):
- `Tramo a b` — entra con pop y sale rápido; fuera del tramo no se dibuja.
- `Pop at` — aparece en la palabra.
- `Typed` — texto que se escribe; lo no escrito va `transparent`, así la línea no salta.
- `Pill`, `Caja`, `Check`, `golpe` (botón que recibe un clic).

**Cursor:** `src/datos/cursor.json` es la fuente ÚNICA de verdad (`visible`, `puntos [t, x, y]`, `clics`). Lo dibuja `ui.tsx → Cursor` y lo suena `efectos.py --cursor`: sonido y dibujo nunca se desfasan. Dos puntos con la misma posición = el cursor se queda quieto.

**Render del cuadro completo** (el video se mueve en las transiciones): proxy en `public/video/bruto.mp4` COPIADO (un symlink no carga en `OffthreadVideo`) con keyframe cada 15 cuadros, `<OffthreadVideo muted style={{ maxWidth: "none" }}/>`, render `--muted` y audio con `montar.sh`.

**Variante «gráficos arriba, cara abajo»:** Remotion renderiza solo la franja de arriba (opaca) y ffmpeg la apila con el video (`scale` + `crop` + `vstack`, `-c:a copy`). Re-render y montaje en ~2 min.

### 5.B Video largo de YouTube con pantallas negras (16:9)

El editor deja en negro los tramos donde quiere motion, con la burbuja de cámara encima.
- **Estilo aprobado a la primera:** fondo verde con puntos + crema, logos en baldosas, íconos en vez de texto, clips oficiales en tarjeta, tablero ✓/✕. El color de fondo cambia cada DOS escenas con un barrido líquido marcado; las escenas del mismo color se cambian con un fundido de 0,35 s.
- **Un overlay por tramo,** escrito en segundos del video completo y renderizado en ProRes 4444 con alfa (`--codec=prores --prores-profile=4444 --pixel-format=yuva444p10le --image-format=png`; ~0,93 MB por cuadro).
- **Montaje:** cadena de `-itsoffset <inicio> -i sN.mov` + `overlay=eof_action=pass`, x264 CRF 18, y el audio (voz + efectos) mezclado APARTE a `.m4a` y unido con `-c:a copy`.
- **Barrido líquido:** cada escena se pinta ENCIMA del barrido que la abre (así el barrido se lleva la anterior sin animar salidas). Borde ondulado con dos senos, dos franjas de acento al frente, 0,55 s con `bezier(0.76, 0, 0.24, 1)`. La cresta va a ≤ ~1.500 px/s y sale completa del cuadro; nada del cuadro siguiente se ve antes de que la ola lo cubra.
- **Cortes secos pantalla → negro → pantalla** (la burbuja salta de chica a grande): el overlay arranca 14 cuadros ANTES del negro con un barrido sobre la grabación, el hueco de la burbuja se queda cerrado mientras crece y se abre cuando está quieta, y otro barrido destapa la pantalla 15 cuadros DESPUÉS. No se ve ni el corte ni un destello negro.
- **Un clip insertado sobre negro:** detrás nunca queda negro: va el fondo del motion con huecos exactos para el clip y la burbuja.
- **Antes de un render largo:** revisa el disco. Remotion escribe cada cuadro en `TMPDIR` (PNG ~6,7 MB). En videos enormes, renderiza por bloques de ~1.200 cuadros y únelos con `concat -c copy`.

### 5.C Motion en un tramo de un video ya terminado

1. Renderiza SOLO el tramo como overlay ProRes 4444 con alfa.
2. `ffmpeg -i FINAL -itsoffset <a> -i overlay.mov -filter_complex "overlay=eof_action=pass" -c:a copy …` (PSNR ≥ 46 dB fuera del tramo).
3. Entrega también el `.mov` transparente por si el editor lo quiere montar él.

Un sello sobre un video HEVC terminado: recodifica todo (`libx265 -crf 16 -tag:v hvc1`), no pegues un tramo recodificado con el resto copiado.

### 5.D Anuncios desde brutos crudos (estilo pauta)

El estilo pauta NO es el de los reels orgánicos:
- subtítulos de 2-3 palabras con la palabra activa en el color claro de la marca;
- gancho de 3 estilos de línea (fina cursiva, palabra grande en extra negrita, remate en negrita cursiva);
- nombre del presentador arriba, tarjeta con la fecha del evento y cierre «Regístrate gratis / en el botón de abajo»;
- solo voz, sin música, con un «pop» suave en los remates.

Flujo: `islas.py` → elegir tomas → `cortar.py` → verificar pedazo por pedazo. Tomas en una mesa con dos personas y un solo micrófono: quién habla sale del movimiento de la boca (`hablante.py`); el zoom alterna entre el plano general y el que habla.

### 5.E Anuncio in-stream de YouTube (16:9) con QR

- **Zona de peligro in-stream:** nada legible bajo y ≈ 842 (barra del botón en el celular); abajo a la izquierda va la tarjeta del anunciante (x < 820, y > 760); abajo a la derecha, «Saltar».
- **QR para quien lo ve en el televisor:** generado con `qrcode` (npm, nivel Q), pintado como SVG `crispEdges` en una tarjeta blanca de ~360 px, con la web escrita debajo. Cada formato lleva su propia UTM.
- **No pasable de 15 s:** el QR está en TODO el video como un objeto que nunca desaparece (un dock fijo que al final crece hasta ser el QR grande). Nada de animación de escaneo encima: quieto y limpio.
- **Verificar:** `verificar.py qr FINAL` debe leerlo desde < 1 s hasta el final, también a 640×360.
- **Modo tarjeta:** el plano se encoge a una tarjeta redondeada a un lado y la otra columna lleva listas: nunca se pierden las caras durante gráficos largos.

### 5.F Grabación de pantalla sincronizada con la cámara

Si el presentador grabó su pantalla mientras hablaba, el micrófono de esa grabación oye lo mismo que la cámara.
1. **Rescátala YA:** las grabaciones de macOS caen en una carpeta temporal `NSIRD_screencaptureui_*` que se borra sola, y copiar con la ruta escrita falla por las tildes. Copia con comodín: `…/NSIRD_screencaptureui_xxx/*.mov`.
2. **Desfase:** `sincro.py CAMARA PANTALLA`. Si la base ya está cortada: `sincro.py BASE PANTALLA --fino` da los tramos de desfase constante y la pantalla se corta con esos mismos tramos.
3. **Cuadros irregulares** (~24 fps variable): primero `fps=30` y DESPUÉS `trim` por número de cuadro, o sale segundos más larga (`cortar.py` ya lo hace así).
4. **Zoom por paso** en coordenadas normalizadas de la pantalla, y anillos sobre botones reales ubicados con OCR (`bin/ocr`) sobre cuadros reales.

**Resumen vertical de un video largo:** con los brutos de cámara y pantalla, el audio da el desfase de cada tramo contra el video final. Diseño: tarjeta de contenido arriba, presentador en otra tarjeta abajo con encuadre por tramo (Vision) y zoom alterno 1 / 1,12 para disimular los cortes, pastilla «Paso N», nada arriba de 260 ni debajo de 1700.

### 5.G Editar encima de una base ya cortada en CapCut

- `herramientas/capcut.py "<proyecto>"` resume el proyecto: tramos del bruto con su velocidad, sonidos con volumen y segundo, textos y stickers.
- **«Ponle mis efectos»:** la receta exacta (archivo, volumen lineal, segundo) está en ese JSON; no se adivina. Revisa antes qué trae ya horneado la base para no repetirlo.
- **Palabras sin transcribir la base:** `capcut.py … --palabras BRUTO.palabras.json --clip IMG_1234` pasa las palabras del bruto a la línea de tiempo de la base (sin las voces de los memes ni la música).
- **Coloca cada efecto por su PICO,** no por el inicio del archivo (un clic de mouse tiene su pico ~0,12 s dentro del archivo): `"alinear": "pico"` en `efectos.json`.

### 5.H Copiar un reel de referencia («hazlo igualito»)

- Muestréalo a 8-10 cuadros/s en hojas de contacto y anota cada escena en segundos y píxeles. Traduce la MECÁNICA (un objeto que se transforma, cómo entra y sale cada cosa), no los assets.
- **Un reel de Instagram sin descargarlo** (en tu navegador, con tu sesión): pausa el `<video>`, búscalo con `currentTime` (espera `seeked`), dibuja cada segundo en un `<canvas>` en una cuadrícula fija encima de la página y toma una captura (9 cuadros por captura). Instagram entrega el cuadro a 1080×1920 aunque `videoWidth` diga 720, y reemplaza el `<video>` cuando sale el aviso de registro: vuelve a buscar el elemento en cada llamada.
- **Los gráficos siguen lo que dice TU video,** no el guion de la referencia.

### 5.I HyperFrames (HTML + GSAP)

Útil para intros, separadores y motion de producto (`plantillas/motion-viaje/PROMPT.md` es un prompt autosuficiente que reconstruye un motion completo con tus fotos).
- Un `fromTo` con opacidad 1 en el «from» se pinta desde el cuadro 0 por `immediateRender`: lleva `immediateRender: false`.
- `radial-gradient(circle at X% Y%, … 34%)` se corta en cuadrado: dale radio en px.
- Los `<audio>` van estáticos dentro de `#root`, con `id` y pista propia.
- **Varias capas de video:** cada capa con su `z-index` explícito en el CSS; si no, un hijo con `zIndex` alto tapa las capas siguientes sin ningún error.
- `snapshot --at` con muchos tiempos y varios videos se cae por memoria: máximo ~10 tiempos por llamada.
- GSAP: `power2` es CÚBICA. `onUpdate` no corre en `seek()`: para trayectorias usa `keyframes` con `ease: "none"`.
- «Se pixela» en la vista previa casi nunca es el export: compruébalo con un render borrador. Nada de `filter: blur/drop-shadow` en elementos que se animan.
- `hyperframes remove-background` solo sirve para personas; para objetos, `bin/quitar_fondo` (Vision).
- **Lápiz que escribe:** UNA onda larga y continua por línea, nunca un zigzag por letra. «Fluido» = curvas largas y velocidad constante.

### 5.J Video generado con IA (cuentos animados)

- Si el prompt va en inglés, la voz sale en inglés: el diálogo va ENTRE COMILLAS en español, con «habla en español con acento colombiano» (o el tuyo).
- Primero se corta la narración real y después se pide UNA toma con los tiempos de cada tramo amarrados en el prompt (0-3 s saluda, 3-9 s trepa…): queda más fluido que encadenar extensiones.
- Para el parecido con una persona, describe sus rasgos uno por uno (cara larga, cejas rectas, pecas…) y pasa su foto como referencia.
- Verifica el saldo ANTES de diseñar y no gastes créditos sin permiso.
- Mezcla: la voz intacta y el audio generado por debajo (−14 dB cuando habla, pleno en sus pausas).

---

## 6. Interfaces reales: cómo recrearlas bien

1. **Abre la app real** en tu navegador (con tu sesión). Solo mira: no toques chats ni configuración. Las capturas con datos personales no se usan tal cual: se redibuja.
2. **Lee los estilos con JavaScript** desde la página: textos exactos, orden, `fontSize`, `color`, `borderRadius`, `boxShadow`, alto de filas. Así lo «real» sale de datos, no de memoria.
3. **Redibuja en React a tamaño de reel:** mismos textos y proporciones, letra agrandada para el celular (nombres ~31-32 px y descripciones ~27 px en un menú de 900 px).
4. **Sobre video oscuro,** lo que en la app vive sobre una página blanca va dentro de una tarjeta blanca, o no se lee.
5. **Los nombres de modelos y botones cambian cada pocas semanas:** revisa la app el mismo día. Ejemplo de cómo se documenta (3-nov-2026): el selector de claude.ai se abría sobre un botón bajo la caja de texto, popover blanco de radio 14 y filas de 46 px; la lista de modelos de chatgpt.com solo aparecía en la vista «Work».

**Logos e imágenes oficiales:**
- **LobeHub** (`@lobehub/icons-static-svg` en jsDelivr): OpenAI, Claude, xAI, Meta y otros de IA.
- **`https://logos.composio.dev/api/<slug>`:** el SVG oficial de cientos de apps (gmail, notion, slack, stripe…), todos con el mismo estilo.
- **Wikimedia Commons (API):** logos de apps conocidas. Ojo con homónimos.
- **La imagen og de la página oficial:** productos nuevos. Si un sitio da 403 a curl, su og o sus `assets.` suelen bajar desde el navegador.
- **Tweets reales:** `https://api.fxtwitter.com/<usuario>/status/<id>` da el texto exacto, la fecha, las cifras y el avatar sin iniciar sesión. Nunca de memoria.
- **Clips oficiales** (keynotes): `yt_dlp` (módulo de Python); con los subtítulos ubicas cada anuncio sin ver la hora entera. Pide permiso antes de descargar.
- **Recortes:** un logo sobre fondo blanco se vuelve transparente con alfa = 255 − min(G, B); un objeto, con `bin/quitar_fondo --recortar`.

---

## 7. Audio

- **La voz no se toca.** Se mezcla aparte (`herramientas/efectos.py`) y se une con `-c copy`. Mezclar efectos en el mismo `filter_complex` que los overlays llegó a cortar la pista sin dar error.
- **`amix normalize=0` siempre;** si no, ffmpeg baja la voz.
- **Nunca metas el audio en el render de Remotion:** con `--audio-codec=aac` la voz salió 43 ms atrasada. Render `--muted` + `montar.sh`.

**Niveles que funcionaron** (picos, sobre una voz de −14 a −19 LUFS):

| Uso | Nivel |
|---|---|
| Clic suave de cursor (`click-soft`, pasa-altos 500 / pasa-bajos 7000) | −21 dBFS ± 2,5 aleatorio |
| Whoosh de barrido (`whoosh-short`, pasa-altos 220 / pasa-bajos 7500) | −35 dBFS, energía máxima a mitad del barrido |
| Golpe grave en títulos (seno de 95 → 48 Hz) | −37 dBFS |
| Contador de barras (un tic cada vez que el número pasa un entero, con la misma curva que la barra) | ~13 LU bajo la voz |
| Reels con más efectos | golpe −18, sellos −22, whoosh −27, pop −29, clic −31, teclas −35 |

- **Voz opaca y baja** (no ruidosa), solo si la piden limpia: `herramientas/limpiar_voz.py` (highpass 75 Hz, −3 dB en 300 Hz, +2,5 dB en 3,2 kHz, compresor suave, loudnorm en dos pasadas a −14 LUFS). Sin denoise: solo mete artefactos.
- **`alimiter` sube el nivel solo:** para limitar sin subir, `level=false`.
- **`loudnorm` de una pasada aplana los contrastes** (oficina fuerte → calma): en piezas de contraste, mide el LUFS y aplica una ganancia fija.
- **Librería de efectos:** la que trae HyperFrames (`~/.claude/skills/media-use/audio/assets/sfx/`) y el paquete gratis de efectos de Adobe Audition (descárgalo tú de la página de Adobe; no se redistribuye).

---

## 8. Trampas de Remotion, ffmpeg y el entorno

**Remotion**
- `interpolate` con un rango de duración 0 revienta y el cuadro entero sale NEGRO sin aviso (`ramp` de la plantilla ya lo evita).
- Un CSS global con `max-width:100%` en `<img>`/`<video>` encoge o pone negro un `OffthreadVideo` escalado: `maxWidth: "none"`.
- Las fuentes deben cargar antes de medir texto (la plantilla usa `@remotion/google-fonts`, que bloquea el render hasta que cargan).
- Tailwind v4 escanea TODO el proyecto: un `.wav` grande colgó el bundle 6 min. Mantén el `.gitignore` y los audios fuera de `src/`.
- `remotion bundle` copia todo `public/`: con poco disco, usa `--public-dir` apuntando a una carpeta liviana.
- `Config.setVideoImageFormat("jpeg")` para H.264; PNG solo para overlays con alfa.
- No esperes el render en primer plano: lánzalo en segundo plano.

**ffmpeg y zsh**
- zsh: `$n:layout` o `$ms:all` se leen como modificadores (`:l`, `:a`) y rompen el filtro sin aviso: usa SIEMPRE `${n}` antes de `:`.
- `vstack`/`hstack` con más de 2 entradas necesitan `=inputs=N`.
- Para ver la salida de `psnr` y `ebur128` no uses `-v error`: `-hide_banner` + `grep`.
- `colorkey` pone alfa = 255 a todo lo que no coincide; `tblend` marca un corte un cuadro tarde (usa `select='between(n,a,b)',tile`).
- Chroma key (#00FF00): cero fundidos y ningún verde propio en el diseño.
- `rsync --exclude logos` también excluye `sub/logos`; para la raíz, `--exclude /logos`.

**Entorno (Mac)**
- **Discos exFAT** (discos externos): `npm install` falla, salen archivos `._*` y cada archivo ocupa ≥ 1 MB (una caché de cuadros de 0,5 GB llegó a ocupar 9 GB). Trabaja los proyectos en el disco interno y copia al externo solo código y renders. Mandar algo a la Papelera del mismo disco no libera espacio.
- **Brutos de iPhone en HDR:** conviértelos con `hdr_a_sdr.sh` (conversor de Apple: mismos tiempos, ya girados) y compara un cuadro contra el original. Nunca filtros de color por tu cuenta.
- **Grabaciones de pantalla en carpetas temporales:** se borran solas (sección 5.F).
- **Los scripts de medición viven en el proyecto** (`herramientas/`), no en carpetas temporales que se vacían.

---

## 9. Verificación antes de entregar (siempre)

| Qué | Cómo |
|---|---|
| Duración y cuadros de CADA stream | `verificar.py streams FINAL` |
| Sincronía de la voz contra la base (0 ms) | `verificar.py sincro FINAL BASE` (si la voz no se re-cortó) |
| Lo que no se tocó sigue igual | `verificar.py psnr FINAL BASE a-b` (≥ ~42 dB) |
| Volumen de la voz igual que en la base | `verificar.py volumen FINAL BASE` |
| No se coló ninguna toma repetida | `verificar.py texto FINAL` y leerlo entero |
| Zonas de peligro y cabeza | `verificar.py zonas FINAL 1.5,6.4,…` (cuadros del ENTREGABLE, no del proyecto) |
| QR legible | `verificar.py qr FINAL` |
| Datos sensibles censurados | OCR (`bin/ocr`) de TODOS los cuadros del entregable; lo que siga legible se vuelve cajas extra |

En los cuadros del entregable pregúntate: ¿la cabeza entera en las pantallas partidas?, ¿nada en las zonas de peligro?, ¿nada encima de lo que ya venía quemado?, ¿las tarjetas caben?

---

## 10. Entrega y comunicación

- **Nombre:** `<Tema> EDITADO.mp4` junto a la base; correcciones con nombre NUEVO (`… v2`, `… sin subtitulos`). Los editores de video cachean por ruta: un archivo sobrescrito puede seguir mostrando la duración vieja.
- **Muéstralo:** `open -R "<archivo>"` (lo abre seleccionado en el Finder).
- **Mensaje final, corto y en español:** qué tiene el video por tramos con sus segundos; qué respetaste; cómo lo verificaste; qué se puede quitar fácil. Si algo no se pudo hacer o no está verificado, dilo claro.

---

## 11. Números de referencia (Mac Apple Silicon)

| Qué | Cuánto |
|---|---|
| Whisper large-v3-turbo con Metal | ~5-10× tiempo real (40 s → ~9 s) |
| `cortar.py` de un bruto 1080p de 40 s | ~15 s |
| `still.sh` (bundle + 6 cuadros) | ~25 s |
| Reel 1080×1920 de 196 s, render H.264 | ~6 min |
| ProRes 4444 de overlay | ~0,93 MB por cuadro |
| Montaje x264 CRF 18 de 2 h 35 min | ~27 min |
| Pantallas negras por keyframes, 2 h 35 min | ~2,5 min |
| Caras con Vision, 200 cuadros | ~5 s |
