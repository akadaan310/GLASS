#include "glass.hpp"
#include <chrono>
#include <iostream>
#include <poll.h>
#include <signal.h>
#include <sys/wait.h>
struct Result{int code;std::string output;};
static Result run(const std::filesystem::path& cwd,glass::Words args){
 int pipes[2];glass::require(pipe(pipes)==0,"process pipe failed");
 pid_t child=fork();
 if(child<0){close(pipes[0]);close(pipes[1]);throw std::runtime_error("fork failed");}
 if(child==0){
  setpgid(0,0);close(pipes[0]);dup2(pipes[1],1);dup2(pipes[1],2);close(pipes[1]);
  if(chdir(cwd.c_str())!=0)_exit(126);
  setenv("GIT_TERMINAL_PROMPT","0",1);
  std::vector<char*> argv;for(auto& a:args)argv.push_back(a.data());argv.push_back(nullptr);
  execvp(argv[0],argv.data());_exit(127);
 }
 setpgid(child,child);close(pipes[1]);fcntl(pipes[0],F_SETFL,O_NONBLOCK);
 auto deadline=std::chrono::steady_clock::now()+std::chrono::seconds(30);
 std::string output;int status=0;bool ended=false;
 while(!ended){
  char b[4096];ssize_t n;while((n=read(pipes[0],b,sizeof b))>0){if(output.size()<65536)output.append(b,std::min<size_t>(n,65536-output.size()));}
  auto waited=waitpid(child,&status,WNOHANG);
  if(waited==child){ended=true;break;}
  if(waited<0&&errno!=EINTR){kill(-child,SIGKILL);waitpid(child,&status,0);close(pipes[0]);throw std::runtime_error("wait failed");}
  if(std::chrono::steady_clock::now()>=deadline){kill(-child,SIGKILL);waitpid(child,&status,0);close(pipes[0]);return {124,output};}
  pollfd p{pipes[0],POLLIN,0};poll(&p,1,20);
 }
 char b[4096];ssize_t n;while((n=read(pipes[0],b,sizeof b))>0){if(output.size()<65536)output.append(b,std::min<size_t>(n,65536-output.size()));}
 close(pipes[0]);return {WIFEXITED(status)?WEXITSTATUS(status):128,output};
}
int main(int argc,char** argv){
 std::string outcome="queued",reason="publication awaiting transport",head;
 std::filesystem::path receipt;
 try{
  glass::require(argc>=4,"glass-publish REPO RECEIPT PATH...");
  auto repo=std::filesystem::canonical(argv[1]);receipt=std::filesystem::absolute(argv[2]);
  glass::Journal lock(repo/".git/glass-publication.lock");
  auto git=[&](glass::Words args){args.insert(args.begin(),"git");return run(repo,args);};
  auto branch=git({"branch","--show-current"});glass::require(branch.code==0&&branch.output=="main\n","publication uses checked-out main");
  for(int i=3;i<argc;++i){
   std::filesystem::path p(argv[i]);glass::require(!p.empty()&&!p.is_absolute(),"relative publication path required");
   auto it=p.begin();glass::require(it!=p.end()&&*it!=".git","publication path belongs to worktree");
   for(auto& component:p)glass::require(component!=".."&&component!=".","canonical relative path required");
   auto current=repo;for(auto& component:p){current/=component;glass::require(!std::filesystem::is_symlink(current),"publish regular paths with source visibility review");}
  }
  glass::require(git({"diff","--cached","--quiet"}).code==0,"preserve existing staged work before publication");
  glass::require(git({"fetch","origin","main"}).code==0,"remote fetch queued for retry");
  glass::require(git({"merge","--ff-only","origin/main"}).code==0,"main reconciliation queued");
  glass::Words add={"add","--"};for(int i=3;i<argc;++i)add.push_back(argv[i]);
  glass::require(git(add).code==0,"selected paths await staging");
  auto diff=git({"diff","--cached","--quiet"});
  glass::require(diff.code==0||diff.code==1,"staged comparison requires inspection");
  if(diff.code==1)glass::require(git({"commit","-m","glass: publish durable commission unit"}).code==0,"local commit queued");
  auto local=git({"rev-parse","HEAD"});glass::require(local.code==0,"local head required");head=local.output;if(!head.empty()&&head.back()=='\n')head.pop_back();
  glass::require(git({"push","origin","HEAD:refs/heads/main"}).code==0,"local main retained; remote push queued");
  auto remote=git({"ls-remote","origin","refs/heads/main"});
  glass::require(remote.code==0&&remote.output.starts_with(head+"\t"),"remote observation queued for reconciliation");
  outcome="published";reason="remote main observed at local head";
 }catch(const std::exception& e){reason=e.what();}
 std::string record="{\"schema\":\"glass.publication.v1\",\"branch\":\"main\",\"outcome\":"+glass::quote(outcome)+",\"head\":"+glass::quote(head)+",\"reason\":"+glass::quote(reason)+"}\n";
 try{
  if(!receipt.empty()){
   if(!receipt.parent_path().empty())std::filesystem::create_directories(receipt.parent_path());
   int fd=open(receipt.c_str(),O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW,0600);glass::require(fd>=0,"new receipt path required");
   size_t done=0;while(done<record.size()){ssize_t n=write(fd,record.data()+done,record.size()-done);if(n<0&&errno==EINTR)continue;if(n<=0){close(fd);throw std::runtime_error("receipt write failed");}done+=size_t(n);}int synced=fsync(fd);close(fd);glass::require(synced==0,"receipt durability requires inspection");
  }
 }catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 3;}
 std::cout<<record;return outcome=="published"?0:2;
}
