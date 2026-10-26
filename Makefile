CXX ?= g++
CXXFLAGS ?= -std=c++20 -O2 -Wall -Wextra -Werror

.PHONY: all test clean
all: build/glass build/glass-publish
build/glass: runtime/main.cpp runtime/glass.hpp
	mkdir -p build
	$(CXX) $(CXXFLAGS) runtime/main.cpp -o $@
build/kernel-test: tests/kernel.cpp runtime/glass.hpp
	mkdir -p build
	$(CXX) $(CXXFLAGS) tests/kernel.cpp -o $@
build/glass-publish: runtime/publish.cpp runtime/glass.hpp
	mkdir -p build
	$(CXX) $(CXXFLAGS) runtime/publish.cpp -o $@
test: build/kernel-test build/glass-publish
	./build/kernel-test
	sh tests/publisher.sh build/glass-publish
clean:
	rm -f build/glass build/kernel-test
