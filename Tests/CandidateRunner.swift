import AppKit

// Diagnostic only: exercises the actual layout engine without replacing the installed app.
@main struct CandidateRunner {
    @MainActor static func main() {
        let app = NSApplication.shared
        app.setActivationPolicy(.accessory)
        Task { @MainActor in
            do {
                let engine = LayoutEngine()
                if CommandLine.arguments.contains("--inspect") { printJSON(try engine.inspect(verify: false)); exit(0) }
                let report = try await engine.run()
                printJSON(report)
                exit(0)
            } catch { print(error.localizedDescription); exit(1) }
        }
        app.run()
    }
}
