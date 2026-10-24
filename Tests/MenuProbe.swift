import AppKit
import ApplicationServices
func value(_ el: AXUIElement, _ key: String) -> CFTypeRef? {
 var v: CFTypeRef?; return AXUIElementCopyAttributeValue(el, key as CFString, &v) == .success ? v : nil
}
func children(_ el: AXUIElement) -> [AXUIElement] { value(el, "AXChildren") as? [AXUIElement] ?? [] }
func dump(_ el: AXUIElement, _ depth: Int = 0) {
 var actions: CFArray?; AXUIElementCopyActionNames(el, &actions)
 print(String(repeating: " ", count: depth), value(el, "AXRole") as? String ?? "?", value(el, "AXTitle") as? String ?? "", value(el, "AXDescription") as? String ?? "", "actions=", actions as Any)
 if depth < 5 { for c in children(el) { dump(c, depth+1) } }
}
guard let app = NSRunningApplication.runningApplications(withBundleIdentifier: "br.com.luizfilipe.modo-desenvolvedor").first else { fatalError("app absent") }
let ax = AXUIElementCreateApplication(app.processIdentifier)
AXUIElementSetMessagingTimeout(ax, 3)
guard let raw = value(ax, "AXExtrasMenuBar") else { fatalError("bar absent") }
let bar = raw as! AXUIElement
if CommandLine.arguments.contains("--open"), let button = children(bar).first {
 print("OPEN:", AXUIElementPerformAction(button, "AXPress" as CFString).rawValue)
}
if CommandLine.arguments.contains("--activate") || CommandLine.arguments.contains("--quit") {
 let wantedTitle = CommandLine.arguments.contains("--quit") ? "Sair" : "Ativar Modo Desenvolvedor"
 func find(_ el: AXUIElement, _ depth: Int = 0) -> AXUIElement? {
  if value(el, "AXTitle") as? String == wantedTitle { return el }
  if depth < 6 { for child in children(el) { if let result = find(child, depth+1) { return result } } }
  return nil
 }
 guard let command = find(bar) else { fatalError("Menu command absent: open the menu first") }
 print("ACTIVATE real NSMenuItem AXPress:", AXUIElementPerformAction(command, "AXPress" as CFString).rawValue)
}
dump(bar)
