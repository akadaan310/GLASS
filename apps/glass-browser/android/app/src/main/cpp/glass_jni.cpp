#include <jni.h>
#include <chrono>
#include <exception>
#include <string>
#include "../../../../../core/glass_core.hpp"

namespace {
glass::native::Ledger ledger;
std::string read(JNIEnv* env,jstring s) {
  if(!s)return {};
  const char* data=env->GetStringUTFChars(s,nullptr);
  if(!data)throw std::runtime_error("Java string could not be read");
  std::string value(data);
  env->ReleaseStringUTFChars(s,data);
  return value;
}
jstring answer(JNIEnv* env,const std::string& s) {return env->NewStringUTF(s.c_str());}
uint64_t monotonic(jlong t){if(t<0)throw std::invalid_argument("negative clock");return static_cast<uint64_t>(t);}
std::string error(const std::exception &e){return "{\"error\":"+glass::native::quote(e.what())+"}";}
}
extern "C" JNIEXPORT jstring JNICALL
Java_org_glass_nativebrowser_Bridge_nativeEvent(JNIEnv* env,jclass,jstring kind,jstring origin,jstring detail,jlong t){
  try{return answer(env,glass::native::Ledger::json(ledger.append(read(env,kind),read(env,origin),read(env,detail),monotonic(t))));}
  catch(const std::exception& e){return answer(env,error(e));}
}
extern "C" JNIEXPORT jstring JNICALL
Java_org_glass_nativebrowser_Bridge_nativeTransition(JNIEnv* env,jclass,jint op,jstring reason,jlong t){
  try{
    if(op==0) ledger.requestAgain(monotonic(t));
    else if(op==1) ledger.approved(monotonic(t));
    else if(op==2) ledger.refused(monotonic(t));
    else if(op==3) ledger.stopped(read(env,reason),monotonic(t));
    else throw std::invalid_argument("transition not admitted");
    return answer(env,ledger.status());
  }catch(const std::exception& e){return answer(env,error(e));}
}
extern "C" JNIEXPORT jstring JNICALL
Java_org_glass_nativebrowser_Bridge_nativeStatus(JNIEnv* env,jclass){return answer(env,ledger.status());}
extern "C" JNIEXPORT jstring JNICALL
Java_org_glass_nativebrowser_Bridge_nativeTerminal(JNIEnv* env,jclass,jstring url){
  try{return answer(env,glass::native::route(read(env,url),ledger));}
  catch(const std::exception& e){return answer(env,error(e));}
}
