// GLASS Unison / 0.1 — localhost-only read-only Swift HTTP server.
// Linux demo. No remote market feed, broker, filesystem upload or user code execution.
import Foundation
import Glibc

struct XorShift32 {
    var state: UInt32
    init(seed: UInt32) { state = seed == 0 ? 1 : seed }
    mutating func next() -> UInt32 {
        var x = state
        x ^= x << 13; x ^= x >> 17; x ^= x << 5
        state = x
        return x
    }
}

let symbols = ["AUR", "ORCA", "SOLA", "NOVA", "VRT", "HELI", "LUM", "ION"]

func marketFixture(seed: UInt32) -> [String: Any] {
    var rng = XorShift32(seed: seed)
    var counts = [String: (previous: Int, recent: Int)]()
    var priceSeries = [String: [[String: Any]]]()
    var totals = [String: Int]()
    for s in symbols { counts[s] = (0,0); priceSeries[s] = []; totals[s] = 0 }
    for tick in 0..<768 {
        let original = Int(rng.next() % UInt32(symbols.count))
        let active = (tick >= 635 && tick < 748 && tick % 5 <= 3) ? 1 : original
        let symbol = symbols[active]
        let basis = Double((rng.next() % 280)) / 40.0
        let vol = Int(rng.next() % 350) + 40
        let price = 94 + Double(original) * 9 + sin(Double(tick) / 24 + Double(active)) * 5 + basis
        totals[symbol, default: 0] += vol
        if tick >= 512 && tick < 640 { counts[symbol,default:(0,0)].previous += 1 }
        if tick >= 640 { counts[symbol,default:(0,0)].recent += 1 }
        if priceSeries[symbol,default:[]].count < 180 && tick >= 588 {
            priceSeries[symbol, default:[]].append(["t":tick,"p":Double((price * 100).rounded())/100,"v":vol])
        }
    }
    let ranking: [[String: Any]] = symbols.map { symbol in
        let c = counts[symbol] ?? (0,0)
        let delta = c.recent - c.previous
        let score = Double(delta)/sqrt(Double(max(1,c.previous)))
        return ["symbol":symbol,"prior_128":c.previous,"latest_128":c.recent,
                "burst_score":Double((score*100).rounded())/100,"synthetic_volume":totals[symbol] ?? 0,
                "series":priceSeries[symbol] ?? []]
    }.sorted {
        let lhs=($0["burst_score"] as? Double ?? 0)
        let rhs=($1["burst_score"] as? Double ?? 0)
        return lhs == rhs ? ($0["symbol"] as? String ?? "") < ($1["symbol"] as? String ?? "") : lhs > rhs
    }
    return ["schema":"glass.unison.market/0.1","origin":"synthetic-xorshift32","seed":seed,
            "event_count":768,"provider":"NONE","orders":0,"ticks_are":"logical indices, not exchange times",
            "interpretation":"retrospective activity anomaly, not future-price forecast", "ranking":ranking]
}

func serialized(_ object: [String: Any]) -> Data {
    return (try? JSONSerialization.data(withJSONObject: object, options: [.sortedKeys, .fragmentsAllowed])) ?? Data("{}".utf8)
}

let project = URL(fileURLWithPath: #filePath).deletingLastPathComponent().deletingLastPathComponent()
let publicRoot = project.appendingPathComponent("public")
let permittedFiles = Set(["/", "/index.html", "/styles.css", "/app.js", "/data/catalog.json",
  "/data/ir-swift.json", "/data/ir-swiftui.json", "/data/ir-web.json",
  "/data/ir-typescript.json", "/data/ir-python.json", "/data/ir-java.json", "/data/unibet.json", "/data/strategy.json"])

func readResource(_ raw: String) -> (Int, String, Data) {
    let urlParts = raw.split(separator: "?", maxSplits: 1, omittingEmptySubsequences: false)
    let path = String(urlParts[0])
    if path == "/api/status" {
        return (200, "application/json", serialized([
          "schema":"glass.unison.status/0.1","mode":"Swift/Linux HTTP", "backend":"Swift 6.2+",
          "source":"Swift compiler syntax and TypeScript/Python/HTML parsers",
          "network":"localhost only", "market":"synthetic", "native_iOS_emulation":false,
          "disclaimer":"read-only research instrumentation; no operating system virtualization"
        ]))
    }
    if path == "/api/market" {
        var seed: UInt32 = 24681357
        if urlParts.count == 2 {
            let query = String(urlParts[1]); let pair = query.split(separator:"=",maxSplits:1)
            if pair.count != 2 || pair[0] != "seed" || UInt32(pair[1]) == nil || UInt32(pair[1]) == 0 {
                return (400,"application/json",serialized(["error":"seed must be an integer in 1..4294967295"]))
            }
            seed = UInt32(pair[1])!
        }
        return (200, "application/json", serialized(marketFixture(seed:seed)))
    }
    guard permittedFiles.contains(path) else {
        return (404,"application/json",serialized(["error":"route not admitted"]))
    }
    let p = publicRoot.appendingPathComponent(path == "/" ? "index.html" : String(path.dropFirst()))
    guard let data = try? Data(contentsOf: p), data.count < 1_000_000 else {
        return (404,"application/json",serialized(["error":"artifact not installed"]))
    }
    let type: String
    if path.hasSuffix(".css") {type="text/css; charset=utf-8"}
    else if path.hasSuffix(".js") {type="application/javascript; charset=utf-8"}
    else if path.hasSuffix(".json") {type="application/json; charset=utf-8"}
    else {type="text/html; charset=utf-8"}
    return (200,type,data)
}

func writeAll(_ client: Int32, data: Data) {
    data.withUnsafeBytes { buffer in
        guard let base=buffer.baseAddress else{return}
        var sent=0
        while sent < buffer.count {
            let n=Glibc.write(client,base.advanced(by:sent),buffer.count-sent)
            if n<=0 {break}
            sent += n
        }
    }
}

func respond(client: Int32) {
    defer{_ = Glibc.close(client)}
    var bytes=[UInt8](repeating:0,count:8192)
    let received=bytes.withUnsafeMutableBytes { ptr in Glibc.read(client,ptr.baseAddress,ptr.count) }
    if received<=0 {return}
    let req=String(decoding:bytes.prefix(Int(received)),as:UTF8.self)
    let parts=req.split(separator:" ",maxSplits:2)
    guard parts.count>=2, parts[0]=="GET",parts[1].count<=300 else {
        let err=serialized(["error":"GET-only, bounded request"])
        let header="HTTP/1.1 405 Method Not Allowed\r\nContent-Type: application/json\r\nContent-Length: \(err.count)\r\nConnection: close\r\n\r\n"
        writeAll(client, data: Data(header.utf8)+err);return
    }
    let (code,mime,data)=readResource(String(parts[1]))
    let description=code==200 ? "OK" : code==400 ? "Bad Request" : "Not Found"
    let header="HTTP/1.1 \(code) \(description)\r\nContent-Type: \(mime)\r\nContent-Length: \(data.count)\r\nCache-Control: no-store\r\nContent-Security-Policy: default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self'; connect-src 'self'; img-src 'self' data:\r\nX-Content-Type-Options: nosniff\r\nConnection: close\r\n\r\n"
    writeAll(client,data:Data(header.utf8)+data)
}

func startServer() {
    let port = Int(CommandLine.arguments.dropFirst().first ?? "8765") ?? 8765
    guard (1024...65535).contains(port) else { fputs("Invalid port\n",stderr);exit(2) }
    let fd=Glibc.socket(AF_INET,Int32(SOCK_STREAM.rawValue),0)
    guard fd>=0 else {fatalError("socket")};defer{_ = Glibc.close(fd)}
    var yes:Int32=1
    _ = setsockopt(fd,SOL_SOCKET,SO_REUSEADDR,&yes,socklen_t(MemoryLayout<Int32>.size))
    var addr=sockaddr_in();addr.sin_family=sa_family_t(AF_INET)
    addr.sin_port=in_port_t(UInt16(port).bigEndian)
    addr.sin_addr=in_addr(s_addr:inet_addr("127.0.0.1"))
    let bindStatus=withUnsafePointer(to:&addr) { p in
        p.withMemoryRebound(to:sockaddr.self,capacity:1){Glibc.bind(fd,$0,socklen_t(MemoryLayout<sockaddr_in>.size))}
    }
    guard bindStatus==0, Glibc.listen(fd,16)==0 else {fputs("Bind failed\n",stderr);exit(2)}
    print("GLASS UNISON Swift engine on http://127.0.0.1:\(port) (GET-only, synthetic data)")
    fflush(stdout)
    while true {
        let client=Glibc.accept(fd,nil,nil)
        if client>=0 {respond(client:client)}
    }
}

startServer()
