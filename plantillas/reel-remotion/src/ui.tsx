import React from "react";
import { Easing, interpolate } from "remotion";
import CURSOR from "./datos/cursor.json";
import PARTIDA from "./datos/partida.json";
import { clamp, golpe, ramp, useT } from "./kit";
import { MARCA } from "./marca";

// ── Zonas de un reel 1080×1920 (Instagram / TikTok). NADA importante en ellas.
//   arriba 0-270: la interfaz de Instagram · abajo desde ~1480: la descripción · derecha x > 960: los botones.
export const ZONA = { arriba: 270, abajo: 1480, derecha: 960 };
// Franjas libres con el presentador completo (mídelas con herramientas/cabeza.py: cambian con cada persona y plano).
export const PARED = { top: 300, bottom: 568 }; // sobre la cabeza
export const PIERNAS = { top: 1080, bottom: 1470, left: 120, w: 840 }; // sobre las piernas, simétrica respecto al centro

// ── Pantalla partida: el panel baja desde arriba y el video baja lo justo para que la cabeza quede ≥ 30 px bajo la ola.
export const PANEL = PARTIDA.panel;
const TR = 0.5;
const tramo = (t: number, a: number, b: number) =>
  Math.min(
    interpolate(t, [a, a + TR], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) }),
    interpolate(t, [b, b + TR], [1, 0], { ...clamp, easing: Easing.inOut(Easing.cubic) }),
  );
const TRAMOS = PARTIDA.tramos as [number, number, number][];
/** 0 = pantalla completa · 1 = partida. Panel y video se mueven con la MISMA curva. */
export const partida = (t: number) => (TRAMOS.length ? Math.max(...TRAMOS.map(([a, b]) => tramo(t, a, b))) : 0);
/** Cuántos px baja el video en t. */
export const bajada = (t: number) => TRAMOS.reduce((acc, [a, b, d]) => acc + tramo(t, a, b) * d, 0);

/** Borde inferior del panel: línea de acento de 10 px que ondula. */
const Ola: React.FC = () => {
  const t = useT();
  const pts: string[] = [];
  for (let x = 0; x <= 1080; x += 12) pts.push(`${x},${14 + Math.sin(x / 70 + t * 3) * 7}`);
  return (
    <svg width={1080} height={60} style={{ position: "absolute", left: 0, top: PANEL - 14, overflow: "visible" }}>
      <path d={`M0,-20 L${pts.join(" L")} L1080,-20 Z`} fill={MARCA.crema} />
      <polyline points={pts.join(" ")} fill="none" stroke={MARCA.acento} strokeWidth={10} strokeLinejoin="round" />
    </svg>
  );
};

/** Panel crema con cuadrícula suave. Lo que va dentro: las demos (apps reales recreadas). */
export const Panel: React.FC<{ children?: React.ReactNode }> = ({ children }) => {
  const t = useT();
  const s = partida(t);
  if (s < 0.001) return null;
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: 1080, height: PANEL, transform: `translateY(${(s - 1) * (PANEL + 60)}px)` }}>
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundColor: MARCA.crema,
          backgroundImage: "linear-gradient(rgba(13,51,38,0.06) 2px, transparent 2px), linear-gradient(90deg, rgba(13,51,38,0.06) 2px, transparent 2px)",
          backgroundSize: "54px 54px",
          backgroundPosition: "-2px -2px",
        }}
      />
      <Ola />
      {/* contenido diseñado para la franja libre: debajo de los 270 px de arriba */}
      <div style={{ position: "absolute", left: 0, top: ZONA.arriba, width: 1080, height: PANEL - ZONA.arriba - 30 }}>{children}</div>
    </div>
  );
};

// ── Cursor de Mac con onda de acento al hacer clic. Lee datos/cursor.json, igual que el sonido de los clics.
const easeIO = Easing.inOut(Easing.cubic);
export const posCursor = (t: number): [number, number] => {
  const p = CURSOR.puntos as number[][];
  if (t <= p[0][0]) return [p[0][1], p[0][2]];
  for (let i = 1; i < p.length; i++) {
    if (t <= p[i][0]) {
      const [t0, x0, y0] = p[i - 1];
      const [t1, x1, y1] = p[i];
      const k = easeIO((t - t0) / Math.max(0.001, t1 - t0));
      return [x0 + (x1 - x0) * k, y0 + (y1 - y0) * k];
    }
  }
  const u = p[p.length - 1];
  return [u[1], u[2]];
};
export const clic = (nombre: keyof typeof CURSOR.clics) => CURSOR.clics[nombre];

export const Cursor: React.FC = () => {
  const t = useT();
  const tr = (CURSOR.visible as number[][]).find(([a, b]) => t >= a - 0.01 && t < b);
  if (!tr) return null;
  const [a, b] = tr;
  const op = Math.min(ramp(t, a, 0.25), 1 - interpolate(t, [b - 0.3, b], [0, 1], clamp));
  const [x, y] = posCursor(t);
  const clics = Object.values(CURSOR.clics).filter((c) => t >= c - 0.05 && t < c + 0.45);
  const press = clics.reduce((m, c) => Math.min(m, golpe(t, c)), 1);
  return (
    <div style={{ position: "absolute", inset: 0, opacity: op, pointerEvents: "none" }}>
      {clics.map((c) => {
        const k = interpolate(t, [c, c + 0.45], [0, 1], clamp);
        return (
          <div
            key={c}
            style={{ position: "absolute", left: x - 46 * k, top: y - 46 * k, width: 92 * k, height: 92 * k, borderRadius: "50%", border: `6px solid ${MARCA.acento}`, opacity: 1 - k }}
          />
        );
      })}
      <div style={{ position: "absolute", left: x - 3, top: y - 2, transform: `scale(${press})`, transformOrigin: "3px 2px" }}>
        <svg width={44} height={66} viewBox="0 0 20 30" style={{ overflow: "visible", display: "block" }}>
          <path d="M1 1 L1 23 L6.5 17.8 L10.2 27 L14 25.4 L10.4 16.4 L18 16.4 Z" fill="#111" stroke="#fff" strokeWidth={2} strokeLinejoin="round" />
        </svg>
      </div>
    </div>
  );
};
