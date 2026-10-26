#!/usr/bin/env python3
"""Source-linked deterministic generation, explicit parser provenance, no code execution."""
from __future__ import annotations
from pathlib import Path
import hashlib
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from compiler.unison_ir import analyze
from compiler.strategy import parse_strategy, signal
from compiler.unibet import codebook, unpack

SOURCES={
 'swift':'Counter.swift','swiftui':'CounterUI.swift',
 'web':'Shell.html','typescript':'Strategy.ts','python':'LeanStrategy.py','java':'AndroidActivity.java'
}
LANG={'swift':'swift','swiftui':'swift','web':'html','typescript':'typescript','python':'python','java':'java'}
STRATEGY='WHEN SMA(3) CROSS_ABOVE SMA(9) THEN SIGNAL BUY'

def build():
    out=ROOT/'public'/'data';out.mkdir(parents=True,exist_ok=True)
    manifest={}
    label_sequence=[]
    for key,name in SOURCES.items():
        src=ROOT/'examples'/name
        result=analyze(LANG[key],src.read_text(encoding='utf-8'))
        target=out/f'ir-{key}.json'
        target.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n',encoding='utf-8')
        manifest[key]={'title':key.upper(),'language':LANG[key],'node_count':len(result['nodes']),'edge_count':len(result['edges']),'source_hash':result['source_sha256'],'parser':result['parser'],'warnings':result['warnings'],'path':'/data/'+target.name}
        label_sequence.extend(n['kind'] for n in result['nodes'])
    strategy=parse_strategy(STRATEGY)
    strategy['fixture']={'prices':[10]*10+[1]*9+[30],'triggered':signal(strategy,[10]*10+[1]*9+[30])}
    (out/'strategy.json').write_text(json.dumps(strategy,indent=2)+'\n',encoding='utf-8')
    caps=codebook(label_sequence)
    assert unpack(caps)==label_sequence
    (out/'unibet.json').write_text(json.dumps(caps,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    cat={'schema':'glass.unison.catalog/0.1','scope':'syntactic + synthetic, no OS translation or live orders','sources':manifest,'strategy':'/data/strategy.json','codebook':'/data/unibet.json','owner_source':'GLASS/main Unison 005'}
    (out/'catalog.json').write_text(json.dumps(cat,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'entries':len(manifest),'nodes':sum(v['node_count'] for v in manifest.values()),'codebook_letters':len(caps['codebook']),'strategy_fixture':strategy['fixture'],'complete':True},indent=2))

if __name__=='__main__':build()
