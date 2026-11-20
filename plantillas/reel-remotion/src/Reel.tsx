import React from "react";
import { AbsoluteFill, OffthreadVideo, staticFile } from "remotion";
import CONFIG from "./datos/config.json";
import { Cta, Demo, Gancho, Lista } from "./escenas";
import { useT } from "./kit";
import { TEXTO } from "./marca";
import { bajada, Cursor, Panel } from "./ui";

/** Sin video todavía: un fondo de prueba para poder ver el motion. ./preparar.sh pone el tuyo. */
const SinVideo: React.FC = () => (
  <AbsoluteFill style={{ background: "linear-gradient(180deg,#3b3f3c,#1d201e)", alignItems: "center", justifyContent: "center" }}>
    <div style={{ width: 380, height: 480, borderRadius: "48% 48% 40% 40%", background: "rgba(255,255,255,0.07)", marginTop: 220 }} />
    <div style={{ position: "absolute", top: 1180, fontFamily: TEXTO, fontSize: 30, color: "rgba(255,255,255,0.35)" }}>(aquí va tu video: ./preparar.sh VIDEO)</div>
  </AbsoluteFill>
);

export const Reel: React.FC = () => {
  const t = useT();
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <AbsoluteFill style={{ transform: `translateY(${bajada(t)}px)` }}>
        {CONFIG.video ? (
          // maxWidth "none": si un CSS global pone max-width:100% a <video>, el video sale encogido o negro
          <OffthreadVideo src={staticFile("video/bruto.mp4")} muted style={{ width: 1080, height: 1920, maxWidth: "none" }} />
        ) : (
          <SinVideo />
        )}
      </AbsoluteFill>
      <Gancho />
      <Lista />
      <Cta />
      <Panel>
        <Demo />
      </Panel>
      <Cursor />
    </AbsoluteFill>
  );
};
