// Caras en cada PNG de una carpeta (Vision de macOS, local y gratis).
// Uso: caras <carpeta> <salida.json>  →  [{"frame": n, "faces": [[x, y_arriba, ancho, alto, confianza, giro]]}]  (normalizado, origen arriba-izquierda)
import Vision
import AppKit
import Foundation
let a = CommandLine.arguments
guard a.count >= 3 else { print("uso: caras <carpeta> <salida.json>"); exit(1) }
let files = try! FileManager.default.contentsOfDirectory(atPath: a[1]).filter { $0.hasSuffix(".png") }.sorted()
var out: [[String: Any]] = []
for (i, f) in files.enumerated() {
  let req = VNDetectFaceRectanglesRequest()
  req.revision = VNDetectFaceRectanglesRequestRevision3
  try? VNImageRequestHandler(url: URL(fileURLWithPath: a[1] + "/" + f), options: [:]).perform([req])
  var faces: [[Double]] = []
  for r in (req.results ?? []) {
    let b = r.boundingBox
    faces.append([Double(b.minX), Double(1 - b.maxY), Double(b.width), Double(b.height), Double(r.confidence), Double(r.roll?.doubleValue ?? 0)])
  }
  out.append(["frame": i, "faces": faces])
}
try! JSONSerialization.data(withJSONObject: out).write(to: URL(fileURLWithPath: a[2]))
print("caras:", files.count, "cuadros")
