#pragma once
// GLASS/0.1: bounded offline state machine; not an OS screen-access bypass.
#include <array>
#include <cstdint>
#include <mutex>
#include <stdexcept>
#include <string>
#include <string_view>
#include <vector>
#include <sstream>
#include <iomanip>
#include <utility>
#include <algorithm>

namespace glass::native {

enum class Capture { idle, awaiting_consent, capturing, denied, stopped };
inline std::string quote(std::string_view x){
  std::ostringstream o; o << '"';
  for (unsigned char c : x){
    if(c=='"'||c=='\\'){o<<'\\'<<char(c);}
    else if(c<32){o<<"\\u"<<std::hex<<std::setw(4)<<std::setfill('0')<<int(c)<<std::dec;}
    else o<<char(c);
  }
  return o.str()+'"';
}
struct Event {uint64_t sequence, epoch, monotonic_ns;std::string kind, origin, detail;};
class Ledger{
public:
  explicit Ledger(std::size_t capacity=2048): capacity_(capacity){if(capacity<1||capacity>65536)throw std::invalid_argument("bounded ledger");}
  Event append(std::string kind,std::string origin,std::string detail,uint64_t t){
    if(kind.empty()||kind.size()>64||origin.empty()||origin.size()>32||detail.size()>1024)throw std::invalid_argument("event budget");
    std::lock_guard<std::mutex> lock(mu_);
    if(t<last_ns_) throw std::invalid_argument("nonmonotone elapsed time");
    last_ns_=t;
    Event e{++seq_,epoch_,t,std::move(kind),std::move(origin),std::move(detail)};
    if(events_.size()==capacity_){events_.erase(events_.begin());++evicted_;}
    events_.push_back(e);
    return e;
  }
  void consentRequested(uint64_t t){change(Capture::idle,Capture::awaiting_consent,"CONSENT_REQUESTED",t);}
  void approved(uint64_t t){
    std::lock_guard<std::mutex> lock(mu_);
    if(state_!=Capture::awaiting_consent)throw std::logic_error("consent not requested");
    state_=Capture::capturing; ++epoch_;
    appendLocked("CAPTURE_STARTED","system","user authorized this session",t);
  }
  void refused(uint64_t t){
    std::lock_guard<std::mutex> lock(mu_);
    if(state_!=Capture::awaiting_consent)throw std::logic_error("consent not requested");
    state_=Capture::denied;appendLocked("CAPTURE_GAP","system","consent denied",t);
  }
  void stopped(std::string reason,uint64_t t){
    std::lock_guard<std::mutex> lock(mu_);
    if(state_!=Capture::capturing && state_!=Capture::awaiting_consent)throw std::logic_error("capture not active");
    state_=Capture::stopped;appendLocked("CAPTURE_GAP","system",std::move(reason),t);
  }
  void requestAgain(uint64_t t){
    std::lock_guard<std::mutex> lock(mu_);
    if(state_==Capture::capturing||state_==Capture::awaiting_consent)throw std::logic_error("already capturing or requesting");
    state_=Capture::awaiting_consent;appendLocked("CONSENT_REQUESTED","user","new permission session",t);
  }
  std::string status() const{
    std::lock_guard<std::mutex> lock(mu_);
    std::ostringstream o;
    o<<"{\"schema\":\"glass.ledger/0.1\",\"epoch\":"<<epoch_<<",\"sequence\":"<<seq_
     <<",\"evicted\":"<<evicted_<<",\"capture\":"<<quote(captureName(state_))<<"}";
    return o.str();
  }
  static std::string json(const Event& e){
    std::ostringstream o;
    o<<"{\"seq\":"<<e.sequence<<",\"epoch\":"<<e.epoch<<",\"monotonic_ns\":"<<e.monotonic_ns
     <<",\"kind\":"<<quote(e.kind)<<",\"origin\":"<<quote(e.origin)<<",\"detail\":"<<quote(e.detail)<<"}";
    return o.str();
  }
  uint64_t evicted()const{std::lock_guard<std::mutex> l(mu_);return evicted_;}
  static const char* captureName(Capture c){switch(c){case Capture::idle:return "IDLE";case Capture::awaiting_consent:return "AWAITING_CONSENT";case Capture::capturing:return "CAPTURING";case Capture::denied:return "DENIED_GAP";case Capture::stopped:return "STOPPED_GAP";}return "UNKNOWN";}
private:
  void change(Capture from,Capture to,const char* label,uint64_t t){
    std::lock_guard<std::mutex> lock(mu_);
    if(state_!=from)throw std::logic_error("invalid capture transition");
    state_=to;appendLocked(label,"user","",t);
  }
  void appendLocked(std::string k,std::string o,std::string d,uint64_t t){
    if(t<last_ns_)throw std::invalid_argument("nonmonotone elapsed time");
    last_ns_=t;Event e{++seq_,epoch_,t,std::move(k),std::move(o),std::move(d)};
    if(events_.size()==capacity_){events_.erase(events_.begin());++evicted_;}events_.push_back(std::move(e));
  }
  mutable std::mutex mu_;
  const std::size_t capacity_;
  std::vector<Event> events_;
  uint64_t seq_=0,epoch_=0,last_ns_=0,evicted_=0;
  Capture state_=Capture::idle;
};
struct Register {char32_t glyph; unsigned value;bool honorable;};
inline constexpr std::array<Register,28> registry{{
{U'ا',1,true},{U'ب',2,false},{U'ج',3,false},{U'د',4,false},{U'ه',5,true},{U'و',6,false},{U'ز',7,false},{U'ح',8,true},{U'ط',9,true},
{U'ي',10,true},{U'ك',20,true},{U'ل',30,true},{U'م',40,true},{U'ن',50,true},{U'س',60,true},{U'ع',70,true},{U'ف',80,false},{U'ص',90,true},
{U'ق',100,true},{U'ر',200,true},{U'ش',300,false},{U'ت',400,false},{U'ث',500,false},{U'خ',600,false},{U'ذ',700,false},{U'ض',800,false},{U'ظ',900,false},{U'غ',1000,false}
}};
inline std::u32string utf8(std::string_view x){
  std::u32string result;
  for(size_t i=0;i<x.size();){const auto a=static_cast<unsigned char>(x[i]);char32_t cp=0;unsigned len=0;
    if(a<0x80){cp=a;len=1;}else if((a&0xe0)==0xc0){cp=a&31;len=2;if(cp<2)throw std::invalid_argument("UTF8 overlong");}
    else if((a&0xf0)==0xe0){cp=a&15;len=3;}else if((a&0xf8)==0xf0){cp=a&7;len=4;if(cp>4)throw std::invalid_argument("UTF8 out of range");}
    else throw std::invalid_argument("UTF8 lead");
    if(i+len>x.size())throw std::invalid_argument("UTF8 truncated");
    for(unsigned j=1;j<len;j++){const auto b=static_cast<unsigned char>(x[i+j]);if((b&0xc0)!=0x80)throw std::invalid_argument("UTF8 continuation");cp=(cp<<6)|(b&63);}
    if((len==2&&cp<128)||(len==3&&cp<2048)||(len==4&&cp<65536)||cp>0x10ffff||(cp>=0xd800&&cp<=0xdfff))throw std::invalid_argument("UTF8 scalar");
    result.push_back(cp);i+=len;
  }
  return result;
}
inline char32_t skeleton(char32_t c){
  if(c==U'أ'||c==U'إ'||c==U'آ'||c==U'ٱ')return U'ا';
  if(c==U'ؤ')return U'و';
  if(c==U'ئ'||c==U'ى')return U'ي';
  if(c==U'ة')return U'ه';
  return c;
}
inline std::string spell(std::string_view word){
  if(word.size()>512)throw std::invalid_argument("word size");
  const auto cps=utf8(word);unsigned hon=0,nob=0,sum=0,unknown=0;std::string sig;
  for(auto cp:cps){if((cp>=0x064b&&cp<=0x065f)||cp==0x0670||(cp>=0x06d6&&cp<=0x06ed))continue;
    cp=skeleton(cp);bool found=false;
    for(const auto& r:registry)if(r.glyph==cp){++(r.honorable?hon:nob);sum+=r.value;sig+=r.honorable?'H':'N';found=true;break;}
    if(!found)++unknown;
  }
  std::string cls=unknown?"UNRESOLVED":hon&&nob?"MIXED":hon?"HONORABLE":"NOBLE";
  std::ostringstream o;o<<"{\"word\":"<<quote(word)<<",\"profile\":\"lossy-skeleton-v0.1\",\"class\":"<<quote(cls)
    <<",\"signature\":"<<quote(sig)<<",\"honorable\":"<<hon<<",\"noble\":"<<nob<<",\"native_sum\":"<<sum<<",\"unresolved\":"<<unknown<<"}";
  return o.str();
}
// Small explicit terminal protocol, READ-ONLY. No web-page may call this without GLASS UI admission.
inline std::string route(std::string_view url, const Ledger& ledger){
  constexpr std::string_view p="glass://terminal/v1/";
  if(url.substr(0,p.size())!=p)throw std::invalid_argument("unrecognized terminal namespace");
  auto rest=url.substr(p.size());
  if(rest=="state")return ledger.status();
  if(rest.substr(0,6)=="spell?"){
    constexpr std::string_view q="spell?word=";
    if(rest.substr(0,q.size())!=q)throw std::invalid_argument("unsupported query");
    auto val=rest.substr(q.size());if(val.size()>1024)throw std::invalid_argument("terminal input budget");
    std::string decoded;
    for(size_t i=0;i<val.size();++i){char c=val[i];if(c=='%'){
        if(i+2>=val.size())throw std::invalid_argument("bad percent escape");
        auto digit=[](char x)->int{if(x>='0'&&x<='9')return x-'0';if(x>='a'&&x<='f')return x-'a'+10;if(x>='A'&&x<='F')return x-'A'+10;throw std::invalid_argument("bad hex");};
        decoded.push_back(static_cast<char>((digit(val[i+1])<<4)|digit(val[i+2])));i+=2;
      }else if(c=='+')decoded.push_back(' ');else decoded.push_back(c);}
    return spell(decoded);
  }
  throw std::invalid_argument("terminal route refused");
}
enum class BinaryKind{elf,pe,macho,zip,unknown};
inline const char* name(BinaryKind k){switch(k){case BinaryKind::elf:return "ELF";case BinaryKind::pe:return "PE";case BinaryKind::macho:return "MACH_O";case BinaryKind::zip:return "ZIP_APK_OR_JAR";default:return "UNKNOWN";}}
// Header *identification*, not format verification or executable loading.
inline BinaryKind identify(const uint8_t *p,size_t n){
  if(n>=4&&p[0]==0x7f&&p[1]=='E'&&p[2]=='L'&&p[3]=='F')return BinaryKind::elf;
  if(n>=4&&p[0]=='P'&&p[1]=='K'&&p[2]==3&&p[3]==4)return BinaryKind::zip;
  if(n>=4&&((p[0]==0xfe&&p[1]==0xed&&p[2]==0xfa&&(p[3]==0xce||p[3]==0xcf))||(p[0]==0xcf&&p[1]==0xfa&&p[2]==0xed&&p[3]==0xfe)||(p[0]==0xce&&p[1]==0xfa&&p[2]==0xed&&p[3]==0xfe)))return BinaryKind::macho;
  if(n>=64&&p[0]=='M'&&p[1]=='Z'){
    uint32_t off=uint32_t(p[0x3c])|(uint32_t(p[0x3d])<<8)|(uint32_t(p[0x3e])<<16)|(uint32_t(p[0x3f])<<24);
    if(off<=n&&n-off>=4&&p[off]=='P'&&p[off+1]=='E'&&p[off+2]==0&&p[off+3]==0)return BinaryKind::pe;
  }
  return BinaryKind::unknown;
}
}
