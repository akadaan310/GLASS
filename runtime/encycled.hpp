#pragma once
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <map>
#include <optional>
#include <stdexcept>
#include <string>
#include <vector>

namespace glass::encycled {
using Tick = std::uint64_t;
enum class Cause { software_write, clock_edge, device_io, injected_fault, recovery };
inline const char* name(Cause c) {
  switch(c) {
    case Cause::software_write: return "software_write";
    case Cause::clock_edge: return "clock_edge";
    case Cause::device_io: return "device_io";
    case Cause::injected_fault: return "injected_fault";
    case Cause::recovery: return "recovery";
  }
  return "unknown";
}
struct Event {
  Tick sequence;
  Tick tick;
  Tick transaction;
  unsigned bit;
  bool before;
  bool after;
  Cause cause;
};
struct Lifetime { std::string id; Tick start; std::optional<Tick> end; };

class Machine {
 public:
  explicit Machine(unsigned width = 4, std::size_t max_events = 4096)
     : width_(width), max_events_(max_events) {
    if(width==0 || width>63 || max_events==0) throw std::invalid_argument("invalid width or event budget");
  }
  unsigned width() const {return width_;}
  Tick tick() const {return tick_;}
  std::uint64_t word() const {return word_;}
  const std::vector<Event>& events() const {return events_;}
  void advance(Tick dt=1) {
    if(dt==0 || dt>1000000 || tick_>UINT64_MAX-dt) throw std::invalid_argument("invalid clock step");
    tick_+=dt;
  }
  void write_bit(unsigned bit, bool value, Cause cause=Cause::software_write) {
    if(bit>=width_) throw std::out_of_range("bit outside word");
    const auto mask=std::uint64_t{1}<<bit;
    const auto next=value?(word_|mask):(word_&~mask);
    write_word(next,cause);
  }
  void flip_bit(unsigned bit, Cause cause=Cause::software_write) {
    if(bit>=width_) throw std::out_of_range("bit outside word");
    write_word(word_^(std::uint64_t{1}<<bit),cause);
  }
  void write_word(std::uint64_t next, Cause cause=Cause::software_write) {
    const std::uint64_t valid=(std::uint64_t{1}<<width_)-1;
    if((next&~valid)!=0) throw std::out_of_range("word outside width");
    const unsigned changed=__builtin_popcountll(next^word_);
    if(changed>max_events_-events_.size()) throw std::length_error("event budget exceeded");
    if(changed==0) return;
    const auto tx=++transaction_;
    for(unsigned b=0;b<width_;++b){
      const bool prior=((word_>>b)&1u)!=0;
      const bool after=((next>>b)&1u)!=0;
      if(prior!=after) events_.push_back({static_cast<Tick>(events_.size()+1),tick_,tx,b,prior,after,cause});
    }
    word_=next;
  }
  Tick open(const std::string& id) {
    if(id.empty() || id.size()>128 || lifetimes_.count(id)) throw std::invalid_argument("bad or duplicate lifetime identity");
    lifetimes_.emplace(id,Lifetime{id,tick_,std::nullopt});
    return tick_;
  }
  void close(const std::string& id) {
    auto it=lifetimes_.find(id);
    if(it==lifetimes_.end() || it->second.end) throw std::invalid_argument("lifetime missing or closed");
    it->second.end=tick_;
  }
  std::optional<Tick> duration(const std::string& id) const {
    auto it=lifetimes_.find(id);
    if(it==lifetimes_.end()) throw std::out_of_range("unknown identity");
    if(!it->second.end) return std::nullopt;
    return *it->second.end - it->second.start;
  }
  std::uint64_t replay() const {
    std::uint64_t result=0;
    Tick last_seq=0,last_tick=0;
    for(const auto& e:events_){
      if(e.sequence!=last_seq+1||e.tick<last_tick||e.bit>=width_)
        throw std::logic_error("malformed temporal trace");
      const auto mask=std::uint64_t{1}<<e.bit;
      if(((result&mask)!=0)!=e.before || e.before==e.after)
        throw std::logic_error("trace before/after mismatch");
      result^=mask;last_seq=e.sequence;last_tick=e.tick;
    }
    return result;
  }
 private:
  unsigned width_;
  std::size_t max_events_;
  Tick tick_{0}, transaction_{0};
  std::uint64_t word_{0};
  std::vector<Event> events_;
  std::map<std::string,Lifetime> lifetimes_;
};

inline double cycle_residual(double f, double t, double period) {
  if(!std::isfinite(f)||!std::isfinite(t)||!std::isfinite(period)||period<=0)
    throw std::invalid_argument("finite cycle inputs required");
  return f*(t+period)-f*t;
}
inline double integrate_step(const std::vector<std::pair<double,double>>& samples, double end) {
  if(samples.empty()||samples.front().first!=0||!std::isfinite(end)||end<0)
    throw std::invalid_argument("samples must begin at time 0");
  double sum=0.0;
  for(std::size_t i=0;i<samples.size();++i){
    const auto [t,v]=samples[i];
    const double to=(i+1<samples.size()?samples[i+1].first:end);
    if(!std::isfinite(t)||!std::isfinite(v)||to<t||to>end)
      throw std::invalid_argument("nonmonotone or nonfinite samples");
    sum+=v*(to-t);
  }
  return sum;
}
} // namespace glass::encycled
