#!/usr/bin/env python3
"""Build an independently signed, Java-only GLASS UNISON Android APK.

No native NDK or Gradle required; official Android SDK platform/build tools
are used directly, same approach as SURFACE's pinned build system. Requires
Android SDK platform 35/36, build-tools 35/36, Java 17+ and Python 3.11+.

Local developer signing key is generated under build/ only if no --keystore
is supplied. The secret NEVER enters Git or a release ZIP. Different ephemeral
keys produce APKs that cannot update each other; this is a preview build.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
import zipfile

ROOT=Path(__file__).resolve().parents[1]
def call(argv:list[str], *, timeout=180)->None:
    print("RUN", " ".join(str(x) for x in argv[:5]), "...", flush=True)
    subprocess.run([str(x) for x in argv], cwd=ROOT, check=True, timeout=timeout)

def resolve_sdk(sdk:Path)->tuple[Path,Path]:
    platforms=sorted((sdk/"platforms").glob("android-*"),key=lambda p:int(p.name.split("-")[-1]))
    builds=sorted((sdk/"build-tools").glob("*"),key=lambda p:tuple(int(n) for n in p.name.split(".") if n.isdigit()))
    if not platforms or not builds:raise RuntimeError("Official Android SDK platform and build-tools required")
    android_jar=platforms[-1]/"android.jar"
    if not android_jar.is_file():raise RuntimeError("Missing android.jar")
    return android_jar,builds[-1]

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--sdk-root",type=Path,required=True)
    ap.add_argument("--keystore",type=Path)
    ap.add_argument("--output",type=Path,default=ROOT/"build"/"Glass-UNISON-Live.apk")
    args=ap.parse_args()
    sdk=args.sdk_root.resolve()
    jar,tools=resolve_sdk(sdk)
    build=ROOT/"build";classes=build/"classes";dex=build/"dex";build.mkdir(exist_ok=True,parents=True)
    classes.mkdir(exist_ok=True);dex.mkdir(exist_ok=True)
    sources=sorted((ROOT/"src").rglob("*.java"))
    if len(sources)<7:raise RuntimeError("Incomplete Glass Java source tree")
    java=shutil.which("javac")
    if not java:raise RuntimeError("Java compiler unavailable")
    call([java,"--release","11","-cp",str(jar),"-d",str(classes),*[str(x) for x in sources]],timeout=90)
    # D8 dexes the Java bytecode into a universal ABI-independent application.
    call([str(tools/"d8"),"--min-api","29","--lib",str(jar),"--output",str(dex),
          *[str(x) for x in sorted(classes.rglob("*.class"))]],timeout=120)
    if not (dex/"classes.dex").is_file():raise RuntimeError("D8 produced no classes.dex")
    unsigned=build/"glass-unsigned.apk";aligned=build/"glass-aligned.apk"
    call([str(tools/"aapt2"),"link","-I",str(jar),"--manifest",
          str(ROOT/"AndroidManifest.xml"),"--min-sdk-version","29","--target-sdk-version","35",
          "-o",str(unsigned)],timeout=70)
    with zipfile.ZipFile(unsigned,"a",zipfile.ZIP_DEFLATED,6) as z:
        z.write(dex/"classes.dex","classes.dex")
    call([str(tools/"zipalign"),"-f","-p","4",str(unsigned),str(aligned)])
    signing=(args.keystore or build/"glass-dev-only.jks").resolve()
    if not signing.is_file():
        call(["keytool","-genkeypair","-keystore",str(signing),"-storepass","android",
              "-keypass","android","-alias","glass-dev","-keyalg","RSA","-keysize","3072",
              "-validity","3650","-dname","CN=GLASS Development, O=GLASS, C=US","-noprompt"],timeout=80)
    target=args.output.resolve();target.parent.mkdir(parents=True,exist_ok=True)
    call([str(tools/"apksigner"),"sign","--ks",str(signing),"--ks-key-alias","glass-dev",
          "--ks-pass","pass:android","--key-pass","pass:android","--out",str(target),str(aligned)],timeout=60)
    call([str(tools/"apksigner"),"verify","--verbose","--print-certs",str(target)],timeout=60)
    call([str(tools/"zipalign"),"-c","-v","4",str(target)],timeout=60)
    digest=hashlib.sha256(target.read_bytes()).hexdigest()
    receipt={
      "artifact":str(target.relative_to(ROOT)) if target.is_relative_to(ROOT) else str(target),
      "sha256":digest,"bytes":target.stat().st_size,
      "package":"org.glass.unison","application":"GLASS UNISON Live",
      "min_api":29,"target_api":35,"architecture":"universal-Java-only",
      "mic":"explicit user action, RECORD_AUDIO, no background service",
      "autoplay":False,"network":"explicit opt-in HTTPS private derived events only",
      "on_device_recognizer":"optional and only if OS provides an installed on-device service",
      "muqri_ctc_tajwid":"not embedded",
      "signature":"ephemeral development key; NOT production/release signing",
      "build_evidence":"javac+D8+aapt2+zipalign+apksigner completed; on-device launch separate",
      "built_utc":int(time.time())
    }
    receipt_file=build/"GLASS_APK_RECEIPT.json"
    receipt_file.write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps(receipt,indent=2))
    return 0

if __name__=="__main__":
    try:sys.exit(main())
    except (RuntimeError,subprocess.CalledProcessError,subprocess.TimeoutExpired) as e:
        print(f"GLASS APK BUILD FAILED: {e}",file=sys.stderr);sys.exit(1)
