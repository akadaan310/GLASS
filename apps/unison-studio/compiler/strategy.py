"""Finite, read-only strategy IR; never places trades or evaluates source code."""
from __future__ import annotations
import re

PATTERN=re.compile(r'\AWHEN\s+(SMA|EMA)\(([2-9][0-9]?)\)\s+(CROSS_ABOVE|CROSS_BELOW)\s+(SMA|EMA)\(([2-9][0-9]?)\)\s+THEN\s+SIGNAL\s+(BUY|SELL)\Z',re.I)

class StrategyRefusal(ValueError):pass

def parse_strategy(source: str) -> dict:
    if len(source)>256:raise StrategyRefusal('source length 256 limit')
    match=PATTERN.fullmatch(source.strip())
    if not match:raise StrategyRefusal('grammar: WHEN SMA(3) CROSS_ABOVE SMA(9) THEN SIGNAL BUY')
    left,left_window,rel,right,right_window,side=match.groups()
    left_window,right_window=int(left_window),int(right_window)
    if left_window==right_window:raise StrategyRefusal('distinct windows required')
    return {'schema':'glass.unison.strategy/0.1','operation':'SIGNAL_ONLY','left':{'indicator':left.upper(),'window':left_window},'relation':rel.upper(),'right':{'indicator':right.upper(),'window':right_window},'side':side.upper(),'auth':'simulation_only','executed_orders':0}

def _value(values: list[float], indicator:str, window:int) -> float|None:
    if len(values)<window:return None
    if indicator=='SMA':return sum(values[-window:])/window
    # bounded EMA: initialize with initial SMA and accumulate deterministic float arithmetic
    alpha=2/(window+1)
    acc=sum(values[:window])/window
    for price in values[window:]:acc=alpha*price+(1-alpha)*acc
    return acc

def signal(strategy:dict, prices:list[float]) -> bool:
    if len(prices)<max(strategy['left']['window'],strategy['right']['window'])+1:return False
    def diff(v):
        l=_value(v,**strategy['left']);r=_value(v,**strategy['right'])
        return None if l is None or r is None else l-r
    before,after=diff(prices[:-1]),diff(prices)
    if before is None or after is None:return False
    return (before<=0 and after>0) if strategy['relation']=='CROSS_ABOVE' else (before>=0 and after<0)
