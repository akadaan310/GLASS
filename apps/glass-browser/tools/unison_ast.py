#!/usr/bin/env python3
"""Unison finite AST generator calculus: deterministic, replayable program families.

100,000 denotes a deterministic addressable combination space, not 100,000
pre-written independent algorithms. Every family derives from a typed grammar.
"""
from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
import argparse, json

OPERATORS = ("add","sub","mul","xor","and","or","shl","shr","eq","lt")
WIDTHS = (1,2,4,8,16,32,64,128,256,512)
CONTEXTS = ("scalar","vector","matrix","register","clock","event","address","arabic","css","dom")
STRATEGIES = ("direct","reverse","fold","scan","tree","memo","lazy","parallel","bitwise","symbolic")
# 10 x 10 x 10 x 10 = 10,000; include ten time-phase selectors => 100,000.
PHASES = tuple(range(10))
SPACE=len(OPERATORS)*len(WIDTHS)*len(CONTEXTS)*len(STRATEGIES)*len(PHASES)
@dataclass(frozen=True)
class Address:
    id:int
    operator:str
    width:int
    context:str
    strategy:str
    phase:int

def decode(index:int)->Address:
    if not 0<=index<SPACE: raise ValueError("generator id out of range")
    original=index
    phase=index%10;index//=10
    strategy=STRATEGIES[index%10];index//=10
    context=CONTEXTS[index%10];index//=10
    width=WIDTHS[index%10];index//=10
    return Address(original,OPERATORS[index],width,context,strategy,phase)

def ast(index:int)->dict:
    a=decode(index)
    node={"kind":"UnisonOperation","schema":"glass.unison.ast/0.1",
          "address":a.id,"operator":a.operator,"width":a.width,
          "context":a.context,"strategy":a.strategy,"phase":a.phase,
          "inputs":[{"kind":"Variable","name":"a","width":a.width},
                    {"kind":"Variable","name":"b","width":a.width}],
          "clock":{"kind":"LogicalPhase","value":a.phase}}
    payload=json.dumps(node,sort_keys=True,separators=(",",":"))
    node["digest"]="sha256:"+sha256(payload.encode()).hexdigest()
    return node

def execute_integer(index:int,a:int,b:int)->int|bool:
    t=decode(index)
    mask=(1<<t.width)-1
    a&=mask;b&=mask
    # Numeric fixture semantics only. Strategy/context remain unimplemented research descriptors.
    match t.operator:
        case "add": return (a+b)&mask
        case "sub": return (a-b)&mask
        case "mul": return (a*b)&mask
        case "xor": return a^b
        case "and": return a&b
        case "or": return a|b
        case "shl": return (a<<b)&mask
        case "shr": return a>>b
        case "eq": return a==b
        case "lt": return a<b
    raise AssertionError(t.operator)

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("id",type=int,nargs="?",default=0)
    p.add_argument("--space",action="store_true")
    args=p.parse_args()
    print(SPACE if args.space else json.dumps(ast(args.id),ensure_ascii=False,indent=2))
