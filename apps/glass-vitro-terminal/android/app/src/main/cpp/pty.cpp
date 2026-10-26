#include <jni.h>
#include <atomic>
#include <cstdlib>
#include <cerrno>
#include <csignal>
#include <fcntl.h>
#include <poll.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <termios.h>
#include <unistd.h>
#include <string>
namespace { struct Pty { int fd{-1};pid_t child{-1};std::atomic<bool> closed{false}; };
Pty* get(jlong x){return reinterpret_cast<Pty*>(x);} }
extern "C" JNIEXPORT jlong JNICALL Java_com_glass_unison_MainActivity_nativeShellOpen(JNIEnv* env,jobject,jstring directory){
  const char* raw=directory?env->GetStringUTFChars(directory,nullptr):nullptr;
  std::string cwd=raw?raw:"/";
  if(raw)env->ReleaseStringUTFChars(directory,raw);
  int fd=posix_openpt(O_RDWR|O_NOCTTY|O_CLOEXEC);
  if(fd<0)return 0;
  if(grantpt(fd)||unlockpt(fd)){close(fd);return 0;}
  char slavepath[128]{};
  if(ptsname_r(fd,slavepath,sizeof(slavepath))){close(fd);return 0;}
  pid_t pid=fork();
  if(pid<0){close(fd);return 0;}
  if(pid==0){
    close(fd);setsid();
    int slave=open(slavepath,O_RDWR);
    if(slave<0)_exit(127);
    ioctl(slave,TIOCSCTTY,0);
    dup2(slave,STDIN_FILENO);dup2(slave,STDOUT_FILENO);dup2(slave,STDERR_FILENO);
    if(slave>2)close(slave);
    chdir(cwd.c_str());setenv("HOME",cwd.c_str(),1);
    setenv("PATH","/system/bin:/system/xbin",1);
    setenv("TERM","xterm",1);
#ifdef __ANDROID__
    execl("/system/bin/sh","sh","-i",static_cast<char*>(nullptr));
#else
    execl("/bin/sh","sh","-i",static_cast<char*>(nullptr));
#endif
    _exit(127);
  }
  auto* p=new Pty();p->fd=fd;p->child=pid;
  return reinterpret_cast<jlong>(p);
}
extern "C" JNIEXPORT jbyteArray JNICALL Java_com_glass_unison_MainActivity_nativeShellRead(JNIEnv* env,jobject,jlong h){
  auto* p=get(h);if(!p||p->closed)return nullptr;
  pollfd pf{p->fd,static_cast<short>(POLLIN|POLLHUP|POLLERR),0};
  int status=poll(&pf,1,250);
  if(p->closed)return nullptr;
  if(status<0&&errno==EINTR)return env->NewByteArray(0);
  if(status<=0)return env->NewByteArray(0);
  if(!(pf.revents&POLLIN))return nullptr;
  char buf[4096];ssize_t n=read(p->fd,buf,sizeof(buf));
  if(n<=0)return nullptr;
  jbyteArray a=env->NewByteArray(static_cast<jsize>(n));
  if(a)env->SetByteArrayRegion(a,0,static_cast<jsize>(n),reinterpret_cast<jbyte*>(buf));
  return a;
}
extern "C" JNIEXPORT void JNICALL Java_com_glass_unison_MainActivity_nativeShellWrite(JNIEnv* env,jobject,jlong h,jbyteArray input){
  auto* p=get(h);if(!p||p->closed||!input)return;
  jsize n=env->GetArrayLength(input);if(n<=0||n>65536)return;
  auto* b=env->GetByteArrayElements(input,nullptr);if(!b)return;
  size_t i=0;
  while(i<static_cast<size_t>(n)&&!p->closed){
    ssize_t k=write(p->fd,b+i,static_cast<size_t>(n)-i);
    if(k<0&&errno==EINTR)continue;
    if(k<=0)break;
    i+=static_cast<size_t>(k);
  }
  env->ReleaseByteArrayElements(input,b,JNI_ABORT);
}
extern "C" JNIEXPORT void JNICALL Java_com_glass_unison_MainActivity_nativeShellResize(JNIEnv*,jobject,jlong h,jint c,jint r){
  auto* p=get(h);if(!p||p->closed||c<=0||r<=0)return;
  winsize size{};size.ws_col=static_cast<unsigned short>(c);size.ws_row=static_cast<unsigned short>(r);
  ioctl(p->fd,TIOCSWINSZ,&size);if(p->child>0)kill(p->child,SIGWINCH);
}
extern "C" JNIEXPORT void JNICALL Java_com_glass_unison_MainActivity_nativeShellStop(JNIEnv*,jobject,jlong h){
  auto* p=get(h);if(!p||p->closed.exchange(true))return;
  if(p->child>0)kill(p->child,SIGHUP);
  if(p->fd>=0){close(p->fd);p->fd=-1;}
}
extern "C" JNIEXPORT void JNICALL Java_com_glass_unison_MainActivity_nativeShellDispose(JNIEnv*,jobject,jlong h){
  auto* p=get(h);if(!p)return;
  if(!p->closed.exchange(true)){
    if(p->child>0)kill(p->child,SIGHUP);
    if(p->fd>=0)close(p->fd);
  }
  if(p->child>0){int status=0;pid_t done=waitpid(p->child,&status,WNOHANG);
  if(done==0){kill(p->child,SIGKILL);waitpid(p->child,&status,0);}}
  delete p;
}
