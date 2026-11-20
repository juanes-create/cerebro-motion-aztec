// Texto de cada PNG de una carpeta, línea por línea con su caja (Vision). Sirve para censurar datos y para
// ubicar botones de una grabación de pantalla real.
// Uso: ocr <carpeta> <salida.json>  →  [{"file", "lines": [[texto, x, y_arriba, ancho, alto]]}]
import Vision
import AppKit
import Foundation
let a = CommandLine.arguments
guard a.count >= 3 else { print("uso: ocr <carpeta> <salida.json>"); exit(1) }
let files = try! FileManager.default.contentsOfDirectory(atPath: a[1]).filter { $0.hasSuffix(".png") }.sorted()
var out: [[String: Any]] = []
for f in files {
  let req = VNRecognizeTextRequest()
  req.recognitionLevel = .accurate
  req.recognitionLanguages = ["es-ES", "en-US"]
  req.usesLanguageCorrection = false
  try? VNImageRequestHandler(url: URL(fileURLWithPath: a[1] + "/" + f), options: [:]).perform([req])
  var lines: [[Any]] = []
  for r in (req.results ?? []) {
    guard let c = r.topCandidates(1).first else { continue }
    let b = r.boundingBox
    lines.append([c.string, Double(b.minX), Double(1 - b.maxY), Double(b.width), Double(b.height)])
  }
  out.append(["file": f, "lines": lines])
}
try! JSONSerialization.data(withJSONObject: out).write(to: URL(fileURLWithPath: a[2]))
print("ocr:", files.count, "cuadros")
