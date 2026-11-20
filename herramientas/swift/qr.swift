// Lee el QR en cada PNG de una carpeta (cuadros a 10 por segundo) y dice desde qué segundo se puede escanear.
// Uso: qr <carpeta> [fps=10]
import Vision
import AppKit
let a = CommandLine.arguments
guard a.count >= 2 else { print("uso: qr <carpeta> [fps]"); exit(1) }
let fps = a.count > 2 ? Double(a[2]) ?? 10 : 10
let files = try! FileManager.default.contentsOfDirectory(atPath: a[1]).filter { $0.hasSuffix(".png") }.sorted()
var ok: [Int] = []
var texto = ""
for (i, f) in files.enumerated() {
  guard let img = NSImage(contentsOfFile: a[1] + "/" + f), let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { continue }
  let req = VNDetectBarcodesRequest()
  req.symbologies = [.qr]
  try? VNImageRequestHandler(cgImage: cg).perform([req])
  if let s = (req.results ?? []).compactMap({ $0.payloadStringValue }).first { ok.append(i); texto = s }
}
let pct = files.isEmpty ? 0 : 100 * ok.count / files.count
print("QR legible en \(ok.count) de \(files.count) cuadros (\(pct) %)")
if let p = ok.first, let u = ok.last { print(String(format: "desde %.1f s hasta %.1f s · lleva a: %@", Double(p) / fps, Double(u) / fps, texto)) }
