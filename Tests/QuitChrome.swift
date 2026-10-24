import AppKit

// Normal application termination only. Never force-quit or bypass a save dialog.
if let app = NSRunningApplication.runningApplications(withBundleIdentifier: "com.google.Chrome").first {
    guard app.terminate() else { print("Chrome declined normal termination"); exit(1) }
    let deadline = Date().addingTimeInterval(10)
    while !app.isTerminated && Date() < deadline { RunLoop.current.run(until: Date().addingTimeInterval(0.1)) }
    guard app.isTerminated else { print("Chrome still open; no force-quit performed"); exit(1) }
}
assert(NSRunningApplication.runningApplications(withBundleIdentifier: "com.google.Chrome").isEmpty)
print("PASS: Chrome fechado normalmente, sem encerramento forçado")
