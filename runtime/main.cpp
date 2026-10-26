#include "glass.hpp"
#include <iostream>
int main(int argc,char** argv){
 try{
  glass::require(argc>=3,"glass spell TEXT | glass JOURNAL state|weight|CURSOR COMMAND ARGUMENTS");
  if(std::string(argv[1])=="spell"){std::cout<<glass::spell(argv[2])<<'\n';return 0;}
  glass::Journal journal(argv[1]);std::string op=argv[2];
  if(op=="state")std::cout<<"{\"cursor\":"<<journal.cursor()<<",\"configuration\":"<<journal.machine.state()<<"}\n";
  else if(op=="weight")std::cout<<journal.machine.weight()<<'\n';
  else{
   glass::require(op.size()>0&&std::all_of(op.begin(),op.end(),[](char c){return c>='0'&&c<='9';}),"cursor must be a decimal integer");
   glass::Words command;for(int i=3;i<argc;++i)command.push_back(argv[i]);
   journal.submit(command,std::stoull(op));
   std::cout<<"{\"cursor\":"<<journal.cursor()<<",\"configuration\":"<<journal.machine.state()<<"}\n";
  }return 0;
 }catch(const std::exception& e){std::cerr<<"glass: "<<e.what()<<'\n';return 2;}
}
