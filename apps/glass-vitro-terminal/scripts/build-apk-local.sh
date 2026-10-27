#!/usr/bin/env bash
# GLASS ARM64 APK builder: run on an x86_64 Linux PC/VM, no GitHub Actions.
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
ANDROID="$ROOT/android"
DIST="$ROOT/dist"
CACHE="${GLASS_TOOLCHAIN_DIR:-$HOME/.cache/glass-android-toolchain}"
GRADLE_VERSION=8.10.2
BOOTSTRAP=0
INSTALL=0
usage(){
  cat <<'USAGE'
GLASS APK, built directly on Linux/VM — never GitHub Actions or Railway.
  bash scripts/build-apk-local.sh --bootstrap   # downloads missing official SDK + Gradle
  bash scripts/build-apk-local.sh               # existing SDK/Gradle
  bash scripts/build-apk-local.sh --install     # builds and adb-installs on attached phone
JDK 17+, Linux x86_64, Gradle >=8.9, SDK 35, NDK 27.2.12479018, CMake 3.22.1.
Output: dist/GLASS-Vitromaton-arm64-debug.apk and JSON SHA-256 receipt.
Android license acceptance is interactive, never silently automated.
USAGE
}
for arg in "$@"; do case "$arg" in
  --bootstrap) BOOTSTRAP=1;;
  --install) INSTALL=1;;
  --help|-h) usage;exit 0;;
  *) echo "Unknown option $arg" >&2;usage;exit 2;;
esac;done
fail(){ echo "GLASS ERROR: $*" >&2;exit 1; }
for cmd in java python3 unzip;do command -v "$cmd" >/dev/null || fail "Missing $cmd";done
[[ "$(uname -sm)" == "Linux x86_64" ]] || fail "Use an x86_64 Linux VM/PC for official Android SDK build tools."
[[ -f "$ANDROID/app/build.gradle" ]] || fail "Android project missing"
export ANDROID_HOME="${ANDROID_HOME:-${ANDROID_SDK_ROOT:-$HOME/Android/Sdk}}"
export ANDROID_SDK_ROOT="$ANDROID_HOME"
mkdir -p "$CACHE"
download(){
  local url="$1" target="$2"
  command -v curl >/dev/null || fail "curl required for bootstrap"
  if [[ ! -s "$target" ]];then
    curl --fail --location --retry 3 --connect-timeout 20 -o "$target.part" "$url"
    mv "$target.part" "$target"
  fi
}
if ((BOOTSTRAP));then
  mkdir -p "$ANDROID_HOME/cmdline-tools"
  if [[ ! -x "$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager" ]];then
    download "https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip" "$CACHE/commandline-tools.zip"
    mkdir -p "$CACHE/cmdline"
    unzip -qo "$CACHE/commandline-tools.zip" -d "$CACHE/cmdline"
    mkdir -p "$ANDROID_HOME/cmdline-tools/latest"
    cp -a "$CACHE/cmdline/cmdline-tools/." "$ANDROID_HOME/cmdline-tools/latest/"
  fi
  if [[ ! -x "$CACHE/gradle-$GRADLE_VERSION/bin/gradle" ]];then
    download "https://services.gradle.org/distributions/gradle-$GRADLE_VERSION-bin.zip" "$CACHE/gradle-$GRADLE_VERSION-bin.zip"
    unzip -qo "$CACHE/gradle-$GRADLE_VERSION-bin.zip" -d "$CACHE"
  fi
  "$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager" --sdk_root="$ANDROID_HOME" --install \
    'platforms;android-35' 'build-tools;35.0.0' 'ndk;27.2.12479018' 'cmake;3.22.1' \
    || fail "SDK installation failed; accept licenses interactively with sdkmanager --licenses"
fi
[[ -f "$ANDROID_HOME/platforms/android-35/android.jar" ]] || fail "Install Android SDK platform 35, or use --bootstrap"
[[ -d "$ANDROID_HOME/ndk/27.2.12479018" ]] || fail "Install NDK 27.2.12479018, or use --bootstrap"
[[ -d "$ANDROID_HOME/cmake/3.22.1" ]] || fail "Install CMake 3.22.1, or use --bootstrap"
if [[ -x "$ANDROID/gradlew" ]];then GRADLE="$ANDROID/gradlew"
elif [[ -x "$CACHE/gradle-$GRADLE_VERSION/bin/gradle" ]];then GRADLE="$CACHE/gradle-$GRADLE_VERSION/bin/gradle"
elif command -v gradle >/dev/null;then GRADLE="$(command -v gradle)"
else fail "Gradle missing, run with --bootstrap";fi
(cd "$ANDROID" && "$GRADLE" :app:assembleDebug --no-daemon --stacktrace)
SOURCE="$ANDROID/app/build/outputs/apk/debug/app-debug.apk"
[[ -s "$SOURCE" ]] || fail "Gradle finished, but APK missing: $SOURCE"
mkdir -p "$DIST"
TARGET="$DIST/GLASS-Vitromaton-arm64-debug.apk"
cp "$SOURCE" "$TARGET"
PROJECT="$ROOT" APK="$TARGET" python3 - <<'PY'
import datetime, hashlib, json, os, pathlib, subprocess
apk=pathlib.Path(os.environ["APK"])
try: sha=subprocess.check_output(["git","-C",os.environ["PROJECT"],"rev-parse","HEAD"],text=True,stderr=subprocess.DEVNULL).strip()
except (OSError,subprocess.CalledProcessError):sha=None
receipt={"schema":"glass.apk.local/1","filename":apk.name,"bytes":apk.stat().st_size,
         "sha256":hashlib.sha256(apk.read_bytes()).hexdigest(),"abi":"arm64-v8a",
         "mode":"debug","commit":sha,"built_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat()}
(apk.parent/"GLASS-Vitromaton-arm64-debug.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt,indent=2))
PY
if ((INSTALL));then command -v adb >/dev/null || fail "adb not installed";adb install -r "$TARGET";fi
echo "⟦ APK READY ⟧ $TARGET"
