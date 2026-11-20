// Apertura de la boca de cada cara en cada PNG de una carpeta (Vision, labios internos).
// Uso: bocas <carpeta> <salida.json>  →  [{"frame": n, "faces": [[centro_x, centro_y, alto_cara, apertura]]}]
import Vision
import AppKit
import Foundation
let a = CommandLine.arguments
guard a.count >= 3 else { print("uso: bocas <carpeta> <salida.json>"); exit(1) }
let files = try! FileManager.default.contentsOfDirectory(atPath: a[1]).filter { $0.hasSuffix(".png") }.sorted()
var out: [[String: Any]] = []
for (i, f) in files.enumerated() {
  let req = VNDetectFaceLandmarksRequest()
  try? VNImageRequestHandler(url: URL(fileURLWithPath: a[1] + "/" + f), options: [:]).perform([req])
  var faces: [[Double]] = []
  for r in (req.results ?? []) {
    let b = r.boundingBox
    var abre = -1.0
    if let labios = r.landmarks?.innerLips {
      let ys = labios.normalizedPoints.map { Double($0.y) }
      if let mx = ys.max(), let mn = ys.min() { abre = (mx - mn) * Double(b.height) }
    }
    faces.append([Double(b.midX), Double(1 - b.midY), Double(b.height), abre])
  }
  out.append(["frame": i, "faces": faces])
}
try! JSONSerialization.data(withJSONObject: out).write(to: URL(fileURLWithPath: a[2]))
print("bocas:", files.count, "cuadros")
