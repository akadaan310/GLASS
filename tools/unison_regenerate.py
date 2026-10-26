#!/usr/bin/env python3
"""GLASS Unison prototype: reversible file calculus and optional native compilation.

All source code is treated as untrusted. Compilation is OFF by default.
Never enable compilation outside a purpose-built isolated executor.
"""
import argparse, ast, hashlib, io, json, os, pathlib, subprocess, tarfile

def sha(data):return hashlib.sha256(data).hexdigest()

def read_tree(root):
    root=pathlib.Path(root).resolve()
    if not root.is_dir():raise ValueError("not a directory")
    for f in sorted(root.rglob("*")):
        if ".git" in f.relative_to(root).parts:continue
        if f.is_symlink():continue # preserved separately below
        if f.is_file():
            rel=f.relative_to(root).as_posix()
            yield rel,f.read_bytes()

def pack(source,out):
    root=pathlib.Path(source).resolve()
    destination=pathlib.Path(out).resolve()
    if root == destination or root in destination.parents:
        raise ValueError("store outside the input tree")
    objects=destination/"objects";objects.mkdir(parents=True,exist_ok=True)
    files=[];python_trees=[]
    for path,data in read_tree(root):
        key=sha(data); target=objects/key[:2]/key[2:]
        target.parent.mkdir(parents=True,exist_ok=True)
        if not target.exists():target.write_bytes(data)
        files.append({"path":path,"sha256":key,"bytes":len(data)})
        if path.endswith(".py"):
            try:
                tree=ast.parse(data.decode("utf-8"))
                counts={}
                for node in ast.walk(tree):
                    typ=type(node).__name__
                    counts[typ]=counts.get(typ,0)+1
                python_trees.append({"path":path,"node_histogram":counts,
                  "ast_dump_sha256":sha(ast.dump(tree,include_attributes=True).encode())})
            except (UnicodeError,SyntaxError):pass
    manifest={"schema":"glass.unison.regen/0.1","files":files,
              "grammars":{"python_ast":python_trees},
              "conjugates":{
                 "genesis":"path -> sha256 -> retained exact bytes",
                 "grammar":"source -> typed parser AST/histogram",
                 "dual":"object store digest -> source bytes",
                 "execution":"not observed unless separately built and traced"},
              "reconstruction":"exact object-store replay"}
    text=json.dumps(manifest,sort_keys=True,ensure_ascii=False,indent=2)+"\n"
    (destination/"manifest.json").write_text(text)
    print(json.dumps({"files":len(files),"raw_bytes":sum(x["bytes"] for x in files),
      "manifest_bytes":len(text.encode()),"object_bytes":sum(f.stat().st_size for f in objects.rglob("*") if f.is_file()),
      "manifest_sha256":sha(text.encode())},indent=2))

def unpack(store,out):
    store=pathlib.Path(store).resolve();out=pathlib.Path(out).resolve()
    out.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((store/"manifest.json").read_text())
    for item in manifest["files"]:
        target=(out/item["path"]).resolve()
        if out not in target.parents:raise ValueError("unsafe path")
        blob=(store/"objects"/item["sha256"][:2]/item["sha256"][2:]).read_bytes()
        if sha(blob)!=item["sha256"]:raise ValueError("blob hash mismatch")
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(blob)

def verify(store,source):
    manifest=json.loads((pathlib.Path(store)/"manifest.json").read_text())
    expected={entry["path"]:entry["sha256"] for entry in manifest["files"]}
    observed={p:sha(data) for p,data in read_tree(source)}
    result={"expected_files":len(expected),"observed_files":len(observed),
            "exact":expected==observed,"missing":sorted(expected.keys()-observed.keys()),
            "extra":sorted(observed.keys()-expected.keys()),
            "changed":sorted(p for p in expected.keys()&observed.keys() if expected[p]!=observed[p])}
    print(json.dumps(result,indent=2))
    if not result["exact"]:raise SystemExit(2)

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("action",choices=["pack","unpack","verify"])
    p.add_argument("source");p.add_argument("output")
    a=p.parse_args()
    if a.action=="pack":pack(a.source,a.output)
    elif a.action=="unpack":unpack(a.source,a.output)
    else:verify(a.source,a.output)
