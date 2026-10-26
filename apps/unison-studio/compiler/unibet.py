"""Reversible GLASS glyph *codebook*, not SHA decryption or impossible compression."""
from __future__ import annotations
from collections import Counter
import hashlib
import json
import zlib

class CodebookError(ValueError):pass

def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')

def codebook(sequence:list[str],capacity=256)->dict:
    if len(sequence)>65536:raise CodebookError('token budget')
    freq=Counter(sequence)
    names=[name for name,_ in sorted(freq.items(),key=lambda p:(-p[1],p[0]))[:capacity]]
    mapping={chr(0xE000+i):name for i,name in enumerate(names)}
    reverse={v:k for k,v in mapping.items()}
    glyphs=[reverse.get(x) for x in sequence]
    if any(x is None for x in glyphs):
        raise CodebookError('token outside bounded codebook; no lossy fallback')
    reconstructed=[mapping[x] for x in glyphs]
    if reconstructed!=sequence:raise CodebookError('roundtrip failed')
    capsule={'version':'glass.unibet/0.1','codebook':mapping,'glyphs':' '.join(f'{ord(x):04X}' for x in glyphs)}
    capsule['source_sha256']=hashlib.sha256(canonical(sequence)).hexdigest()
    capsule['capsule_sha256']=hashlib.sha256(canonical(capsule)).hexdigest()
    capsule['utf8_bytes_with_codebook']=len(canonical(capsule))
    capsule['raw_token_json_bytes']=len(canonical(sequence))
    capsule['generic_deflate_bytes']=len(zlib.compress(canonical(sequence),9))
    return capsule

def unpack(capsule:dict)->list[str]:
    raw={k:v for k,v in capsule.items() if k not in {'capsule_sha256','utf8_bytes_with_codebook','raw_token_json_bytes','generic_deflate_bytes'}}
    if hashlib.sha256(canonical(raw)).hexdigest()!=capsule['capsule_sha256']:
        raise CodebookError('tampered capsule')
    c=capsule['codebook']
    try:values=[c[chr(int(t,16))] for t in capsule['glyphs'].split()]
    except (KeyError,ValueError) as exc:raise CodebookError('unknown glyph') from exc
    if hashlib.sha256(canonical(values)).hexdigest()!=capsule['source_sha256']:
        raise CodebookError('data mismatch')
    return values
