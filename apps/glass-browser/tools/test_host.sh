#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p build
c++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -pthread tests/test_core.cpp -o build/test_core
./build/test_core
cc -std=c11 -O2 -Wall -Wextra -Wpedantic -fPIC -shared core/glass_gate_bit.c -o build/libglass_gate_bit.so
c++ -std=c++20 -O2 -Wall -Wextra -Wpedantic tests/test_gate.cpp -ldl -o build/test_gate
./build/test_gate "$(pwd)/build/libglass_gate_bit.so"
python3 -m unittest discover -s tests -p 'test_*.py' -v
