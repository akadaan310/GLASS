#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../android"
: "${ANDROID_HOME:?Set ANDROID_HOME to installed Android SDK containing API 36, NDK and CMake}"
if ! command -v gradle >/dev/null; then
  echo "BLOCKED: Gradle >=8.11.1 is not installed; use CI workflow or install in supported Android build host" >&2
  exit 3
fi
if ! test -d "$ANDROID_HOME/ndk/27.2.12479018"; then
  echo "BLOCKED: NDK 27.2.12479018 not installed in SDK" >&2
  exit 3
fi
gradle :app:assembleDebug --no-daemon
ls -lh app/build/outputs/apk/debug/app-debug.apk
