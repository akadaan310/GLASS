#include <jni.h>
#include <algorithm>
#include <mutex>
#include <string>
#include <vector>
#include "unison.hpp"
#include "pixels.hpp"
namespace {
struct Session {
  explicit Session(std::string path):engine(std::move(path)){}
  std::mutex mu;
  glass::Engine engine;
  glass::Result recent{true,"OBSERVING","Λ → Ω → Γ → τ → Π → ۞","◉",0};
};
Session* valid(jlong p){return reinterpret_cast<Session*>(p);}
std::string str(JNIEnv* env,jstring text){if(!text)return {};const char* s=env->GetStringUTFChars(text,nullptr);if(!s)return {};std::string out(s);env->ReleaseStringUTFChars(text,s);return out;}
}
extern "C" JNIEXPORT jlong JNICALL Java_com_glass_unison_MainActivity_nativeCreate(JNIEnv* env,jobject,jstring journal){return reinterpret_cast<jlong>(new Session(str(env,journal)));}
extern "C" JNIEXPORT void JNICALL Java_com_glass_unison_MainActivity_nativeRelease(JNIEnv*,jobject,jlong pointer){delete valid(pointer);}
extern "C" JNIEXPORT jstring JNICALL Java_com_glass_unison_MainActivity_nativeDispatch(JNIEnv* env,jobject,jlong pointer,jstring input){
 auto* s=valid(pointer);if(!s)return env->NewStringUTF("NOT INITIALIZED");
 std::lock_guard<std::mutex> guard(s->mu);
 s->recent=s->engine.dispatch(str(env,input));
 auto text=s->recent.symbol+" "+s->recent.title+"\n"+s->recent.detail;
 return env->NewStringUTF(text.c_str());
}
extern "C" JNIEXPORT jstring JNICALL Java_com_glass_unison_MainActivity_nativeStatus(JNIEnv* env,jobject,jlong pointer){
 auto* s=valid(pointer);if(!s)return env->NewStringUTF("NOT INITIALIZED");std::lock_guard<std::mutex> guard(s->mu);
 auto text=s->engine.snapshot()+"\n"+s->recent.symbol+" "+s->recent.title+"\n"+s->recent.detail;
 return env->NewStringUTF(text.c_str());
}
extern "C" JNIEXPORT void JNICALL Java_com_glass_unison_MainActivity_nativeRaster(JNIEnv* env,jobject,jlong pointer,jintArray destination,jint width,jint height,jlong phase){
 auto* s=valid(pointer);if(!s||!destination||width<1||height<1||width>2048||height>2048)return;
 auto n=env->GetArrayLength(destination);if(n<width*height)return;
 std::lock_guard<std::mutex> guard(s->mu);
 std::vector<uint32_t> pixels;
 glass::render_pixels(pixels,width,height,static_cast<uint64_t>(phase),s->engine.is_halted());
 env->SetIntArrayRegion(destination,0,width*height,reinterpret_cast<const jint*>(pixels.data()));
 s->engine.render_step();
}
