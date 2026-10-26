#!/usr/bin/env python3
"""GLASS Unison corpus 0.1: deterministic 1000-repo selection and bounded ingestion.

Selection and acquisition are deliberately separate. Source retrieval does not execute
untrusted build scripts. Full fidelity requires a committed git tree + its metadata.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
import urllib.request
import urllib.error
import urllib.parse

TOPICS = [
 ("C","language:C"),("C++","language:C++"),("Rust","language:Rust"),
 ("Go","language:Go"),("Python","language:Python"),("Java","language:Java"),
 ("Kotlin","language:Kotlin"),("TypeScript","language:TypeScript"),
 ("JavaScript","language:JavaScript"),("C#","language:C%23"),
 ("Swift","language:Swift"),("Ruby","language:Ruby"),
 ("PHP","language:PHP"),("Zig","language:Zig"),("Lua","language:Lua"),
 ("Haskell","language:Haskell"),("OCaml","language:OCaml"),
 ("Julia","language:Julia"),("Dart","language:Dart"),("Scala","language:Scala")
]
# 20 language strata x 50 = 1000. Query pages are fixed and deterministic
# after source identities have been snapshotted into the manifest.
TARGET_PER_STRATUM = 50
DEFAULT_REQUEST_SECONDS = 4.0
DEFAULT_CLONE_SECONDS = 30.0

def digest(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()

def http_json(url: str, token: str | None):
    headers = {"Accept":"application/vnd.github+json","User-Agent":"glass-unison-corpus/0.1",
               "X-GitHub-Api-Version":"2022-11-28"}
    if token: headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(url,headers=headers)
    with urllib.request.urlopen(req,timeout=40) as response:
        return json.load(response)

def call_with_backoff(url,token,interval):
    for attempt in range(5):
        try:
            result=http_json(url,token)
            time.sleep(interval)
            return result
        except urllib.error.HTTPError as err:
            if err.code not in (403,429,502,503): raise
            wait=err.headers.get("Retry-After")
            reset=err.headers.get("X-RateLimit-Reset")
            if wait:
                delay=max(1.0,float(wait))
            elif err.headers.get("X-RateLimit-Remaining")=="0" and reset:
                delay=max(1,float(reset)-time.time()+1)
            else:
                delay=60*(2**attempt)
            time.sleep(min(delay,3600))
    raise RuntimeError("GitHub API retries exhausted: "+url)

def select(path,token,interval=DEFAULT_REQUEST_SECONDS):
    seen=set()
    rows=[]
    for label,filter_query in TOPICS:
        count=0
        for page in range(1,6):
            if count>=TARGET_PER_STRATUM:break
            q=filter_query+" stars:>=20 archived:false fork:false size:<50000"
            url="https://api.github.com/search/repositories?"+urllib.parse.urlencode(
                {"q":q,"sort":"stars","order":"desc","per_page":100,"page":page})
            data=call_with_backoff(url,token,interval)
            if data.get("incomplete_results"):raise RuntimeError("incomplete GitHub search: "+label)
            for r in data["items"]:
                name=r["full_name"]
                if name in seen or r.get("disabled") or r.get("archived"):continue
                if not r.get("license"):continue
                seen.add(name)
                rows.append({"index":len(rows),"repository":name,"stratum":label,
                  "github_id":r["id"],"default_branch":r["default_branch"],
                  "clone_url":r["clone_url"],"license_spdx":r["license"].get("spdx_id"),
                  "selection_updated_at":r["updated_at"],"state":"selected"})
                count+=1
                if count>=TARGET_PER_STRATUM:break
            if len(data["items"])<100:break
        if count<TARGET_PER_STRATUM:
            raise RuntimeError("insufficient eligible repositories in "+label+": "+str(count))
    if len(rows)!=1000:raise AssertionError(len(rows))
    manifest={"schema":"glass.unison.corpus/0.1","count":len(rows),
              "policy":{"per_stratum":TARGET_PER_STRATUM,"min_stars":20,
                        "max_size_kb":49999,"forks":False,"archived":False,
                        "license_required":True},
              "repositories":rows}
    serialized=json.dumps(manifest,sort_keys=True,indent=2)+"\n"
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    Path(path).write_text(serialized,encoding="utf-8")
    print("selected",len(rows),"manifest sha256",digest(serialized.encode()))

def run(cmd, timeout):
    return subprocess.run(cmd,capture_output=True,text=True,timeout=timeout,check=True)

def inspect_git_tree(folder, identity):
    head=run(["git","-C",str(folder),"rev-parse","HEAD"],30).stdout.strip()
    listing=run(["git","-C",str(folder),"ls-tree","-r","--full-tree","HEAD"],60).stdout
    source_bytes=listing.encode()
    # Do not infer the bytes of files from git tree output; retain tree hash and metadata.
    return {"schema":"glass.unison.identity/0.1","repository":identity,
      "commit":head,"tree":run(["git","-C",str(folder),"rev-parse","HEAD^{tree}"],30).stdout.strip(),
      "tree_listing_sha256":digest(source_bytes),
      "file_records":len(listing.splitlines())}

def clone(manifest_path, dest, interval, max_count, timeout):
    manifest=json.loads(Path(manifest_path).read_text())
    root=Path(dest).resolve()
    root.mkdir(parents=True,exist_ok=True)
    receipts=root/"receipts.jsonl"
    attempted=0
    for item in manifest["repositories"]:
        if attempted>=max_count:break
        name=item["repository"]
        repo_dir=root/"repos"/name
        receipt_file=root/"evidence"/(str(item["index"]).zfill(4)+".json")
        if receipt_file.exists():continue
        repo_dir.parent.mkdir(parents=True,exist_ok=True)
        receipt_file.parent.mkdir(parents=True,exist_ok=True)
        outcome={"index":item["index"],"repository":name,"status":"failed"}
        try:
            # Metadata-only partial clone, with fixed head subsequently recorded.
            if not repo_dir.exists():
                run(["git","clone","--filter=blob:none","--no-checkout",
                  "--single-branch","--depth","1",item["clone_url"],str(repo_dir)],timeout)
            run(["git","-C",str(repo_dir),"checkout","--force","HEAD"],timeout)
            outcome.update(inspect_git_tree(repo_dir,name))
            outcome["status"]="acquired"
        except (subprocess.CalledProcessError,subprocess.TimeoutExpired,OSError) as error:
            outcome["error"]=str(error)[:1000]
        receipt_file.write_text(json.dumps(outcome,sort_keys=True,indent=2)+"\n")
        with receipts.open("a",encoding="utf-8") as output:
            output.write(json.dumps(outcome,sort_keys=True)+"\n")
        print(item["index"],name,outcome["status"],flush=True)
        attempted+=1
        time.sleep(interval)

def main():
    p=argparse.ArgumentParser()
    subs=p.add_subparsers(dest="command",required=True)
    a=subs.add_parser("select")
    a.add_argument("--manifest",default="corpus/selection.json")
    a.add_argument("--request-interval",type=float,default=DEFAULT_REQUEST_SECONDS)
    b=subs.add_parser("clone")
    b.add_argument("--manifest",default="corpus/selection.json")
    b.add_argument("--destination",default="corpus/acquired")
    b.add_argument("--clone-interval",type=float,default=DEFAULT_CLONE_SECONDS)
    b.add_argument("--limit",type=int,default=10)
    b.add_argument("--timeout",type=int,default=300)
    args=p.parse_args()
    if args.command=="select":
        select(args.manifest,os.environ.get("GITHUB_TOKEN"),max(2.5,args.request_interval))
    else:
        clone(args.manifest,args.destination,max(5.0,args.clone_interval),args.limit,args.timeout)
if __name__=="__main__": main()
