#include "unison.hpp"
#include <algorithm>
#include <atomic>
#include <chrono>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <sstream>
#include <string>
#include <thread>
#include <vector>
#include <sys/ioctl.h>
#include <sys/select.h>
#include <sys/wait.h>
#include <termios.h>
#include <unistd.h>

namespace {
struct Cell {std::string glyph{" "};int color{0};};
class Scene {
 int w{},h{}; std::vector<Cell> grid;
 void dot(int x,int y,const std::string& g,int c){if(x>=1&&x<w-1&&y>=1&&y<h-1)grid[y*w+x]={g,c};}
 void words(int x,int y,const std::string& text,int color){int col=x;for(const auto& ch:glass::Engine::graphemes(text)){if(col>=w-1)break;if(static_cast<uint8_t>(ch[0])<32)continue;dot(col++,y,ch,color);}}
 uint32_t rand_at(int i,int tick){uint32_t n=uint32_t(i)*747796405u+uint32_t(tick)*2891336453u+277803737u;n=((n>>((n>>28)+4))^n)*277803737u;return (n>>22)^n;}
 public:
 Scene(int W,int H):w(W),h(H),grid(w*h){}
 std::string frame(const glass::Engine& engine,const glass::Result& last,const std::string& input,int frameNo){
  std::fill(grid.begin(),grid.end(),Cell{});
  const std::string glyphs[]={"0","1","Λ","Ω","Γ","τ","Π","ج","∅","⊕","۞","α","λ","⟐","◉","↻"};
  for(int i=0;i<std::min(w*h/7,650);i++){
    uint32_t k=rand_at(i,0);int x=1+(int)((k+uint32_t(frameNo)/4)%(w-2)),y=1+(int)(((k>>12)+(frameNo/19)*(1+(i%3)))%(h-2));
    if(i%5==0)dot(x,y,glyphs[(i+frameNo/9)%16],i%4?1:2);
    else dot(x,y,(i%7)?"·":"*",i%8?2:1);
  }
  double t=frameNo*0.034;
  auto cx=w*.5,cy=h*.48;
  // Symbolic orbital field: no claim to astronomical coordinates or physical gravity.
  for(int ring=0;ring<4;ring++){
    double rx=std::min(w*.38,6+ring*3.1),ry=std::min(h*.23,2+ring*1.8);
    for(int i=0;i<130;i++){
      double a=i*6.283185307/130+t*(ring%2?-0.28:0.34);
      int x=int(cx+rx*std::cos(a)),y=int(cy+ry*std::sin(a));
      if((i+ring*7+frameNo/10)%7==0)dot(x,y,"∘",ring%2?2:3);
    }
    double a=t*(1+ring*.27)+ring*1.9;
    dot(int(cx+rx*std::cos(a)),int(cy+ry*std::sin(a)),glyphs[(ring+frameNo/8)%16],4);
  }
  // Perspective glyph tape / simulated continuous universes; cell count adapts to viewport.
  for(int y=3;y<h-3;y++){
    int dy=y-3;
    int x=int(cx+2*std::sin(y*.24+t));
    dot(x,y,glyphs[(dy+frameNo/5)%16],4);
    if(dy%4==0)dot(x+2,y,(dy%8==0?"1":"0"),3);
  }
  for(int x=1;x<w-1;x++){
    dot(x,1,(x+frameNo/3)%17==0?"◉":"─",(x+frameNo)%9?1:4);
    dot(x,h-2,(x+frameNo/3)%19==0?"⟐":"─",(x+frameNo)%9?1:4);
  }
  for(int y=2;y<h-2;y++){
    dot(1,y,glyphs[(y+frameNo/5)%16],2);
    dot(w-2,y,glyphs[(y*3+frameNo/7)%16],2);
  }
  words(4,2,"GLASS  /  UNISON  /  VITROMATON",4);
  words(4,3,"⟦جَ⟧ → ◉ → ⟐ K↔Q → ۞",3);
  if(w>55)words(w-23,2,"PROTOCOL / U-0.1",2);
  int base=std::clamp(int(cy),7,h-11);
  words(4,base-4,"Λ   Ω   Γ   τ   Π",3);
  words(4,base-3,"ALPHABET → GENERATOR",1);
  if(w>60){words(w-28,base-4,"SOURCE → AST → IR",3);words(w-28,base-3,"STATE → TRACE → PROOF",1);}
  words(4,h-11,"◉ "+last.title,4);
  // Render diagnostic text as readable terminal letters, not interactive buttons.
  std::string info=last.detail;for(size_t at=0,y=0;at<info.size()&&y<3;y++){
    size_t take=std::min(size_t(w>14?w-10:25),info.size()-at);
    size_t end=info.rfind(' ',at+take);
    if(end==std::string::npos||end<at)end=at+take;
    words(4,h-10+int(y),info.substr(at,end-at),2);at=end;while(at<info.size()&&info[at]==' ')at++;
  }
  words(4,h-5,"⟐ "+input+(frameNo%8<4?"▏":" "),4);
  words(4,h-3,"τ:"+std::to_string(engine.tick())+" | "+(engine.is_halted()?"HALT":"RUN")+" | D:"+std::to_string(engine.space.coordinates.size())+"  ·  typing is perturbation",1);
  std::ostringstream o;o<<"\033[H";int lastColor=-1;
  for(int y=0;y<h;y++){
   for(int x=0;x<w;x++){
    int c=grid[y*w+x].color;
    if(c!=lastColor){switch(c){case 0:o<<"\033[38;2;22;58;70m";break;case 1:o<<"\033[38;2;51;107;123m";break;case 2:o<<"\033[38;2;89;160;176m";break;case 3:o<<"\033[38;2;111;239;215m";break;case 4:o<<"\033[38;2;208;251;251m";break;}lastColor=c;}
    o<<grid[y*w+x].glyph;
   }
   if(y<h-1)o<<"\r\n";
  }
  o<<"\033[0m";return o.str();
 }
};
struct TtyRaw {
 struct termios old{};bool active{false};
 void enable(){if(active||!isatty(STDIN_FILENO))return;if(tcgetattr(STDIN_FILENO,&old)!=0)return;struct termios raw=old;cfmakeraw(&raw);raw.c_lflag|=ISIG;if(tcsetattr(STDIN_FILENO,TCSAFLUSH,&raw)==0)active=true;}
 void disable(){if(active){tcsetattr(STDIN_FILENO,TCSAFLUSH,&old);active=false;}}
 ~TtyRaw(){disable();}
};
std::pair<int,int> dimensions(){struct winsize ws{};if(ioctl(STDOUT_FILENO,TIOCGWINSZ,&ws)<0||ws.ws_col==0||ws.ws_row==0)return {80,35};return {std::clamp(int(ws.ws_col),30,145),std::clamp(int(ws.ws_row),18,90)};}
int launch_shell(TtyRaw& tty,const std::string& command){
 tty.disable();std::cout<<"\033[0m\033[2J\033[H"<<std::flush;
 const char* path=std::getenv("SHELL");if(!path||!path[0])path=access("/system/bin/sh",X_OK)==0?"/system/bin/sh":"/bin/sh";
 pid_t child=fork();if(child<0)return -1;
 if(child==0){if(command.empty())execl(path,path,"-i",(char*)nullptr);else execl(path,path,"-c",command.c_str(),(char*)nullptr);_exit(127);}
 int status=0;while(waitpid(child,&status,0)<0&&errno==EINTR){};
 std::cout<<"\n[GLASS shell completed: "<<status<<"]\n";tty.enable();std::cout<<"\033[2J"<<std::flush;return status;
}
}
int main(int argc,char**argv){
 using namespace glass;
 std::string journal;const char* home=getenv("HOME");if(home&&home[0])journal=std::string(home)+"/.glass-terminal-events.jsonl";
 Engine engine(journal);Result last{true,"OBSERVING","Λ → Ω → Γ → τ → Π → ۞","◉",engine.tick()};
 if(argc>=3&&std::string(argv[1])=="--eval"){
  auto r=engine.dispatch(argv[2]);std::cout<<r.symbol<<" "<<r.title<<"\n"<<r.detail<<"\n";return r.accepted?0:2;
 }
 if(argc>=2&&std::string(argv[1])=="--batch"){
  std::string line;while(std::getline(std::cin,line)){auto r=engine.dispatch(line);std::cout<<r.symbol<<" "<<r.title<<" | "<<r.detail<<"\n";}return engine.verify()?0:3;
 }
 if(argc>=2&&std::string(argv[1])=="--snapshot"){
  Scene scene(80,36);std::cout<<scene.frame(engine,last,"",20);return 0;
 }
 if(!isatty(STDIN_FILENO)||!isatty(STDOUT_FILENO)){std::cerr<<"GLASS requires a PTY (or use --eval / --batch / --snapshot).\n";return 1;}
 TtyRaw tty;tty.enable();std::cout<<"\033[?1049h\033[?25l\033[2J"<<std::flush;
 std::string input;int frame=0;bool running=true;
 while(running){
  auto [W,H]=dimensions();Scene screen(W,H);std::cout<<screen.frame(engine,last,input,frame++)<<std::flush;engine.render_step();
  fd_set readfds;FD_ZERO(&readfds);FD_SET(STDIN_FILENO,&readfds);timeval tv{0,110000};int ready=select(STDIN_FILENO+1,&readfds,nullptr,nullptr,&tv);
  if(ready<=0)continue;char buf[96];ssize_t n=read(STDIN_FILENO,buf,sizeof(buf));if(n<=0)break;
  for(ssize_t i=0;i<n;i++){
   unsigned char c=static_cast<unsigned char>(buf[i]);
   if(c==3||c==4){running=false;break;}
   if(c==27){if(n==1){running=false;break;}else{while(i+1<n&&buf[i+1]!='\n')i++;continue;}}
   if(c==127||c==8){if(!input.empty()){size_t cut=input.size()-1;while(cut>0&&(static_cast<unsigned char>(input[cut])&0xc0)==0x80)cut--;input.resize(cut);}continue;}
   if(c=='\r'||c=='\n'){
    std::string cmd=input;input.clear();
    if(cmd==":shell"||cmd=="shell"){engine.record("SHELL_OPEN","USER","explicit interactive shell");launch_shell(tty,"");last={true,"SHELL RETURNED","Terminal resumed after real shell session.","۞",engine.tick()};}
    else if(cmd.rfind(":run ",0)==0){engine.record("SHELL_EXEC","USER","explicit command; contents intentionally not journalled");auto rc=launch_shell(tty,cmd.substr(5));last={rc==0,"SHELL FINISHED","Exit status: "+std::to_string(rc),"۞",engine.tick()};}
    else{last=engine.dispatch(cmd);if(cmd=="quit"||cmd=="exit")running=false;}
    continue;
   }
   if(c>=32&&input.size()<1024)input.push_back(char(c));
  }
 }
 std::cout<<"\033[0m\033[?25h\033[?1049l"<<std::flush;tty.disable();return 0;
}
