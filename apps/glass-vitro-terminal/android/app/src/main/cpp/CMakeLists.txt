cmake_minimum_required(VERSION 3.22.1)
project(glass_ndk LANGUAGES C CXX)
set(CMAKE_CXX_STANDARD 20)
# Use the identical native runtime built and tested on desktop Linux.
add_library(unison_bridge SHARED
    ../../../../../core/unison.cpp
    ../../../../../core/pixels.cpp
    bridge.cpp
    pty.cpp
)
target_include_directories(unison_bridge PRIVATE ../../../../../core)
find_library(log-lib log)
target_link_libraries(unison_bridge ${log-lib})
