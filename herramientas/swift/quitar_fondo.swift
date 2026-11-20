// Quita el fondo de cualquier foto (persona, producto, objeto, monumento) con Vision de macOS 14+. Local y gratis.
// Uso: quitar_fondo <entrada> <salida.png> [--recortar]   (--recortar: ajusta el PNG al borde del objeto)
import Foundation
import Vision
import CoreImage
import AppKit
let a = CommandLine.arguments
guard a.count >= 3 else { print("uso: quitar_fondo <entrada> <salida.png> [--recortar]"); exit(1) }
let handler = VNImageRequestHandler(url: URL(fileURLWithPath: a[1]), options: [:])
let req = VNGenerateForegroundInstanceMaskRequest()
do { try handler.perform([req]) } catch { print("error de Vision:", error); exit(2) }
guard let obs = req.results?.first else { print("no encontré un objeto principal en la foto"); exit(3) }
do {
  let buf = try obs.generateMaskedImage(ofInstances: obs.allInstances, from: handler, croppedToInstancesExtent: a.contains("--recortar"))
  let ci = CIImage(cvPixelBuffer: buf)
  guard let cg = CIContext().createCGImage(ci, from: ci.extent) else { print("no se pudo crear la imagen"); exit(4) }
  try NSBitmapImageRep(cgImage: cg).representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: a[2]))
  print("listo:", a[2], Int(ci.extent.width), "x", Int(ci.extent.height))
} catch { print("error:", error); exit(5) }
