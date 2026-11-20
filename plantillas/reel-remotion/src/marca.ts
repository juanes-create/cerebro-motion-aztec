import { loadFont as cargarJakarta } from "@remotion/google-fonts/PlusJakartaSans";
import { loadFont as cargarInter } from "@remotion/google-fonts/Inter";

// ── Tu marca. Cambia estos valores con los de MARCA.md (por defecto, la paleta Aztec Lab).
export const MARCA = {
  crema: "#FBF2EC", // fondo de paneles
  acento: "#6EDD62", // verde de acento (ola, clics, checks)
  claro: "#A9EBA2", // palabra activa, detalles
  oscuro: "#0D3326", // píldoras y textos fuertes
  tinta: "#1F1E1C", // texto normal
  gris: "#6B706C", // texto secundario
  linea: "#E7E2DC",
  rojo: "#E5484D",
  blanco: "#FFFFFF",
  usuario: "@aztec.lab", // tu cuenta, para el CTA
  palabraCta: "GUIA", // la palabra que la gente comenta
};

// Títulos en Plus Jakarta Sans 800 y textos en Inter (Google Fonts, licencia OFL).
// loadFont bloquea el render hasta que la fuente carga: así nada se mide con la fuente de respaldo.
export const TITULO = cargarJakarta("normal", { weights: ["700", "800"], subsets: ["latin", "latin-ext"] }).fontFamily;
export const TEXTO = cargarInter("normal", { weights: ["400", "500", "700"], subsets: ["latin", "latin-ext"] }).fontFamily;

export const SOMBRA = "0 24px 60px rgba(0,0,0,0.30), 0 6px 16px rgba(0,0,0,0.18)";
