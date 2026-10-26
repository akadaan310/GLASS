#include "../core/glass_gate.h"
#include <dlfcn.h>
#include <cassert>
#include <iostream>
#include <string_view>
int main(int argc,char** argv){
  assert(argc==2);
  void* handle=dlopen(argv[1],RTLD_NOW|RTLD_LOCAL);assert(handle);
  auto entry=reinterpret_cast<glass_gate_entry_fn>(dlsym(handle,"glass_gate_entry"));assert(entry);
  const auto* g=entry();assert(g&&g->abi_version==GLASS_GATE_ABI);
  assert(std::string_view(g->id)=="glass.bitdiff.1");
  const uint8_t in[]={0b1110,0b1000};uint8_t out[3]{};size_t written=0;
  assert(g->invoke(in,2,out,3,&written)==0&&written==3&&out[2]==2);
  assert(g->invoke(in,2,out,2,&written)==-1);
  assert(dlclose(handle)==0);
  std::cout<<"PASS GLASS approved shared-object gate ABI and bit delta fixture\n";
}
