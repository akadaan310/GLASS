#include "unison.hpp"
#include "sha256.hpp"
#include <cassert>
#include <cmath>
#include <fstream>
#include <iostream>
#include <sstream>
using namespace glass;
int main(){
 int checks=0;
 auto check=[&](bool x,const char* name){if(!x){std::cerr<<"FAIL "<<name<<"\n";std::exit(1);}checks++;std::cout<<"PASS "<<name<<"\n";};
 check(sha256("")=="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","sha256 empty");
 check(sha256("abc")=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad","sha256 abc");
 check(Engine::bit_gate(0,1,"xor")==1 && Engine::bit_gate(3,1,"and")==1 && Engine::bit_gate(3,1,"or")==3,"binary gates");
 check(Engine::bit_gate(0x80000000,1,"rot")==1,"bit rotation");
 check(Engine::encode_uri("ج ⊗") == "%D8%AC%20%E2%8A%97","URL Unicode percent encoding");
 check(Engine::path10("row").size()==100 && Engine::path10("column")[1]==10,"row and column tapes");
 check(Engine::path10("diagonal").size()==10 && Engine::path10("anti-diagonal").back()==90,"diagonal paths");
 check(Engine::path10("perimeter").size()==36&&Engine::path10("snake").size()==100,"geometric paths");
 std::array<int32_t,100>a{},I{};for(int i=0;i<100;i++){a[i]=i%17;I[i]=(i%11==0)?1:0;}auto m=Engine::multiply10(a,I);
 check(m.values==a && m.trace.size()==1000,"10x10 exact multiply witness");
 check(m.trace[0].row==0&&m.trace[0].col==0&&m.trace[0].k==0,"MAC order preserved");
 Engine e;check(e.verify() && e.tick()==0,"genesis and clock");
 auto b=e.dispatch("xor 0x2 0x3");check(b.accepted&&b.detail.find("0x1")!=std::string::npos,"English opcode parsing");
 auto g=e.dispatch("⟦Λ:binary ⊗ Γ:xor(1,0) ⊗ τ:1⟧");check(g.accepted&&g.detail.find("0x1")!=std::string::npos,"Unison symbolic parsing");
 auto z=e.dispatch("halt clock");uint64_t stopped=e.tick();e.render_step();e.render_step();check(e.is_halted()&&e.tick()==stopped,"clock stop independent of display");
 check(!e.dispatch("xor 1 0").accepted&&e.tick()==stopped,"HALT guard");
 check(e.dispatch("resume").accepted && !e.is_halted(),"RESUME guard");
 check(e.dispatch("space 6").accepted && e.space.coordinates.size()==6,"N dimensional allocation");
 check(e.dispatch("move 0 2.0").accepted,"dimension translate");
 double before=e.space.radius();check(e.dispatch("spin 0 1 1.5707963267948966").accepted&&std::fabs(e.space.radius()-before)<1e-8,"rotation preserves norm");
 check(!e.dispatch("spin 0 0 3").accepted,"invalid plane denied");
 check(e.dispatch("multiply matrices").detail.find("PASS")!=std::string::npos,"natural language matrix");
 check(e.dispatch("energy 0 15").detail.find("4 bit")!=std::string::npos,"heat is switching proxy");
 check(e.dispatch("مرحبا").detail.find("UNKNOWN SEMANTICS")!=std::string::npos,"unmapped input never pretends understanding");
 check(e.dispatch("url Λ").detail.find("%CE%9B")!=std::string::npos,"sterile URL generation");
 check(e.verify(),"SHA chained provenance");
 Engine autonomous;auto initialTick=autonomous.tick();for(int i=0;i<24;i++)autonomous.render_step();
 check(autonomous.tick()==initialTick+1&&autonomous.events().back().kind=="GENERATOR_STEP","autonomous oracle transition");
 autonomous.dispatch("halt");auto haltTick=autonomous.tick();for(int i=0;i<48;i++)autonomous.render_step();
 check(autonomous.tick()==haltTick,"autonomous transition obeys HALT");
 check(NDim{{0,0,0}}.radius()==0.,"Euclidean origin norm");
 std::cout<<"ALL "<<checks<<" tests passed\n";
}
