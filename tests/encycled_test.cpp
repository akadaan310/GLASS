#include "../runtime/encycled.hpp"
#include <cassert>
#include <cmath>
#include <iostream>
#include <stdexcept>
using glass::encycled::Machine;
using glass::encycled::Cause;
int main(){
 Machine m(4);
 m.open("object-1");
 m.advance(); m.write_word(0b1000,Cause::clock_edge);
 m.advance(); m.write_word(0b1100,Cause::clock_edge);
 m.advance(); m.write_word(0b1110,Cause::clock_edge);
 m.advance(); m.write_word(0b1000,Cause::recovery);
 assert(m.word()==0b1000);
 assert(m.replay()==m.word());
 assert(m.events().size()==5);
 assert(m.events()[3].transaction==m.events()[4].transaction);
 m.close("object-1");
 assert(*m.duration("object-1")==4);
 bool refused=false;
 try{m.close("object-1");}catch(const std::invalid_argument&){refused=true;}
 assert(refused);
 refused=false;
 try{m.write_bit(4,true);}catch(const std::out_of_range&){refused=true;}
 assert(refused);
 refused=false;
 try{m.advance(0);}catch(const std::invalid_argument&){refused=true;}
 assert(refused);
 assert(std::abs(glass::encycled::integrate_step({{0,0},{1,1},{3,0}},4)-2.0)<1e-12);
 assert(std::abs(glass::encycled::cycle_residual(2.5,0.3,0.4)-1.0)<1e-12);
 Machine capped(4,1);capped.write_word(0b0001);
 refused=false;
 try{capped.write_word(0b1111);}catch(const std::length_error&){refused=true;}
 assert(refused && capped.word()==1 && capped.events().size()==1);
 std::cout<<"PASS enCycled/0.1 native fixture: trace, replay, lifetimes, integration, guards\n";
}
