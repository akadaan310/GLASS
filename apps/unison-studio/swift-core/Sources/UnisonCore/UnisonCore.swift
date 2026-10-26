// GLASS Unison portable semantics: does not import SwiftUI/UIKit/Android ART.
// Swift Android SDK target is a future build gate, not inferred from Linux conformance.
import Foundation

public enum UnisonError: Error, Equatable {
    case unsupportedKind
    case resourceBudget
    case missingIdentity
    case invalidValue
    case missingCapability
}

public struct SyntaxNode: Codable, Sendable, Equatable {
    public var id: String
    public var kind: String
    public var label: String
    public var parent: String?
    public var span: String?
    public var language: String
}

public struct SyntaxModule: Codable, Sendable {
    public var schema: String
    public var language: String
    public var nodes: [SyntaxNode]

    public func checkShape() throws {
        guard schema == "glass.unison-ir/0.1", nodes.count <= 640 else {throw UnisonError.resourceBudget}
        var seen = Set<String>()
        for node in nodes {
            if seen.contains(node.id) {throw UnisonError.invalidValue}
            if let parent = node.parent, !seen.contains(parent) {throw UnisonError.missingIdentity}
            seen.insert(node.id)
        }
    }
}

public struct ClockEvent: Sendable, Equatable {
    public let sequence: UInt64
    public let tick: UInt64
    public let operation: String
    public let input: Int64
    public let output: Int64
}

public struct PureMachine: Sendable {
    public private(set) var logicalTick: UInt64 = 0
    public private(set) var events: [ClockEvent] = []
    public var budget: Int = 4096

    public init() {}

    public mutating func apply(_ operation: String, _ value: Int64) throws -> Int64 {
        guard events.count < budget && logicalTick < UInt64.max else {throw UnisonError.resourceBudget}
        let output: Int64
        switch operation {
        case "IDENTITY": output=value
        case "INCREMENT":
            let (next, overflow)=value.addingReportingOverflow(1)
            guard !overflow else {throw UnisonError.invalidValue}
            output=next
        case "SIGN": output=value>0 ? 1 : value<0 ? -1 : 0
        default: throw UnisonError.unsupportedKind
        }
        logicalTick += 1
        events.append(ClockEvent(sequence:UInt64(events.count+1), tick:logicalTick,
                                 operation:operation,input:value,output:output))
        return output
    }

    public func replay() throws -> [Int64] {
        var second = PureMachine()
        second.budget = budget
        return try events.map { original in
            let result = try second.apply(original.operation,original.input)
            guard result == original.output, second.events.last == original else {
                throw UnisonError.invalidValue
            }
            return result
        }
    }
}

public struct GeneratorRecipe: Sendable, Equatable {
    public let identifier: String
    public let operatorName: String
    public let sourceSha256: String
    public let effects: [String]
    public let maxEvaluations: Int

    public init(identifier: String, operatorName: String, sourceSha256: String, maxEvaluations: Int = 100) throws {
        guard ["IDENTITY", "INCREMENT", "SIGN"].contains(operatorName) else {throw UnisonError.unsupportedKind}
        guard (1...4096).contains(maxEvaluations), sourceSha256.count == 64, sourceSha256.allSatisfy({$0.isHexDigit}) else {
            throw UnisonError.resourceBudget
        }
        self.identifier=identifier
        self.operatorName=operatorName
        self.sourceSha256=sourceSha256
        self.maxEvaluations=maxEvaluations
        self.effects=[]
    }
}

public struct GeneratorFactory {
    public init() {}
    public func generate(_ recipe:GeneratorRecipe, for inputs:[Int64]) throws -> [Int64] {
        guard inputs.count<=recipe.maxEvaluations else {throw UnisonError.resourceBudget}
        var machine = PureMachine()
        machine.budget = recipe.maxEvaluations
        let output = try inputs.map { try machine.apply(recipe.operatorName,$0) }
        guard try machine.replay()==output else {throw UnisonError.invalidValue}
        return output
    }
}
