#!/usr/bin/env python3
"""GLASS Unison/0.1: source-preserving, bounded, typed syntax projections.

Real parsers: CPython ast, html.parser, TypeScript compiler AST, Swift compiler parse tree.
The output is *syntax*, not automatic behavioral equivalence or iOS/Android ABI translation.
"""
from __future__ import annotations
import argparse
import ast
from collections import Counter
from dataclasses import asdict, dataclass
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Any

VERSION = 'glass.unison-ir/0.1'
MAX_BYTES = 32_768
MAX_NODES = 640
MAX_DEPTH = 80
MAX_LABEL = 100

class Refusal(ValueError):
    pass


def stable_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


@dataclass
class Node:
    id: str
    kind: str
    label: str
    parent: str | None
    span: str | None
    language: str


class Graph:
    def __init__(self, language: str):
        self.language=language
        self.nodes: list[Node]=[]
        self.features: Counter=Counter()
        self.parser=''
        self.warnings: list[str]=[]

    def add(self, kind: str, label: str='', parent: str | None=None, span: str | None=None) -> str:
        if len(self.nodes)>=MAX_NODES: raise Refusal('node budget exceeded')
        nid=f'n{len(self.nodes):04d}'
        node=Node(nid,kind[:80],str(label)[:MAX_LABEL],parent,span,self.language)
        self.nodes.append(node)
        if label and re.fullmatch(r'[A-Za-z_][\w.]{1,100}', str(label),re.UNICODE):
            self.features[str(label)[:MAX_LABEL]]+=1
        return nid


class HTMLTree(HTMLParser):
    def __init__(self, graph: Graph):
        super().__init__(convert_charrefs=True)
        self.graph=graph
        self.stack: list[tuple[str,str]]=[]
        self.graph.add('document','HTML document')
        self.stack=[('document','n0000')]
    def handle_starttag(self, tag: str, attrs: list[tuple[str,str|None]]) -> None:
        parent=self.stack[-1][1]
        nid=self.graph.add('element',tag,parent,span=str(self.getpos()))
        for k,v in attrs[:25]:
            self.graph.add('attribute',k+('='+v[:35] if v else ''),nid)
        if len(self.stack)>=MAX_DEPTH: raise Refusal('depth budget exceeded')
        if tag not in {'br','img','input','meta','link','hr','source','area','base','embed','param','track','wbr'}:
            self.stack.append((tag,nid))
    def handle_startendtag(self,tag,attrs):
        self.handle_starttag(tag,attrs)
        if self.stack and self.stack[-1][0]==tag: self.stack.pop()
    def handle_endtag(self,tag):
        for j in range(len(self.stack)-1,0,-1):
            if self.stack[j][0]==tag:
                self.stack=self.stack[:j]
                break
    def handle_data(self, data):
        if data.strip(): self.graph.add('text',data.strip()[:MAX_LABEL],self.stack[-1][1])


def parse_python(text: str,g: Graph) -> None:
    tree=ast.parse(text, mode='exec')
    g.parser=f'CPython ast {sys.version_info.major}.{sys.version_info.minor}'
    def walk(t,parent,depth):
        if depth>MAX_DEPTH: raise Refusal('depth budget exceeded')
        if not isinstance(t,ast.AST):return
        label=str(getattr(t,'name',getattr(t,'id',getattr(t,'arg',''))))
        span=f'{getattr(t,"lineno",0)}:{getattr(t,"col_offset",0)}'
        nid=g.add(type(t).__name__,label,parent,span)
        for child in ast.iter_child_nodes(t):walk(child,nid,depth+1)
    walk(tree,None,0)


def parse_html(text: str,g: Graph) -> None:
    g.parser='Python html.parser, HTML syntactic event stream (not a browser DOM)'
    p=HTMLTree(g)
    p.feed(text)
    p.close()


def parse_swift(text:str,g:Graph)->None:
    tool=shutil.which('swiftc')
    if not tool:raise Refusal('swiftc not installed; cannot claim a complete Swift parse')
    with tempfile.TemporaryDirectory(prefix='unison-swift-') as tmp:
        path=Path(tmp)/'source.swift'
        path.write_text(text,encoding='utf-8')
        process=subprocess.run([tool,'-frontend','-dump-parse',str(path)],capture_output=True,text=True,timeout=12,check=False)
    if process.returncode:
        raise Refusal('Swift parser error: '+process.stderr[:350])
    g.parser='swiftc -frontend -dump-parse (Swift parser, not typechecker)'
    # The first source_file expression is the root. Indentation records native parentage.
    stack=[]
    for line in process.stdout.splitlines():
        match=re.match(r'^( *)(\([A-Za-z_][A-Za-z_0-9]*)',line)
        if not match:continue
        indent=len(match.group(1))
        kind=match.group(2)[1:]
        while stack and stack[-1][0]>=indent:stack.pop()
        parent=stack[-1][1] if stack else None
        named=re.search(r'(?:name=|module=)"([^"]+)"',line)
        last_name=re.search(r'"([A-Za-z_][A-Za-z_0-9.()]*)"',line)
        label=(named or last_name).group(1) if (named or last_name) else kind
        src=re.search(r'range=\[([^]]+)\]',line)
        nid=g.add(kind,label,parent,src.group(1).replace(str(path),"<source>")[:100] if src else None)
        stack.append((indent,nid))
    if not g.nodes:raise Refusal('Swift parser produced no nodes')
    # Imports are only a compatibility hint, never evidence of runnable platform semantics.
    imports=re.findall(r'\bimport\s+(\w+)',text)
    if any(x in {'SwiftUI','UIKit','AppKit','Combine'} for x in imports):
        g.warnings.append('Apple framework import: syntax parsed but iOS UI/ABI remains unavailable on Android')


def parse_js(text:str,g:Graph,language:str) -> None:
    runner=Path(__file__).with_name('typescript_ast.cjs')
    p=subprocess.run(['node',str(runner),language],input=text,capture_output=True,text=True,timeout=12)
    if p.returncode:raise Refusal('TypeScript parser error: '+p.stderr[:350])
    data=json.loads(p.stdout)
    g.parser=data['parser']
    for raw in data['nodes']:
        g.add(raw['kind'],raw.get('label',''),raw.get('parent'),raw.get('span'))
    if data.get('diagnostics'):g.warnings.extend(data['diagnostics'][:5])


def parse_java(text:str,g:Graph) -> None:
    if not shutil.which('java'):
        raise Refusal('Java JDK not installed; cannot claim a parsed Android Java tree')
    runner=Path(__file__).with_name('JavaAst.java')
    p=subprocess.run(['java',str(runner)],input=text,capture_output=True,text=True,timeout=20)
    if p.returncode:raise Refusal('Java compiler parser failed: '+p.stderr[:350])
    data=json.loads(p.stdout)
    g.parser=data['parser']
    for n in data['nodes']:
        g.add(n['kind'],n.get('label',''),n.get('parent'),n.get('span'))
    if 'android.' in text:
        g.warnings.append('Android framework imports: syntax parsed without Android SDK API resolution or ART execution')


def build_trie(words: list[str]) -> dict:
    root={}
    for word in words:
        current=root
        for char in word:current=current.setdefault(char,{})
        current['$']=True
    def count(n):return 1+sum(count(v) for k,v in n.items() if k!='$')
    return {'distinct_identifiers':len(words),'prefix_nodes':count(root),'sample':sorted(words)[:12]}


def analyze(language: str, source: str) -> dict:
    if not isinstance(source,str) or len(source.encode('utf-8'))>MAX_BYTES:
        raise Refusal('input exceeds 32 KiB UTF-8 source budget')
    if language not in {'swift','typescript','javascript','python','html','java'}:
        raise Refusal('no trusted parser adapter installed for '+str(language))
    g=Graph(language)
    {'python':parse_python,'html':parse_html,'swift':parse_swift,'java':parse_java}[language](source,g) if language not in {'typescript','javascript'} else parse_js(source,g,language)
    canon=[asdict(n) for n in g.nodes]
    edges=[{'from':n.parent,'to':n.id,'relation':'AST_CHILD'} for n in g.nodes if n.parent is not None]
    features=sorted(g.features)
    node_digest=sha(stable_json(canon).encode())
    return {
        'schema':VERSION,'language':language,'parser':g.parser,'status':'SYNTAX_ONLY','source_sha256':sha(source.encode()),
        'node_digest':node_digest,'nodes':canon,'edges':edges,'trie':build_trie(features),
        'features':g.features.most_common(24),'warnings':g.warnings,
        'nonclaims':['not a CFG/SSA or verified runtime translation','not an executed program','not a platform API equivalence proof']
    }


def main():
    p=argparse.ArgumentParser(description='Bounded source-only compiler to GLASS Unison syntax IR')
    p.add_argument('language',choices=['swift','typescript','javascript','python','html','java'])
    p.add_argument('source',type=Path)
    p.add_argument('--out',type=Path)
    args=p.parse_args()
    source=args.source.read_text(encoding='utf-8')
    result=analyze(args.language,source)
    value=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(value,encoding='utf-8')
        print(f'Wrote {args.out} ({len(result["nodes"])} nodes; {len(result["edges"])} edges)')
    else:print(value)

if __name__=='__main__':
    try:main()
    except (Refusal,subprocess.TimeoutExpired,UnicodeDecodeError,SyntaxError) as e:
        print('UNISON REFUSAL: '+str(e),file=sys.stderr)
        raise SystemExit(2)
