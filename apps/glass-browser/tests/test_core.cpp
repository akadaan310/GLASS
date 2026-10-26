#include "../core/glass_core.hpp"
#include <cassert>
#include <iostream>
using namespace glass::native;
int main(){
 Ledger l(3);
 l.consentRequested(1);l.refused(2);assert(l.status().find("DENIED_GAP")!=std::string::npos);
 l.requestAgain(3);l.approved(4);assert(l.status().find("CAPTURING")!=std::string::npos);
 auto e=l.append("NAVIGATION","browser","example.com",5);assert(e.sequence==5&&e.epoch==1);
 assert(l.evicted()==2);
 l.stopped("screen_locked",6);assert(l.status().find("STOPPED_GAP")!=std::string::npos);
 bool refused=false;try{l.append("X","x","",5);}catch(const std::invalid_argument&){refused=true;}assert(refused);
 auto x=spell("أجد");assert(x.find("MIXED")!=std::string::npos);assert(x.find("\"native_sum\":8")!=std::string::npos);
 auto y=spell("قط");assert(y.find("109")!=std::string::npos);
 assert(route("glass://terminal/v1/state",l).find("ledger")!=std::string::npos);
 assert(route("glass://terminal/v1/spell?word=%D9%82%D8%B7",l).find("109")!=std::string::npos);
 refused=false;try{route("glass://terminal/v1/fetch?url=http://localhost",l);}catch(const std::invalid_argument&){refused=true;}assert(refused);
 const uint8_t elf[]={0x7f,'E','L','F'};assert(identify(elf,4)==BinaryKind::elf);
 uint8_t pe[72]={};pe[0]='M';pe[1]='Z';pe[0x3c]=64;pe[64]='P';pe[65]='E';assert(identify(pe,72)==BinaryKind::pe);
 const uint8_t pdf[]={'%','P','D','F'};assert(identify(pdf,4)==BinaryKind::unknown);
 assert(registry.size()==28);
 std::cout<<"PASS GLASS browser native core: capture gates, epochs, Arabic signature, read-only terminal, PE/ELF, bounded retention\n";
}
