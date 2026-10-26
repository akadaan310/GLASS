#include "encycled.hpp"
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
using glass::encycled::Machine;
using glass::encycled::Cause;
int main(int argc,char** argv){
 try{
  if(argc>1 && std::string(argv[1])=="help"){
    std::cout<<"Usage: enCycled [trace] | [help]. Fixed deterministic, synthetic control trace.\n";return 0;
  }
  if(argc>1 && std::string(argv[1])!="trace") throw std::invalid_argument("unsupported command");
  Machine m(4);
  m.open("world-session");
  for(auto next:{0b1000,0b1100,0b1110,0b1000}){m.advance(1);m.write_word(next,Cause::clock_edge);}
  m.close("world-session");
  if(m.replay()!=m.word()) throw std::logic_error("replay mismatch");
  std::cout<<"{\"schema\":\"glass.encycled.trace/0.1\",\"model\":\"synthetic-bit-control\",\"tick\":"<<m.tick()
    <<",\"word\":"<<m.word()<<",\"verified_replay\":true,\"duration\":"<<*m.duration("world-session")<<",\"events\":[";
  bool first=true;
  for(auto& e:m.events()){
    if(!first) std::cout<<",";
    first=false;
    std::cout<<"{\"seq\":"<<e.sequence<<",\"tick\":"<<e.tick<<",\"tx\":"<<e.transaction<<",\"bit\":"<<e.bit
      <<",\"before\":"<<(e.before?1:0)<<",\"after\":"<<(e.after?1:0)<<",\"cause\":\""<<glass::encycled::name(e.cause)<<"\"}";
  }
  std::cout<<"]}\n";
  return 0;
 }catch(const std::exception& e){std::cerr<<"enCycled refusal: "<<e.what()<<"\n";return 2;}
}
