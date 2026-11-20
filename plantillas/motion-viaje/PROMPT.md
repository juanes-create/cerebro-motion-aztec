Quiero que me hagas un motion graphic con HyperFrames, desde cero. Vas a seguir una coreografía ya probada (la describo abajo con tiempos y medidas exactas) y la vas a adaptar a lo que yo quiera presentar: un producto, un viaje, un evento, un servicio, lo que sea. Te adjunto mis fotos.

## 0. Antes de empezar
- Revisa que tenga Node 22 o más nuevo y ffmpeg. Si falta algo, dime cómo instalarlo y espera.
- Instala las skills de HyperFrames con `npx hyperframes skills` y úsalas: empieza por /hyperframes y sigue su flujo de /motion-graphics. Crea el proyecto con `npx hyperframes init mi-motion --non-interactive --example=blank`.

## 1. Entrevístame (UNA sola ronda de preguntas, todas juntas, cortas y con opciones)
Mira primero las fotos que adjunté y después pregúntame solo lo que no puedas deducir:
1. ¿Qué vas a presentar y cuál es el mensaje principal? (ej.: «mi nueva botella térmica», «un viaje a Japón»)
2. ¿Formato? a) mitad de arriba de un reel 1080×960 (para poner tu cara abajo) · b) reel completo 1080×1920 · c) horizontal 1920×1080.
3. ¿Colores? a) el gris claro neutro del ejemplo · b) los colores de mi marca (dime cuáles o pásame el logo).
4. ¿Idioma de los textos y tono? (ej.: español, cercano)
5. ¿Con efectos de sonido? (recomendado: sí)
6. ¿Cómo cierra? a) el círculo se vuelve un punto que revienta (como el ejemplo) · b) el punto se convierte en mi logo · c) el punto se convierte en una frase final corta.
Con mis respuestas, propón el GUION: qué foto va en cada papel y todos los textos. Muéstramelo en una tabla y espera mi «ok» antes de construir.

## 2. Los papeles (adáptalos a mi tema)
- PROTAGONISTA (va sin fondo): lo principal, al centro. Un producto, un reloj, un celular, una taza…
- 3 TARJETAS: datos cortos sobre lo que presento (precio, característica, fecha, clima, un QR…).
- OBJETO QUE CRUZA (sin fondo, ancho y horizontal): algo que pasa de lado a lado (avión, carro, el mismo producto acostado…). Si no hay ninguna foto ancha, usa el protagonista girado o una frase grande en una sola línea.
- 4 BURBUJAS con ícono (íconos sin fondo): beneficios, destinos, ingredientes, ventajas. Una palabra cada una. Si no tengo íconos, recórtalos de mis fotos.
- REDONDO (sin fondo): algo circular que asoma abajo dentro del círculo (planeta, plato, balón, el producto visto desde arriba…). Si no hay, dibuja un planeta con degradados.
- 4 FOTOS para el círculo: dónde se usa, ambientes, resultados. La segunda puede ser un objeto sin fondo que flota sobre un cielo.
Si me falta algo importante, pídemelo dentro de la misma ronda de preguntas.

Para quitar fondos en Mac (macOS 14 o más nuevo), escribe un script de Swift con Vision: `VNGenerateForegroundInstanceMaskRequest` y `generateMaskedImage(ofInstances: obs.allInstances, from: handler, croppedToInstancesExtent: true)`, guardando PNG transparente. (`npx hyperframes remove-background` solo sirve con personas.) Abre cada recorte y revisa que esté limpio. Si no estoy en Mac, pídeme los PNG sin fondo.

## 3. La coreografía (respétala; solo cambian imágenes, textos y colores)
Medidas para el lienzo de referencia 1080×960, 30 fps, 3,5 s (4,5 s si cierra con logo o frase). Las medidas del protagonista y del objeto son la altura y el ancho máximos: respeta las proporciones de cada foto. Si una foto es pequeña (menos de 600 px de ancho), muéstrala más chica en vez de estirarla, para que no se pixele. Si elegí 1080×1920, usa el mismo diseño centrado verticalmente (súmale 480 px a todas las «y») y extiende el fondo. Si elegí 1920×1080, escala todo ×1,125 y céntralo. Fuente Inter 400 y 700 con @font-face a archivos locales (cópialos de las skills: `hyperframes-creative/frame-presets/code-editorial/fonts/`), o la fuente de mi marca si me la pediste. Un solo `index.html`, una línea de tiempo GSAP pausada, todo animado con transform/opacity (x, y, scale, rotation), nunca left/top.

Fondo (con los colores del ejemplo; si elegí mi marca, tradúcelo a mis colores en tonos suaves): #EDEDF0 con una franja gris arriba (degradado vertical #8d8d91 en 0 px → #bdbdc1 en 110 → #e3e3e6 en 250 → #ededf0 en 360). Anillos concéntricos suaves centrados en (540, 490): círculo #dddce1 hasta radio 200, anillo #e4e3e7 hasta 323, anillo #e9e8ec hasta 456. Detrás del protagonista, un brillo de colores con degradados radiales suaves (rosa arriba a la izquierda, verde abajo a la derecha, lila arriba a la derecha).

Cámara: todo (menos el fondo) va en un contenedor que hace scale 1 → 1,06 durante toda la pieza (sine.inOut). Los anillos hacen scale 0,94 → 1,04.

ESCENA 1 · Protagonista (0 – 0,95 s). Todo se ve desde el cuadro 0.
- PROTAGONISTA centrado en (540, 490), 415 px de alto, con scale 1,1 → 1 (expo.out, 0,5 s). Si tiene pantalla, tápala con un div redondeado: primero un degradado cálido, y a los 0,55 s una interfaz oscura mini con datos de mi tema. Si no tiene pantalla (una lata, una taza), no tapes nada: las tarjetas vuelan a su centro.
- 3 tarjetas de vidrio gris (rgba(118,118,124,0,62), radio 18, texto blanco, sombra suave): izquierda (x 235, y 400, 185×118), arriba a la derecha (600, 255, 240×140) y abajo a la derecha (505, 540, 160×190). De 0 a 0,3 s se asientan desde un poco afuera (expo.out). De 0,30 a 0,56 s (0,03 s entre ellas) vuelan al centro del protagonista, encogiéndose a 0,16 y girando ±8° (power3.in), y desaparecen.
- A los 0,56 s el protagonista «recibe» las tarjetas: scale 1 → 1,07 (0,09 s) → 1 (elastic.out(1, 0.5), 0,3 s).
- Frase en dos partes a los lados del protagonista (Inter 400 de 50 px, #2b2b2e, máximo 12 caracteres por lado): la primera termina 45 px a la izquierda del protagonista y la segunda empieza 40 px a su derecha. Entran a los 0,5 s desde ±320 px (expo.out, 0,45 s).

ESCENA 2 · Objeto y burbujas (0,95 – 1,75 s)
- El OBJETO (990 px de ancho, centrado en y = 465) entra desde x −1350 en 0,38 s (expo.out). El protagonista sale empujado (x +120, scale 0,8, opacity 0, power3.in, 0,24 s), la frase sale hacia los lados y el brillo se apaga. Después el objeto flota suave (x +22, y −6, rotación −1,2°).
- 4 burbujas tipo chat (52 px de alto, radio 26, texto Inter 28 px, sombra suave, colita triangular abajo a la derecha): 1 azul #2f8cff con texto blanco en (268, 285); 2 blanca en (690, 256); 3 blanca en (205, 596); 4 azul en (620, 602). El ícono sobresale por el borde izquierdo de la burbuja; si es alto y delgado (un monumento) puede medir 74 a 116 px de alto, y si es ancho (una fruta, un plato) va en una caja de 72×72 con object-fit: contain para que no tape el texto. En la 4 va a la derecha y más pequeño. Aparecen a 1,28 s + 0,06 s cada una, desde scale 0 (back.out(2.6), 0,32 s). Si elegí mis colores, el azul se cambia por mi color principal.

ESCENA 3 · El círculo (1,75 – 2,6 s)
- Un contenedor con clip-path circle se abre de 0 a 285 px en (540, 470) (back.out(1.4), 0,32 s). Adentro: un disco gris #5e5f65, las fotos (620×620, object-fit cover) y el REDONDO (660 px), que sube desde 220 px más abajo (expo.out, 0,45 s), queda asomado abajo y gira 14° despacio.
- Las burbujas se van «chupadas» al centro (scale 0, power3.in, 0,22 s) y el objeto se encoge a 0,58 (power3.inOut, 0,34 s). El objeto va POR ENCIMA del círculo, sin recortar.
- Las fotos cambian con cortes secos a 1,98 / 2,14 / 2,30 / 2,46 s, cada una con zoom 1,22 → 1 (expo.out, 0,3 s). Si la segunda es un objeto sin fondo, va sobre un cielo degradado (#5f8fd0 → #a9c8ee → #dbe8f7) subiendo un poco.
- Los anillos bajan a opacity 0,35.

CIERRE (2,6 – 3,5 s)
- 2,60 s: el círculo se corre a (470, 478) con radio 225 y muestra la segunda foto (power3.inOut, 0,16 s); el objeto sale disparado a la derecha (x +1300, power3.in, 0,24 s).
- 2,78 s: el círculo se cierra a 0 (power3.in, 0,16 s) y los anillos desaparecen.
- 2,90 s: punto gris #8e8e93 de 50 px en el centro (back.out(2.5)).
  - Cierre a: a los 3,04 s el punto se encoge y un anillo de borde 4 px se expande de 0,3 a 2,6 (expo.out, 0,42 s) mientras se desvanece.
  - Cierre b o c: la pieza dura 4,5 s. A los 3,04 s el punto crece a 2,2 y se desvanece (power2.in, 0,16 s), el mismo anillo se expande, y a los 3,1 s entra mi logo o la frase final en el centro, unos 540 px de ancho (scale 0,2 → 1, back.out(1.6), 0,42 s); luego crece suave a 1,04 hasta el final. El punto y el anillo van del color principal de mi marca. Si el logo viene sobre fondo blanco, vuélvelo transparente antes de usarlo.

## 4. Fluidez
- Motion blur: `npx hyperframes add motion-blur` y `data-hf-motion-blur` SOLO en el objeto y en las 3 tarjetas (en las tarjetas con '{"samplesPerFrame": 8}').
- Ningún tiempo muerto: la cámara nunca para.

## 5. Sonidos (si dije que sí)
Librería que trae HyperFrames (skill media-use, carpeta `audio/assets/sfx/`). Cópialos a `assets/sfx/`. Cada uno va como `<audio>` con id y pista propia:
- whoosh-short a 0,28 s (volumen 0,45): vuelan las tarjetas.
- pop a 0,54 s (0,35): encajan en el protagonista.
- whoosh a 0,90 s (0,6): entra el objeto.
- sparkle a 1,26 s (0,35, dura 0,9 s): aparecen las burbujas.
- whoosh-cinematic a 1,70 s con `data-media-start="1.9"`, duración 1,3 s, volumen 0,3 y fade a 0 en los últimos 0,3 s (`data-automation`): el círculo y las fotos.
- whoosh a 2,58 s (0,55): sale el objeto.
- impact-bass-1 a 3,0 s (0,25) con fade a 0 en 0,5 s: el cierre. Si cierra con logo o frase: a los 3,04 s, que dure 1,4 s con fade al final, y suma sparkle a los 3,12 s (0,3) cuando aparece el logo.
Nada de clics.

## 6. Trampas conocidas (evítalas)
- Los degradados radiales con radio en porcentaje se cortan en un cuadrado visible: dales radio en px (`circle 250px at …`).
- Un `fromTo` cuyo «from» tiene `opacity: 1` y empieza tarde (como el anillo del cierre) se pinta desde el cuadro 0: ponle `immediateRender: false`.
- Los anillos a pantalla completa (`inset: 0`) disparan el error `gsap_fullscreen_overlay_starts_visible`: ponlos en un div de 912×912 centrado.
- El aviso de contraste del texto blanco sobre el vidrio gris es solo un aviso, no lo corrijas.

## 7. Revisa y entrégame
1. `npx hyperframes lint .` y `npx hyperframes check .` sin errores.
2. Capturas con `npx hyperframes snapshot . --at 0.2,0.8,1.2,1.6,2.2,2.7,3.1` (y 4.0 si el cierre lleva logo o frase). Revísalas tú (nada cortado, tapado ni pixelado) y muéstramelas.
3. Renderiza con `npx hyperframes render . -q high -o renders/mi-motion.mp4` y dime dónde quedó.
4. Al final, dime en una línea que en este mismo chat puedo pedirte cambios o motions nuevos solo describiéndolos.
