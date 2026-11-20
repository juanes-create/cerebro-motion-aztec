import React from "react";
import { Easing, interpolate, useCurrentFrame } from "remotion";
import CONFIG from "./datos/config.json";
import { MARCA, SOMBRA, TITULO } from "./marca";

// Todo el motion se escribe en SEGUNDOS DEL VIDEO BASE, copiados de <video>.palabras.json (herramientas/transcribir.py).
export const FPS = CONFIG.fps;
export const useT = () => useCurrentFrame() / FPS;

export const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

/** 0→1 con curva entre a y a+d (segundos). Con d = 0 sería un rango vacío: interpolate revienta y sale todo NEGRO. */
export const ramp = (t: number, a: number, d = 0.35, ease = Easing.out(Easing.cubic)) =>
  interpolate(t, [a, a + Math.max(d, 0.001)], [0, 1], { ...clamp, easing: ease });

/** Golpe de escala corto (botón que recibe un clic). */
export const golpe = (t: number, at: number) => interpolate(t, [at - 0.02, at + 0.06, at + 0.2], [1, 0.9, 1], clamp);

/** Visible entre a y b: entra con pop y sale rápido. Fuera del tramo no se dibuja. */
export const Tramo: React.FC<{ a: number; b: number; y?: number; style?: React.CSSProperties; children: React.ReactNode }> = ({
  a,
  b,
  y = 40,
  style,
  children,
}) => {
  const t = useT();
  if (t < a || t >= b) return null;
  const entra = interpolate(t, [a, a + 0.45], [0, 1], { ...clamp, easing: Easing.out(Easing.back(1.5)) });
  const sale = interpolate(t, [b - 0.25, b], [0, 1], { ...clamp, easing: Easing.in(Easing.cubic) });
  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        opacity: Math.min(ramp(t, a, 0.15), 1 - sale),
        transform: `translateY(${(1 - entra) * y + sale * -24}px) scale(${(0.92 + 0.08 * entra) * (1 - 0.06 * sale)})`,
        ...style,
      }}
    >
      {children}
    </div>
  );
};

/** Aparece en `at` con un pop (escala + opacidad), sincronizado con una palabra. */
export const Pop: React.FC<{ at: number; from?: number; x?: number; y?: number; style?: React.CSSProperties; children: React.ReactNode }> = ({
  at,
  from = 0.5,
  x = 0,
  y = 0,
  style,
  children,
}) => {
  const t = useT();
  const s = interpolate(t, [at, at + 0.4], [0, 1], { ...clamp, easing: Easing.out(Easing.back(1.7)) });
  return (
    <div style={{ ...style, opacity: ramp(t, at, 0.12), transform: `${style?.transform ?? ""} translate(${(1 - s) * x}px, ${(1 - s) * y}px) scale(${from + (1 - from) * s})` }}>
      {children}
    </div>
  );
};

/**
 * Texto que se escribe letra por letra entre a y b. El texto va COMPLETO en el DOM y lo no escrito es transparente:
 * así la línea nunca salta ni se reacomoda mientras se escribe.
 */
export const Typed: React.FC<{ texto: string; a: number; b: number; style?: React.CSSProperties; cursor?: boolean }> = ({ texto, a, b, style, cursor = true }) => {
  const t = useT();
  const n = Math.round(interpolate(t, [a, b], [0, texto.length], clamp));
  const parpadeo = Math.floor(t * 2) % 2 === 0 || (t >= a && t < b);
  return (
    <span style={style}>
      {texto.split("").map((c, i) => (
        <span key={i} style={{ color: i < n ? undefined : "transparent" }}>
          {c}
        </span>
      ))}
      {cursor && t >= a - 0.3 ? (
        <span style={{ display: "inline-block", width: 0, overflow: "visible" }}>
          <span style={{ display: "inline-block", width: 4, height: "1em", marginLeft: 3, verticalAlign: "-0.12em", background: MARCA.acento, opacity: parpadeo ? 1 : 0 }} />
        </span>
      ) : null}
    </span>
  );
};

/** Píldora de texto (títulos cortos en la pared). */
export const Pill: React.FC<{ children: React.ReactNode; bg?: string; color?: string; size?: number; style?: React.CSSProperties }> = ({
  children,
  bg = MARCA.oscuro,
  color = "#fff",
  size = 34,
  style,
}) => (
  <span
    style={{
      display: "inline-flex",
      alignItems: "center",
      gap: 12,
      background: bg,
      color,
      fontFamily: TITULO,
      fontWeight: 800,
      fontSize: size,
      borderRadius: 999,
      padding: `${size * 0.32}px ${size * 0.7}px`,
      whiteSpace: "nowrap",
      boxShadow: "0 10px 30px rgba(0,0,0,0.25)",
      ...style,
    }}
  >
    {children}
  </span>
);

/** Tarjeta blanca redondeada con sombra suave (nunca bordes con trazo). */
export const Caja: React.FC<{ style?: React.CSSProperties; children?: React.ReactNode }> = ({ style, children }) => (
  <div style={{ background: "#fff", borderRadius: 34, boxShadow: SOMBRA, ...style }}>{children}</div>
);

export const Check: React.FC<{ size: number; color?: string; draw?: number }> = ({ size, color = MARCA.acento, draw = 1 }) => (
  <svg width={size} height={size} viewBox="0 0 100 100">
    <circle cx={50} cy={50} r={48} fill={color} />
    <path d="M28 52 L44 67 L73 36" fill="none" stroke="#fff" strokeWidth={10} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={70} strokeDashoffset={70 * (1 - draw)} />
  </svg>
);
