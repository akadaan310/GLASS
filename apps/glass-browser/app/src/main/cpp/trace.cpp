#include <jni.h>
#include <string>
#include <mutex>
#include <chrono>
#include <cstdio>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
namespace {
std::mutex gate;
uint64_t cursor=0;
std::string esc(const std::string& in){ std::string r; for(unsigned char c:in){if(c=='"'||c=='\\'){r+='\\';r+=char(c);}else if(c=='\n')r+="\\n";else if(c>=32)r+=char(c);}return r;}
}
extern "C" JNIEXPORT jlong JNICALL Java_dev_glass_browser_BrowserActivity_record(JNIEnv* env,jobject, jstring path,jstring type,jstring value){
 const char* p=env->GetStringUTFChars(path,nullptr);const char* t=env->GetStringUTFChars(type,nullptr);const char* v=env->GetStringUTFChars(value,nullptr);
 std::lock_guard<std::mutex> guard(gate);
 auto tick=std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::steady_clock::now().time_since_epoch()).count();
 std::string line="{\"cursor\":"+std::to_string(++cursor)+",\"monotonic_ns\":"+std::to_string(tick)+",\"type\":\""+esc(t)+"\",\"value\":\""+esc(v)+"\"}\n";
 int fd=open(p,O_WRONLY|O_CREAT|O_APPEND|O_CLOEXEC,0600);if(fd>=0){size_t off=0;while(off<line.size()){ssize_t n=write(fd,line.data()+off,line.size()-off);if(n<=0)break;off+=(size_t)n;}fsync(fd);close(fd);}
 env->ReleaseStringUTFChars(path,p);env->ReleaseStringUTFChars(type,t);env->ReleaseStringUTFChars(value,v);return (jlong)cursor;
}
