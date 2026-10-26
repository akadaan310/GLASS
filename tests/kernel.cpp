#include "../runtime/glass.hpp"
#include <cassert>
#include <filesystem>
#include <iostream>
#include <unistd.h>
using namespace glass;
template<class F> void refuses(F f){ bool caught=false; try{f();}catch(const std::exception&){caught=true;} assert(caught); }
int main(){
 Machine m;
 m.apply({"region","corpus","acquired"});
 m.apply({"region","publication","queued"});
 m.apply({"rule","r1","corpus","acquired","mapped","mapped"});
 m.apply({"rule","r2","publication","queued","mapped","ready"});
 refuses([&]{m.apply({"outcome","i1","mapped","artifact","rationale"});});
 refuses([&]{m.apply({"intent","bad","unknown","source","adapter","inspect","retain frontier"});});
 m.apply({"intent","i1","mapped","source","adapter","source-bound mapping","retain frontier"});
 refuses([&]{m.apply({"outcome","i1","other","artifact","rationale"});});
 m.apply({"outcome","i1","mapped","artifact","read source then map"});
 assert(m.active.at("corpus")=="mapped");
 assert(m.active.at("publication")=="ready");
 refuses([&]{m.apply({"outcome","i1","mapped","artifact","duplicate"});});
 assert(m.weight().find("mapped")!=std::string::npos);
 auto p=std::filesystem::temp_directory_path()/("glass-test-"+std::to_string(getpid()));
 {
 Journal j(p); j.submit({"region","x","a"},0);
 refuses([&]{j.submit({"region","y","b"},0);});
 j.submit({"rule","a1","x","a","go","b"},1);
 j.submit({"intent","ii","go","src","adapter","choice","retain frontier"},2);
 j.submit({"outcome","ii","go","artifact","observed"},3);
 }
 {Journal j(p); assert(j.cursor()==4); assert(j.machine.active.at("x")=="b");}
 {std::ofstream f(p,std::ios::app); f<<"5\tpartial";}
 refuses([&]{Journal j(p);});
 std::filesystem::remove(p);
 auto trace=spell("IN");
 assert(trace.find("01001001")!=std::string::npos);
 assert(trace.find("01001110")!=std::string::npos);
 assert(trace.find("\"first_changed_bit\":6")!=std::string::npos);
 std::cout<<"PASS concurrent reactions, pre-intents, declared events, duplicate outcomes, replay, stale cursor, torn tail, spelling trace\n";
}
