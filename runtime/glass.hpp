#pragma once
#include <algorithm>
#include <cerrno>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <map>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
#include <fcntl.h>
#include <sys/file.h>
#include <sys/stat.h>
#include <unistd.h>

namespace glass {
using Words=std::vector<std::string>;
inline void require(bool p,const std::string& why){if(!p)throw std::runtime_error(why);}
inline std::string quote(const std::string& s){
 std::ostringstream o; o<<'"';
 for(unsigned char c:s){
  if(c=='"'||c=='\\')o<<'\\'<<char(c);
  else if(c<32)o<<"\\u"<<std::hex<<std::setw(4)<<std::setfill('0')<<int(c)<<std::dec;
  else o<<char(c);
 }o<<'"';return o.str();
}
inline bool identifier(const std::string& s){
 return !s.empty()&&s.size()<=128&&std::all_of(s.begin(),s.end(),[](unsigned char c){return (c>='a'&&c<='z')||(c>='A'&&c<='Z')||(c>='0'&&c<='9')||c=='-'||c=='_'||c=='.';});
}
inline std::string encode(const std::string& s){
 std::ostringstream o;
 for(unsigned char c:s){if(c<=32||c=='%'||c>=127)o<<'%'<<std::hex<<std::uppercase<<std::setw(2)<<std::setfill('0')<<int(c)<<std::dec;else o<<char(c);}return o.str();
}
inline std::string decode(const std::string& s){
 std::string o;
 for(size_t i=0;i<s.size();++i){if(s[i]=='%'){require(i+2<s.size(),"percent escape requires two hex digits"); auto hex=[](char c){if(c>='0'&&c<='9')return c-'0';if(c>='A'&&c<='F')return c-'A'+10;throw std::runtime_error("hex digit required");};o+=char(hex(s[i+1])*16+hex(s[i+2]));i+=2;}else o+=s[i];}return o;
}
inline Words split(const std::string& s){Words out;size_t p=0;while(true){size_t q=s.find('\t',p);out.push_back(s.substr(p,q==s.npos?q:q-p));if(q==s.npos)return out;p=q+1;}}
struct Rule{std::string id,region,from,event,to;};
struct Intent{std::string event,input,adapter,choice; bool done=false;};
struct Observation{std::string intent,event,artifact,rationale;};
struct Machine{
 std::map<std::string,std::string> active;
 std::vector<Rule> rules;
 std::map<std::string,Intent> intents;
 std::vector<Observation> observations;
 void apply(const Words& w){
  require(!w.empty(),"command required");
  for(auto& s:w)require(s.size()<=65536,"field budget 65536 bytes");
  if(w[0]=="region"){
   require(w.size()==3&&identifier(w[1])&&identifier(w[2]),"region ID initial-state");
   require(!active.count(w[1]),"region ID already registered");active.emplace(w[1],w[2]);
  }else if(w[0]=="rule"){
   require(w.size()==6,"rule ID region from event to");
   for(size_t i=1;i<w.size();++i)require(identifier(w[i]),"rule identifiers required");
   require(active.count(w[2]),"declare region first");
   for(auto& r:rules){require(r.id!=w[1],"rule ID already registered");require(r.region!=w[2]||r.from!=w[3]||r.event!=w[4],"one rule per region/state/event");}
   rules.push_back({w[1],w[2],w[3],w[4],w[5]});
  }else if(w[0]=="intent"){
   require(w.size()==7&&identifier(w[1])&&identifier(w[2]),"intent ID event input adapter choice recovery");
   require(!intents.count(w[1]),"intent ID already registered");
   require(!w[3].empty()&&!w[4].empty()&&!w[5].empty()&&!w[6].empty(),"input, adapter, choice and recovery required");
   bool found=false;for(auto& r:rules)if(r.event==w[2]&&active.at(r.region)==r.from)found=true;
   require(found,"declare an enabled event before intent");
   intents.emplace(w[1],Intent{w[2],w[3],w[4],w[5]+"; recovery="+w[6],false});
  }else if(w[0]=="outcome"){
   require(w.size()==5,"outcome intent event artifact rationale");
   auto it=intents.find(w[1]); require(it!=intents.end(),"persist intent before outcome");
   require(!it->second.done,"intent already has an outcome");
   require(it->second.event==w[2],"outcome must match intended event");
   require(!w[3].empty()&&!w[4].empty(),"artifact and observable rationale required");
   auto next=active;bool matched=false;
   for(auto& r:rules)if(r.event==w[2]&&active.at(r.region)==r.from){next[r.region]=r.to;matched=true;}
   require(matched,"enabled transition required; reconcile concurrent changes");
   active=next;it->second.done=true;observations.push_back({w[1],w[2],w[3],w[4]});
  }else throw std::runtime_error("supported commands: region rule intent outcome");
 }
 std::string state()const{
  std::string o="{\"schema\":\"glass.configuration.v1\",\"regions\":{";bool first=true;
  for(auto& [r,s]:active){if(!first)o+=",";first=false;o+=quote(r)+":"+quote(s);}o+="},\"pending_intents\":[";first=true;
  for(auto& [id,in]:intents){if(!in.done){if(!first)o+=",";first=false;o+=quote(id);}}
  return o+"]}";
 }
 std::string weight()const{
  std::string o="{\"schema\":\"glass.structural-weight.v1\",\"construction\":\"exact-observed-prefix-path\",\"alphabet\":[";std::set<std::string> alphabet;
  for(auto& x:observations)alphabet.insert(x.event);
  bool first=true;for(auto& e:alphabet){if(!first)o+=",";first=false;o+=quote(e);}o+="],\"edges\":[";first=true;
  for(size_t i=0;i<observations.size();++i){auto& x=observations[i];if(!first)o+=",";first=false;o+="{\"from\":"+std::to_string(i)+",\"to\":"+std::to_string(i+1)+",\"event\":"+quote(x.event)+",\"intent\":"+quote(x.intent)+",\"artifact\":"+quote(x.artifact)+",\"choice\":"+quote(intents.at(x.intent).choice)+",\"observation\":"+quote(x.rationale)+"}";}
  return o+"]}";
 }
};
struct Journal{
 int fd=-1;uint64_t sequence=0;Machine machine;
 explicit Journal(const std::filesystem::path& path){
  if(!path.parent_path().empty())std::filesystem::create_directories(path.parent_path());
  fd=::open(path.c_str(),O_RDWR|O_CREAT|O_APPEND|O_NOFOLLOW,0600);
  require(fd>=0,"journal open failed");
  try{
   require(::flock(fd,LOCK_EX)==0,"journal lock failed");
   struct stat info{};require(::fstat(fd,&info)==0&&S_ISREG(info.st_mode)&&info.st_size<=64*1024*1024,"regular journal within 64MiB required");
   std::string raw;char buffer[8192];ssize_t n;
   while((n=::read(fd,buffer,sizeof buffer))>0)raw.append(buffer,n);
   require(n==0,"journal read failed");
   require(raw.empty()||raw.back()=='\n',"journal tail requires preserved-tail recovery");
   std::istringstream in(raw);std::string line;
   while(std::getline(in,line)){
    auto w=split(line);require(w.size()>=2,"journal record fields required");
    require(w[0]==std::to_string(sequence+1),"journal sequence discontinuity");
    Words command;for(size_t i=1;i<w.size();++i)command.push_back(decode(w[i]));
    machine.apply(command);++sequence;
   }
  }catch(...){::close(fd);fd=-1;throw;}
 }
 Journal(const Journal&)=delete;Journal& operator=(const Journal&)=delete;
 ~Journal(){if(fd>=0)::close(fd);}
 uint64_t cursor()const{return sequence;}
 void submit(const Words& command,uint64_t expected){
  require(expected==sequence,"stale cursor; reload configuration");
  Machine next=machine;next.apply(command);
  std::string line=std::to_string(sequence+1);for(auto& s:command)line+="\t"+encode(s);line+="\n";
  size_t done=0;while(done<line.size()){ssize_t n=::write(fd,line.data()+done,line.size()-done);if(n<0&&errno==EINTR)continue;require(n>0,"journal append failed; inspect tail");done+=size_t(n);}
  require(::fsync(fd)==0,"journal durability failed; reopen and reconcile");
  machine=std::move(next);++sequence;
 }
};
inline std::string spell(const std::string& text){
 std::string o="{\"schema\":\"glass.byte-write-trace.v1\",\"encoding\":\"input UTF-8 bytes\",\"baseline\":\"zero-filled per-byte\",\"write_order\":\"MSB-first\",\"text\":"+quote(text)+",\"bytes\":[";
 bool first=true;for(size_t i=0;i<text.size();++i){unsigned char c=text[i];if(!first)o+=",";first=false;std::string bits;int first_changed=-1;
  for(int b=7;b>=0;--b){bits+=((c>>b)&1)?'1':'0';if(first_changed<0&&((c>>b)&1))first_changed=b;}
  o+="{\"offset\":"+std::to_string(i)+",\"value\":"+std::to_string(c)+",\"bits\":"+quote(bits)+",\"first_changed_bit\":"+std::to_string(first_changed)+",\"writes\":[";
  for(int b=7;b>=0;--b){if(b<7)o+=",";o+="{\"bit\":"+std::to_string(b)+",\"before\":0,\"after\":"+std::to_string((c>>b)&1)+"}";}o+="]}";
 }return o+"]}";
}
}
