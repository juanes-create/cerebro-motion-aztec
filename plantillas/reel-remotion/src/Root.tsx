import React from "react";
import { Composition } from "remotion";
import CONFIG from "./datos/config.json";
import { Reel } from "./Reel";

// La duración sale de datos/config.json, que escribe ./preparar.sh con los cuadros exactos de tu video.
export const RemotionRoot: React.FC = () => (
  <Composition id="Reel" component={Reel} durationInFrames={CONFIG.cuadros} fps={CONFIG.fps} width={1080} height={1920} />
);
