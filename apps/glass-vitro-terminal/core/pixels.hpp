#pragma once
#include <cstdint>
#include <vector>
namespace glass {
// ARGB8888 deterministic synthetic universe raster; O(width*height).
// Origin at viewport center; all color pixels are produced by native code.
void render_pixels(std::vector<uint32_t>& pixels,int width,int height,uint64_t phase,bool halted);
}
