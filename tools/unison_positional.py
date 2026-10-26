#!/usr/bin/env python3
"""UNISON/0.1: positional tapes, explicit nulls, cyclic operators and landscape probes.
A research automaton, not a claim about physical quantum stars.
"""
from __future__ import annotations
import argparse, hashlib, json, math

NULL = object()
def digits(n:int, base:int=10)->tuple[int,...]:
    if n<0 or base<2: raise ValueError("nonnegative number, base >= 2")
    out=[0] if not n else []
    while n: out.append(n%base);n//=base
    return tuple(reversed(out))
def value(tape,base=10):
    v=0
    for x in tape:
        if not isinstance(x,int) or not 0<=x<base:raise ValueError("invalid digit")
        v=v*base+x
    return v
def rotate(tape,k=1):
    if not tape:return tape
    k%=len(tape)
    return tuple(tape[k:])+tuple(tape[:k])
def successor(tape,base=10):
    if not tape:return (1,)
    out=list(tape);carry=1
    for i in range(len(out)-1,-1,-1):
        x=out[i]+carry;out[i]=x%base;carry=x//base
        if not carry:break
    return tuple(([carry] if carry else [])+out)
def tape_trace(start:int,count:int,base:int=10):
    tape=digits(start,base)
    for tick in range(count):
        yield {"tick":tick,"tape":list(tape),"value":value(tape,base),
          "rotation":list(rotate(tape)),"reverse":list(reversed(tape)),
          "parity":sum(tape)%2,"signature":hashlib.sha256(
             (f"{base}:"+",".join(map(str,tape))).encode()).hexdigest()[:16]}
        tape=successor(tape,base)
def sphere(x,y):return x*x+y*y
def rastrigin(x,y):return 20+x*x+y*y-10*(math.cos(2*math.pi*x)+math.cos(2*math.pi*y))
def ackley(x,y):
    return -20*math.exp(-0.2*math.sqrt((x*x+y*y)/2))-math.exp(
      (math.cos(2*math.pi*x)+math.cos(2*math.pi*y))/2)+20+math.e
FUNCTIONS={"sphere":sphere,"rastrigin":rastrigin,"ackley":ackley}
def landscape(name="rastrigin",side=51,extent=5.0,delta=0.01):
    if side<3:raise ValueError("side >= 3")
    f=FUNCTIONS[name];grid=[]
    for iy in range(side):
        y=extent*(2*iy/(side-1)-1)
        row=[]
        for ix in range(side):
            x=extent*(2*ix/(side-1)-1)
            v=f(x,y)
            grad=((f(x+delta,y)-f(x-delta,y))/(2*delta),
                  (f(x,y+delta)-f(x,y-delta))/(2*delta))
            # contour quantization is a declared profile, not the original function.
            row.append({"x":round(x,7),"y":round(y,7),"f":round(v,9),
                 "g":round(math.hypot(*grad),9),"contour":math.floor(v)})
        grid.append(row)
    candidates=[]
    for iy in range(1,side-1):
        for ix in range(1,side-1):
            cur=grid[iy][ix]
            if all(cur["f"]<=grid[iy+dy][ix+dx]["f"] for dx,dy in
                   ((-1,0),(1,0),(0,-1),(0,1))):
                candidates.append(cur)
    candidates.sort(key=lambda c:(c["f"],c["x"],c["y"]))
    contour_hist={}
    for row in grid:
        for cell in row:
            z=str(cell["contour"]);contour_hist[z]=contour_hist.get(z,0)+1
    return {"function":name,"side":side,"extent":extent,"sampled_local_minima":candidates[:32],
       "sampled_minimum":min((c for row in grid for c in row),key=lambda c:c["f"]),
       "contour_occupancy":contour_hist,"note":"sampled grid, not global proof"}
def typed_state(kind,value_=None):
    if kind=="NULL":return {"tag":"NULL","present":False}
    if kind=="ZERO":return {"tag":"NUMBER","present":True,"value":0}
    if kind=="ONE":return {"tag":"NUMBER","present":True,"value":1}
    if kind=="EMPTY":return {"tag":"STRING","present":True,"value":""}
    return {"tag":kind,"present":True,"value":value_}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--start",type=int,default=8);p.add_argument("--count",type=int,default=6)
    p.add_argument("--base",type=int,default=10);p.add_argument("--function",choices=FUNCTIONS,default="rastrigin")
    p.add_argument("--side",type=int,default=31)
    a=p.parse_args()
    print(json.dumps({"schema":"glass.unison.positional/0.1",
      "states":[typed_state(s) for s in ("NULL","ZERO","ONE","EMPTY")],
      "tape":list(tape_trace(a.start,a.count,a.base)),
      "landscape":landscape(a.function,a.side)},ensure_ascii=False,indent=2))
if __name__=="__main__":main()
