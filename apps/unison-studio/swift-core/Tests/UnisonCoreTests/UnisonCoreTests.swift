import XCTest
@testable import UnisonCore

final class UnisonCoreTests: XCTestCase {
    func testClockReplay() throws {
        var machine=PureMachine()
        XCTAssertEqual(try machine.apply("INCREMENT",4),5)
        XCTAssertEqual(try machine.apply("SIGN",-7),-1)
        XCTAssertEqual(try machine.replay(),[5,-1])
        XCTAssertEqual(machine.logicalTick,2)
        XCTAssertEqual(machine.events.first?.sequence,1)
    }
    func testRefusalIsAtomic() throws {
        var machine=PureMachine()
        XCTAssertThrowsError(try machine.apply("SPAWN_PROCESS",3))
        XCTAssertEqual(machine.events.count,0)
        XCTAssertEqual(machine.logicalTick,0)
        XCTAssertThrowsError(try machine.apply("INCREMENT",Int64.max))
        XCTAssertEqual(machine.events.count,0)
    }
    func testFactory() throws {
        let recipe = try GeneratorRecipe(identifier:"g.increment",operatorName:"INCREMENT",sourceSha256:String(repeating:"a",count:64),maxEvaluations:3)
        XCTAssertEqual(try GeneratorFactory().generate(recipe,for:[0,2,5]),[1,3,6])
        XCTAssertThrowsError(try GeneratorFactory().generate(recipe,for:[0,2,5,7]))
    }
    func testSyntaxShape() throws {
        let a=SyntaxNode(id:"n0000",kind:"Module",label:"",parent:nil,span:nil,language:"python")
        let b=SyntaxNode(id:"n0001",kind:"FunctionDef",label:"f",parent:"n0000",span:"1:1",language:"python")
        let data=SyntaxModule(schema:"glass.unison-ir/0.1",language:"python",nodes:[a,b])
        try data.checkShape()
        let invalid=SyntaxModule(schema:data.schema,language:data.language,nodes:[b,a])
        XCTAssertThrowsError(try invalid.checkShape())
    }
}
