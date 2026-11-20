import React from "react";
import { Easing, interpolate } from "remotion";
import { Caja, Check, clamp, golpe, Pill, Pop, ramp, Tramo, Typed, useT } from "./kit";
import { MARCA, TEXTO, TITULO } from "./marca";
import { clic, PARED, PIERNAS } from "./ui";

/*
 * Escenas de EJEMPLO. Cámbialas por las de tu video, siempre con estas reglas:
 *  - cada cosa entra en el segundo exacto de la palabra que la dispara (de <video>.palabras.json);
 *  - texto mínimo, visuales e interfaces REALES; simétrico respecto al centro (x = 540);
 *  - sin trazos en el texto (nada de WebkitTextStroke): degradado y sombra suave.
 */

/** Gancho: ya está en pantalla en el cuadro 0 (la portada del reel) y sobre la pared, nunca en los 270 px de arriba. */
export const Gancho: React.FC = () => {
  const t = useT();
  if (t >= 2.9) return null;
  const sale = interpolate(t, [2.6, 2.9], [0, 1], { ...clamp, easing: Easing.in(Easing.cubic) });
  const golpeTitulo = interpolate(t, [0, 0.18, 0.4], [1.08, 0.97, 1], clamp);
  return (
    <div style={{ position: "absolute", left: 0, top: PARED.top, width: 1080, height: PARED.bottom - PARED.top, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 18, opacity: 1 - sale }}>
      <div
        style={{
          fontFamily: TITULO,
          fontWeight: 800,
          fontSize: 92,
          lineHeight: 1.02,
          color: "#fff",
          textAlign: "center",
          transform: `scale(${golpeTitulo})`,
          textShadow: "0 6px 30px rgba(0,0,0,0.55)",
        }}
      >
        Tu gancho <span style={{ color: MARCA.claro }}>aquí</span>
      </div>
      <Pop at={0.9}>
        <Pill bg={MARCA.acento} color={MARCA.oscuro}>en 3 pasos</Pill>
      </Pop>
    </div>
  );
};

/** Demo dentro del panel (pantalla partida): una app de chat GENÉRICA. En tu video, recrea la app REAL de hoy. */
export const Demo: React.FC = () => {
  const t = useT();
  const enviado = t >= clic("enviar");
  return (
    <Tramo a={3.2} b={9.4} y={30}>
      <div style={{ position: "absolute", left: 90, top: 40, width: 900 }}>
        <Caja style={{ padding: "34px 36px", borderRadius: 30 }}>
          <div style={{ fontFamily: TEXTO, fontSize: 26, color: MARCA.gris, marginBottom: 18 }}>Nuevo chat</div>
          {enviado ? (
            <div style={{ display: "flex", justifyContent: "flex-end", marginBottom: 20, opacity: ramp(t, clic("enviar"), 0.2) }}>
              <div style={{ background: "#F1EFEA", borderRadius: 26, padding: "18px 24px", fontFamily: TEXTO, fontSize: 30, color: MARCA.tinta, maxWidth: 700 }}>
                Resume este documento en 5 puntos
              </div>
            </div>
          ) : null}
          <div style={{ display: "flex", alignItems: "center", gap: 18, border: `2px solid ${MARCA.linea}`, borderRadius: 26, padding: "20px 22px" }}>
            <div style={{ flex: 1, fontFamily: TEXTO, fontSize: 31, color: MARCA.tinta, minHeight: 40 }}>
              {enviado ? <span style={{ color: MARCA.gris }}>Escribe un mensaje…</span> : <Typed texto="Resume este documento en 5 puntos" a={3.9} b={5.9} />}
            </div>
            <div
              style={{
                width: 64,
                height: 64,
                borderRadius: 20,
                background: MARCA.oscuro,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                transform: `scale(${golpe(t, clic("enviar"))})`,
              }}
            >
              <svg width={30} height={30} viewBox="0 0 24 24">
                <path d="M12 19V5M5 12l7-7 7 7" stroke="#fff" strokeWidth={3} fill="none" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </div>
          </div>
          {enviado ? (
            <div style={{ marginTop: 22, display: "flex", flexDirection: "column", gap: 12 }}>
              {[0, 1, 2].map((i) => (
                <div key={i} style={{ height: 22, borderRadius: 11, background: "#ECEAE5", width: `${[92, 78, 60][i] * interpolate(t, [clic("enviar") + 0.4 + i * 0.25, clic("enviar") + 1 + i * 0.25], [0, 1], clamp)}%` }} />
              ))}
            </div>
          ) : null}
        </Caja>
      </div>
    </Tramo>
  );
};

/** Tarjeta sobre las piernas: lista que se marca palabra por palabra. */
export const Lista: React.FC = () => {
  const t = useT();
  const items: [string, number][] = [
    ["Lo transcribe solo", 10.4],
    ["Corta las pausas", 11.3],
    ["Anima cada palabra", 12.2],
  ];
  return (
    <Tramo a={10.0} b={13.6}>
      <div style={{ position: "absolute", left: PIERNAS.left, top: PIERNAS.top + 20, width: PIERNAS.w }}>
        <Caja style={{ padding: "34px 40px", display: "flex", flexDirection: "column", gap: 22 }}>
          {items.map(([txt, at]) => (
            <div key={txt} style={{ display: "flex", alignItems: "center", gap: 22, opacity: 0.35 + 0.65 * ramp(t, at, 0.2) }}>
              <Check size={54} draw={ramp(t, at, 0.35)} />
              <span style={{ fontFamily: TITULO, fontWeight: 800, fontSize: 40, color: MARCA.tinta }}>{txt}</span>
            </div>
          ))}
        </Caja>
      </div>
    </Tramo>
  );
};

/** CTA final: síguenos (el botón cambia a «Siguiendo») + comenta la palabra (se escribe sola). */
export const Cta: React.FC = () => {
  const t = useT();
  const at = 13.7;
  if (t < at) return null;
  const sigue = t >= at + 0.7;
  return (
    <div style={{ position: "absolute", left: PIERNAS.left, top: PIERNAS.top + 20, width: PIERNAS.w }}>
      <Pop at={at} y={40} from={0.8}>
        <Caja style={{ padding: "30px 36px", display: "flex", flexDirection: "column", gap: 24 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 20, fontFamily: TITULO, fontWeight: 800, fontSize: 38, color: MARCA.tinta }}>
            <span style={{ color: MARCA.acento }}>1</span> Síguenos {MARCA.usuario}
            <span
              style={{
                marginLeft: "auto",
                fontSize: 28,
                padding: "10px 24px",
                borderRadius: 14,
                background: sigue ? "#EFEFEF" : "#0095F6",
                color: sigue ? MARCA.tinta : "#fff",
                transform: `scale(${golpe(t, at + 0.7)})`,
              }}
            >
              {sigue ? "Siguiendo" : "Seguir"}
            </span>
          </div>
          <div style={{ fontFamily: TITULO, fontWeight: 800, fontSize: 38, color: MARCA.tinta }}>
            <span style={{ color: MARCA.acento }}>2</span> Comenta <Typed texto={MARCA.palabraCta} a={at + 0.9} b={at + 1.2} style={{ color: MARCA.oscuro }} />
          </div>
        </Caja>
      </Pop>
    </div>
  );
};
