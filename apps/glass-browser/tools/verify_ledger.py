#!/usr/bin/env python3
"""Offline verifier of the private GLASS JSONL journal after owner-directed export.
File is not signed: hash chaining identifies inconsistent edits, not a hostile rewriter.
"""
import hashlib
import json
import struct
import sys
from pathlib import Path

def verify(path: Path):
    prev=bytes(32)
    rows=0
    gaps=0
    for line in path.read_text(encoding='utf-8').splitlines():
        obj=json.loads(line)
        body=json.dumps(obj['event'],ensure_ascii=False,separators=(',',':'))
        # Original Android event JSON is embedded unchanged in the JSONL row,
        # so slice the original substring rather than serializing as reordered JSON.
        marker='"event":'
        at=line.index(marker)+len(marker)
        raw=line[at:-1].encode('utf-8')
        observed=hashlib.sha256(prev+struct.pack('>I',len(raw))+raw).hexdigest()
        if observed!=obj['hash']:
            raise ValueError('hash mismatch at row '+str(rows+1))
        prev=bytes.fromhex(observed)
        rows+=1
        if obj['event'].get('kind','').endswith('GAP'):
            gaps+=1
    return {'schema':'glass.journal.verify/0.1','records':rows,'gaps':gaps,'sha256_tail':prev.hex(),'status':'CHAIN_CONSISTENT_UNAUTHENTICATED'}

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('usage: python tools/verify_ledger.py exported-glass-events-v1.jsonl')
    print(json.dumps(verify(Path(sys.argv[1])),indent=2))
