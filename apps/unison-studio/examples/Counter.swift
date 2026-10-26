import Foundation
struct TelemetryClock {
    var tick: UInt64 = 0
    mutating func step() { tick += 1 }
}
let clock = TelemetryClock()
