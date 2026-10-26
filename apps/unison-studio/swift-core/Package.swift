// swift-tools-version: 6.0
import PackageDescription
let package = Package(
    name: "GlassUnisonCore",
    platforms: [.macOS(.v13),.iOS(.v16)],
    products: [.library(name: "UnisonCore", targets: ["UnisonCore"])],
    targets: [.target(name: "UnisonCore"), .testTarget(name:"UnisonCoreTests",dependencies:["UnisonCore"])]
)
