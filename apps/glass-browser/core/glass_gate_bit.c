#include "glass_gate.h"
/* Exemplar finite plugin: reports per-byte bit difference; no I/O, eval, or process start. */
static int invoke(const uint8_t *input,size_t n,uint8_t *output,size_t capacity,size_t *written){
  if(!input||!output||!written||n!=2||capacity<3)return -1;
  uint8_t d=(uint8_t)(input[0]^input[1]);unsigned changes=0;
  for(unsigned i=0;i<8;i++)changes+=(d>>i)&1u;
  output[0]=input[0];output[1]=input[1];output[2]=(uint8_t)changes;
  *written=3;return 0;
}
static const glass_gate_v1 gate={GLASS_GATE_ABI,"glass.bitdiff.1","pure-bit-difference",invoke};
#ifdef _WIN32
__declspec(dllexport)
#endif
const glass_gate_v1 *glass_gate_entry(void){return &gate;}
