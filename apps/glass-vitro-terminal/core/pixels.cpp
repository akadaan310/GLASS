#include "pixels.hpp"
#include <algorithm>
#include <cmath>
#include <cstdint>
namespace glass {
namespace {
uint32_t hash32(uint32_t x){x^=x>>16;x*=0x7feb352du;x^=x>>15;x*=0x846ca68bu;x^=x>>16;return x;}
double gaussian(double d,double sigma){return std::exp(-d*d/(2*sigma*sigma));}
uint32_t color(double r,double g,double b){auto cv=[](double v)->uint32_t{return static_cast<uint32_t>(std::clamp(v,0.,255.));};return 0xff000000u|(cv(r)<<16)|(cv(g)<<8)|cv(b);}
}
void render_pixels(std::vector<uint32_t>& out,int width,int height,uint64_t phase,bool halted){
 if(width<1||height<1||width>2048||height>2048){out.clear();return;}
 out.resize(size_t(width)*size_t(height));
 const double w=double(width),h=double(height),f=halted?0.:double(phase)*0.017;
 for(int y=0;y<height;y++){
   double ny=(y-h*.48)/std::min(w,h);
   for(int x=0;x<width;x++){
     double nx=(x-w*.5)/std::min(w,h);
     double r=std::sqrt(nx*nx+ny*ny),a=std::atan2(ny,nx);
     uint32_t seed=hash32(uint32_t(x/2)*77999u^uint32_t(y/2)*104729u);
     double star=(seed%32000==1?120:seed%4001==3?46:0);
     // Multiple physical-looking visual structures with explicitly synthetic equations.
     double core=gaussian(r-.29,.015)*92.;
     double orbit=0;
     for(int n=0;n<5;n++){
       double theta=f*(n%2?-0.08:0.1)+n*.37;
       double xr=nx*std::cos(theta)+ny*std::sin(theta);
       double yr=-nx*std::sin(theta)+ny*std::cos(theta);
       double ellipse=std::sqrt((xr*xr)/std::pow(.21+n*.065,2)+(yr*yr)/std::pow(.075+n*.022,2));
       orbit+=gaussian(ellipse-1,.009)*25;
     }
     double phaseWave=std::sin(a*7-f+std::sin(r*19-f*.15));
     double plasma=gaussian(r,.17)*(9.+7.*phaseWave);
     double column=gaussian(nx+0.014*std::sin(ny*15+f),.008)*gaussian(ny,.5)*40;
     double beams=gaussian(std::sin((ny+f*.003)*37+std::sin(nx*17)),-0.0+0.08)*gaussian(nx,.22)*8;
     double vignette=std::clamp(1.-.68*(nx*nx+ny*ny),.04,1.);
     double bright=orbit+core+column+plasma+star+beams;
     out[size_t(y)*width+x]=color((3+bright*.35)*vignette,(12+bright*.98)*vignette,(22+bright*1.15)*vignette);
   }
 }
}
} // namespace glass
