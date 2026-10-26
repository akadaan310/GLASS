#pragma once
#include <array>
#include <cstdint>
#include <complex>
#include <map>
#include <string>
#include <vector>

namespace glass {
constexpr const char* VERSION = "VITROMATON/0.1";
struct Event {
  uint64_t tick{};
  uint64_t monotonic_ns{};
  std::string kind, source, detail, previous, digest;
};
struct Result {
  bool accepted{true};
  std::string title, detail, symbol;
  uint64_t tick{};
};
struct MatrixOp {
  int row{}, col{}, k{};
  int32_t lhs{}, rhs{}, before{}, after{};
};
struct MatrixResult {
  std::array<int32_t, 100> values{};
  std::vector<MatrixOp> trace;
  std::string signature;
};
struct NDim {
  std::vector<double> coordinates;
  bool translate(size_t axis, double delta);
  bool rotate(size_t p, size_t q, double radians);
  double radius() const;
};
struct Oracle {
  std::string kind, alphabet, op, address;
  std::vector<std::string> glyphs;
};
class Engine {
public:
  explicit Engine(std::string journal="");
  Result dispatch(const std::string& input);
  std::string snapshot() const;
  const std::vector<Event>& events() const { return events_; }
  bool verify() const;
  void record(const std::string& kind, const std::string& source, const std::string& detail);
  void render_step();
  bool is_halted() const { return halted_; }
  uint64_t tick() const { return clock_; }
  NDim space;
  static uint32_t bit_gate(uint32_t lhs, uint32_t rhs, const std::string& gate);
  static MatrixResult multiply10(const std::array<int32_t,100>& a, const std::array<int32_t,100>& b);
  static std::vector<int> path10(const std::string& shape);
  static std::string digest(const std::string& message);
  static std::string encode_uri(const std::string& text);
  static std::vector<std::string> graphemes(const std::string& bytes);
  static bool decode_uint(const std::string& value, uint32_t& output);
  static std::vector<std::string> split(const std::string& input);
private:
  Result report(const std::string& title,const std::string& detail,const std::string& glyph="Ω");
  std::string journal_;
  std::vector<Event> events_;
  uint64_t clock_{0};
  bool halted_{false};
  uint64_t render_frames_{0};
  std::string last_digest_{64,'0'};
  std::string last_input_;
  std::array<std::complex<double>,2> qubit_{{{1.0,0.0},{0.0,0.0}}};
};
} // namespace glass
