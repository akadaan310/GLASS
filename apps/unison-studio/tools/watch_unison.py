#!/usr/bin/env python3
"""Opt-in bounded source-triggered generation, never a covert background agent."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from compiler.build_demo import build

INPUTS=sorted((ROOT/'examples').glob('*'))
JOURNAL=ROOT/'evidence'/'generator-journal.jsonl'

def digest() -> str:
    sha=hashlib.sha256()
    for path in INPUTS:
        if path.is_file():
            sha.update(path.name.encode());sha.update(b'\0');sha.update(path.read_bytes())
    return sha.hexdigest()

def load_last():
    if not JOURNAL.exists():return None
    try:return json.loads(JOURNAL.read_text().splitlines()[-1])
    except (ValueError,IndexError):return None

def check():
    current=digest();last=load_last()
    if last and last.get('source_sha256')==current:return {'status':'UNCHANGED','cursor':last['sequence']}
    build()
    manifest=ROOT/'public/data/catalog.json'
    record={'schema':'glass.unison.generator-journal/0.1','sequence':int(last['sequence']+1) if last else 1,'source_sha256':current,
            'artifact_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),
            'parent_hash':last.get('hash') if last else None,
            'clock':'logical-generator-revision','status':'SPECIFIED_ARTIFACT_REGENERATED'}
    record['hash']=hashlib.sha256(json.dumps(record,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    JOURNAL.parent.mkdir(parents=True,exist_ok=True)
    with JOURNAL.open('a',encoding='utf-8') as f:f.write(json.dumps(record,sort_keys=True)+'\n');f.flush()
    return {'status':'GENERATED','cursor':record['sequence'],'digest':record['hash']}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--watch',action='store_true',help='Poll for source changes when consciously enabled')
    p.add_argument('--max-polls',type=int,default=120)
    p.add_argument('--interval',type=float,default=2.0)
    a=p.parse_args()
    if not 1<=a.max_polls<=43200 or not .2<=a.interval<=3600:p.error('poll/interval bounds')
    for n in range(a.max_polls if a.watch else 1):
        result=check()
        print(json.dumps(result),flush=True)
        if not a.watch:break
        time.sleep(a.interval)
