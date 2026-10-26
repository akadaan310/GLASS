#include "unison.hpp"
#include "sha256.hpp"
#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <limits>
#include <numeric>
#include <sstream>
#include <stdexcept>

namespace glass {
namespace {
uint64_t steady_ns(){return static_cast<uint64_t>(std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::steady_clock::now().time_since_epoch()).count());}
std::string lowercase(std::string s){std::transform(s.begin(),s.end(),s.begin(),[](unsigned char c){return static_cast<char>(std::tolower(c));});return s;}
std::string trim(std::string s){auto first=s.find_first_not_of(" \r\n\t");if(first==std::string::npos)return {};auto last=s.find_last_not_of(" \r\n\t");return s.substr(first,last-first+1);}
std::string json_escape(const std::string& s){std::ostringstream o;for(unsigned char c:s){switch(c){case '"':o<<"\\\"";break;case '\\':o<<"\\\\";break;case '\n':o<<"\\n";break;case '\r':o<<"\\r";break;case '\t':o<<"\\t";break;default:if(c<32){o<<"\\u"<<std::hex<<std::setw(4)<<std::setfill('0')<<int(c)<<std::dec;}else o<<char(c);}}return o.str();}
std::string event_body(const Event& e){return std::to_string(e.tick)+"|"+std::to_string(e.monotonic_ns)+"|"+e.kind+"|"+e.source+"|"+e.detail;}
std::string fmt(double v){std::ostringstream o;o<<std::fixed<<std::setprecision(5)<<v;return o.str();}
}
bool NDim::translate(size_t axis,double delta){if(axis>=coordinates.size()||!std::isfinite(delta))return false;double next=coordinates[axis]+delta;if(!std::isfinite(next))return false;coordinates[axis]=next;return true;}
bool NDim::rotate(size_t p,size_t q,double theta){if(p>=coordinates.size()||q>=coordinates.size()||p==q||!std::isfinite(theta))return false;auto c=std::cos(theta),s=std::sin(theta),a=coordinates[p],b=coordinates[q];coordinates[p]=c*a-s*b;coordinates[q]=s*a+c*b;return true;}
double NDim::radius() const {long double r=0;for(auto x:coordinates)r+=x*x;return std::sqrt(static_cast<double>(r));}
Engine::Engine(std::string journal):space{{0,0,0}},journal_(std::move(journal)){record("GENESIS","GLASS","Λ⊗Ω⊗Γ⊗τ⊗Π→۞");}
std::string Engine::digest(const std::string& s){return sha256(s);}
uint32_t Engine::bit_gate(uint32_t a,uint32_t b,const std::string& gate){
 if(gate=="xor"||gate=="⊕")return a^b;
 if(gate=="and"||gate=="∧")return a&b;
 if(gate=="or"||gate=="∨")return a|b;
 if(gate=="not"||gate=="¬")return ~a;
 if(gate=="shift"||gate=="≪")return a<<(b&31);
 if(gate=="right"||gate=="≫")return a>>(b&31);
 if(gate=="rot"||gate=="↻"){unsigned n=b&31;return n?((a<<n)|(a>>(32-n))):a;}
 throw std::invalid_argument("unknown bit operator");
}
bool Engine::decode_uint(const std::string& s,uint32_t& out){try{size_t used=0;auto v=std::stoull(s,&used,0);if(used!=s.size()||v>UINT32_MAX)return false;out=static_cast<uint32_t>(v);return true;}catch(...){return false;}}
std::vector<std::string> Engine::split(const std::string& s){std::istringstream in(s);std::vector<std::string> v;std::string w;while(in>>w)v.push_back(w);return v;}
std::vector<std::string> Engine::graphemes(const std::string& s){
 // UTF-8 code point slices; true grapheme clusters need Unicode ICU (future adapter).
 std::vector<std::string> v;for(size_t i=0;i<s.size();){auto c=static_cast<uint8_t>(s[i]);size_t n=c<128?1:c>=0xf0?4:c>=0xe0?3:c>=0xc2?2:1;n=std::min(n,s.size()-i);v.push_back(s.substr(i,n));i+=n;}return v;
}
std::string Engine::encode_uri(const std::string& s){std::ostringstream o;for(unsigned char b:s){if((b>='A'&&b<='Z')||(b>='a'&&b<='z')||(b>='0'&&b<='9')||b=='_'||b=='-'||b=='.'||b=='~')o<<b;else o<<'%'<<std::uppercase<<std::hex<<std::setw(2)<<std::setfill('0')<<unsigned(b)<<std::nouppercase<<std::dec;}return o.str();}
MatrixResult Engine::multiply10(const std::array<int32_t,100>& a,const std::array<int32_t,100>& b){MatrixResult r;r.trace.reserve(1000);for(int i=0;i<10;i++)for(int j=0;j<10;j++){int32_t acc=0;for(int k=0;k<10;k++){auto before=acc;acc+=a[i*10+k]*b[k*10+j];r.trace.push_back({i,j,k,a[i*10+k],b[k*10+j],before,acc});}r.values[i*10+j]=acc;}std::ostringstream sig;for(const auto& op:r.trace)sig<<op.row<<','<<op.col<<','<<op.k<<','<<op.lhs<<','<<op.rhs<<','<<op.after<<';';r.signature=digest(sig.str());return r;}
std::vector<int> Engine::path10(const std::string& shape){std::vector<int> v;
 if(shape=="row")for(int i=0;i<100;i++)v.push_back(i);
 else if(shape=="column")for(int c=0;c<10;c++)for(int r=0;r<10;r++)v.push_back(r*10+c);
 else if(shape=="diagonal")for(int r=0;r<10;r++)v.push_back(r*10+r);
 else if(shape=="anti-diagonal")for(int r=0;r<10;r++)v.push_back(r*10+9-r);
 else if(shape=="perimeter"){for(int c=0;c<10;c++)v.push_back(c);for(int r=1;r<9;r++)v.push_back(r*10+9);for(int c=9;c>=0;c--)v.push_back(90+c);for(int r=8;r>0;r--)v.push_back(r*10);}
 else if(shape=="snake")for(int r=0;r<10;r++)for(int c=0;c<10;c++)v.push_back(r*10+(r%2?9-c:c));
 return v;
}
void Engine::record(const std::string& kind,const std::string& source,const std::string& detail){Event e;e.tick=clock_;e.monotonic_ns=steady_ns();e.kind=kind;e.source=source;e.detail=detail;e.previous=last_digest_;e.digest=digest(e.previous+"\n"+event_body(e));last_digest_=e.digest;events_.push_back(e);if(events_.size()>10000)events_.erase(events_.begin());if(!journal_.empty()){std::ofstream out(journal_,std::ios::app);if(out){out<<"{\"clock\":"<<e.tick<<",\"monotonic_ns\":"<<e.monotonic_ns<<",\"kind\":\""<<json_escape(e.kind)<<"\",\"source\":\""<<json_escape(e.source)<<"\",\"detail\":\""<<json_escape(e.detail)<<"\",\"previous\":\""<<e.previous<<"\",\"sha256\":\""<<e.digest<<"\"}\n";out.flush();}}}
bool Engine::verify() const {for(size_t i=0;i<events_.size();i++){const auto& e=events_[i];if(i>0&&e.previous!=events_[i-1].digest)return false;if(e.digest!=digest(e.previous+"\n"+event_body(e)))return false;if(i>0&&e.tick<events_[i-1].tick)return false;}return true;}
Result Engine::report(const std::string& title,const std::string& detail,const std::string& symbol){record("RESULT",title,detail);return {true,title,detail,symbol,clock_};}
void Engine::render_step(){
 render_frames_++;
 // An autonomous, finite, evidence-bearing letter oracle, at a deliberately bounded cadence.
 if(!halted_ && render_frames_%24==0){
   const char* letters[]={"Λ","Ω","Γ","τ","Π","⊕","↻","۞","ج","أ","λ","α"};
   const auto n=(render_frames_/24)%12;
   clock_++;
   record("GENERATOR_STEP","AUTO","⟦Λ:"+std::string(letters[n])+" ⊗ Γ:rotate ⊙ τ:"+std::to_string(clock_)+"⟧");
 }
} // 24 rendered observations per autonomous logical transition.

std::string Engine::snapshot() const {std::ostringstream o;o<<"GLASS ۞ / "<<VERSION<<"  τ:"<<clock_<<"  "<<(halted_?"CLOCK STOPPED":"CLOCK ACTIVE")<<"  Π:"<<last_digest_.substr(0,12)<<"  D:"<<space.coordinates.size();return o.str();}
Result Engine::dispatch(const std::string& original){
 std::string s=trim(original);if(s.empty())return {true,"OBSERVE",snapshot(),"⊙",clock_};
 std::string lower=lowercase(s), mapped=s;
 if(lower=="help"||lower=="?"||lower=="commands")mapped="help";
 else if(lower=="clock"||lower=="time"||lower=="what time is it")mapped="clock";
 else if(lower=="stop clock"||lower=="halt clock"||lower=="halt")mapped="halt";
 else if(lower=="resume clock"||lower=="resume"||lower=="continue")mapped="resume";
 else if(lower=="show state"||lower=="state")mapped="state";
 else if(lower=="show dimensions"||lower=="dimensions")mapped="dimensions";
 else if(lower=="show trace"||lower=="trace")mapped="trace";
 else if(lower=="show protocol"||lower=="protocol")mapped="protocol";
 else if(lower=="multiply 10 by 10 matrix"||lower=="multiply matrices"||lower=="matrix")mapped="matrix";
 else if(lower=="arabic alphabet"||lower=="arabic"||lower=="letters")mapped="alphabet";
 if(s.find("⟦")!=std::string::npos){
   if(s.find("Γ:xor")!=std::string::npos||s.find("⊕")!=std::string::npos){std::string a="1",b="0";size_t p=s.find("xor(");if(p!=std::string::npos){auto end=s.find(')',p);if(end!=std::string::npos){auto x=s.substr(p+4,end-p-4); auto comma=x.find(',');if(comma!=std::string::npos){a=x.substr(0,comma);b=x.substr(comma+1);}}}mapped="xor "+a+" "+b;}
   else if(s.find("Γ:rotate")!=std::string::npos)mapped="spin 0 1 0.125";
   else if(s.find("Γ:halt")!=std::string::npos)mapped="halt";
   else mapped="protocol";
 }
 auto v=split(mapped);if(v.empty())return {true,"OBSERVE",snapshot(),"⊙",clock_};
 std::string op=lowercase(v[0]);if(op.size()>1&&op[0]==':')op=op.substr(1);
 if(halted_&&op!="resume"&&op!="state"&&op!="clock"&&op!="trace"&&op!="help")return {false,"CLOCK STOPPED","⟦τ:HALT⟧ refuses state changes. Type resume.","⊣",clock_};
 if(op=="halt"){record("HALT","τ","logical clock frozen");halted_=true;return {true,"HALTED","Finite-state clock stopped; view remains observable.","∅",clock_};}
 if(op=="resume"){halted_=false;clock_++;return report("RESUMED","Logical clock permits transitions.","τ");}
 if(op!="state"&&op!="clock"&&op!="trace"&&op!="help")clock_++;
 if(op=="help")return {true,"UNISON LANGUAGE","help · clock · halt · resume · xor 1 0 · and 3 1 · rot 1 4 · matrix · tape diagonal · space 5 · move 0 1 · spin 0 1 .2 · energy 0 1 · qubit h · alphabet · protocol · url Λ · :shell (CLI)","Λ",clock_};
 if(op=="clock"||op=="state")return {true,"VITROMATON",snapshot(),"τ",clock_};
 if(op=="trace")return {true,"PROVENANCE",std::to_string(events_.size())+" journal events; SHA256 chain "+(verify()?"VALID":"INVALID")+" · last "+last_digest_.substr(0,16),"Π",clock_};
 if(op=="alphabet")return report("Λ ARABIC / 28","هجائي: ابتثجحخدذرزسشصضطظعغفقكلمنهوي · أبجدي: أبجدهوزحطيكلمنسعفصقرشتثخذضظغ","Λ");
 if(op=="protocol")return report("UNISOL/0.1","⟦Λ:alphabet ⊗ Ω:oracle ⊗ Γ:generator ⊗ τ:clock ⊗ Π:proof⟧ → ۞ ; dimensions are typed axes; network transport remains HTTPS.","۞");
 if(op=="url"){std::string parameter=s.size()>4?s.substr(4):"Λ";return report("STERILE URL","https://glass.invalid/unisol/observe?tape="+encode_uri(parameter),"⟐");}
 if(op=="xor"||op=="⊕"||op=="and"||op=="∧"||op=="or"||op=="∨"||op=="rot"||op=="↻"||op=="not"||op=="shift"||op=="right"){
   if(v.size()<2) return {false,"BAD OPERANDS","Expected: xor 0x2 0x1","⊣",clock_};
   uint32_t a=0,b=0;
   if(!decode_uint(v[1],a)||(v.size()>2&&!decode_uint(v[2],b)))
     return {false,"BAD OPERANDS","Unsigned 32-bit integer required.","⊣",clock_};
   auto r=bit_gate(a,b,op); auto flips=__builtin_popcount(a^r);std::ostringstream msg;msg<<"0x"<<std::hex<<a<<" "<<op<<" 0x"<<b<<" = 0x"<<r<<std::dec<<" · changes "<<flips<<"/32 bits · O(1) fixed word";return report("BIT GATE",msg.str(),"⊕");
 }
 if(op=="energy"||op=="heat"){
   uint32_t a=0,b=0;if(v.size()<3||!decode_uint(v[1],a)||!decode_uint(v[2],b))return {false,"BAD ENERGY SAMPLE","energy <before> <after>; bounded switching proxy only.","⊣",clock_};
   auto flips=__builtin_popcount(a^b);return report("SWITCHING PROXY",std::to_string(flips)+" bit transitions; E∝C·V²·switches. NOT a measured temperature.","∿");
 }
 if(op=="space"){
   uint32_t n;if(v.size()!=2||!decode_uint(v[1],n)||n<1||n>16)return {false,"DIMENSION GUARD","space N (1..16)","⊣",clock_};space.coordinates.assign(n,0.0);return report("N-DIMENSIONAL SPACE","ℝ^"+std::to_string(n)+" initialized to the origin.","Λ");
 }
 if(op=="dimensions")return {true,"DIMENSIONS","Current space: ℝ^"+std::to_string(space.coordinates.size())+" · radius "+fmt(space.radius()),"Λ",clock_};
 if(op=="move"||op=="spin"){
   try{bool ok=false;if(op=="move"&&v.size()==3)ok=space.translate(std::stoul(v[1]),std::stod(v[2]));if(op=="spin"&&v.size()==4)ok=space.rotate(std::stoul(v[1]),std::stoul(v[2]),std::stod(v[3]));if(!ok)return {false,"COORDINATE REFUSED","Axis out of range or nonfinite parameter.","⊣",clock_};return report("N-DIMENSIONAL ORBIT","D="+std::to_string(space.coordinates.size())+" |x|="+fmt(space.radius())+" (Euclidean norm)","↻");}catch(...){return {false,"COORDINATE REFUSED","move axis delta / spin axis axis radians","⊣",clock_};}
 }
 if(op=="qubit"||op=="quantum"){
   std::string action=v.size()>1?lowercase(v[1]):"state";
   auto a=qubit_[0],b=qubit_[1];
   if(action=="reset")qubit_={std::complex<double>(1,0),std::complex<double>(0,0)};
   else if(action=="x")qubit_={b,a};
   else if(action=="z")qubit_={a,-b};
   else if(action=="h"){
     double scale=std::sqrt(.5);
     qubit_={(a+b)*scale,(a-b)*scale};
   }
   else if(action=="measure"){
     // Reproducible pseudorandom simulation, NOT observation of physical hardware.
     auto signature=digest(std::to_string(clock_)+"/qubit/");
     uint32_t draw=static_cast<uint32_t>(std::stoul(signature.substr(0,8),nullptr,16));
     int outcome=double(draw)/double(UINT32_MAX)<std::norm(a)?0:1;
     qubit_={std::complex<double>(outcome==0?1:0,0),std::complex<double>(outcome==1?1:0,0)};
     return report("QUANTUM SIMULATOR","projective Z measurement = "+std::to_string(outcome)+" (deterministic pseudorandom seed; not hardware)","Ω");
   }
   else if(action!="state")return {false,"QUANTUM OPERATOR","qubit reset | x | z | h | measure | state","⊣",clock_};
   double p0=std::norm(qubit_[0]),p1=std::norm(qubit_[1]);
   return report("QUANTUM / CLASSICAL SIM","P(0)="+fmt(p0)+" P(1)="+fmt(p1)+"; norm="+fmt(p0+p1)+"; gate="+action,"Ω");
 }
 if(op=="matrix"){
   std::array<int32_t,100>a{},b{};for(int i=0;i<100;i++){a[i]=(i*7+3)%11;b[i]=(i%11==0)?1:0;}
   auto r=multiply10(a,b);return report("MATRIX 10 × 10","100 outputs; 1,000 MAC gates; exact identity check "+std::string(a==r.values?"PASS":"FAIL")+"; Π:"+r.signature.substr(0,16),"⊗");
 }
 if(op=="tape"&&v.size()>1){auto path=path10(v[1]);return report("TAPE "+v[1],"Elements "+std::to_string(path.size())+"; path hash "+digest([&]{std::ostringstream o;for(auto i:path)o<<i<<',';return o.str();}()).substr(0,16),"Γ");}
 if(op=="quit"||op=="exit")return {true,"EXIT","Closing GLASS terminal.","۞",clock_};
 // Deterministic no-model English fallback; explicit unknown rather than pretending semantic understanding.
 auto glyphs=graphemes(s);std::ostringstream o;o<<"Λ "<<glyphs.size()<<" code points · Ω:"<<digest(s).substr(0,16)<<" · UNKNOWN SEMANTICS; try help";return report("LETTER ORACLE",o.str(),"Ω");
}
} // namespace glass
