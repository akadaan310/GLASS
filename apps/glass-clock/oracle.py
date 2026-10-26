"""GLASS Clock Oracle 0.1 — bounded symbolic grammar and truthful clock models.

Civil zones are IANA political/rule systems. Longitude gives mean SOLAR
coordinate (4 minutes per degree east). Latitude influences solar elevation.
No arbitrary shell execution or location service is used.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError, available_timezones
import json
import math
import re
import time
from typing import Any

VERSION='glass.clock-oracle/0.1'
START_MONO_NS=time.monotonic_ns()
MAX_INPUT=2048
MAX_OPS=24
MAX_ZONE_LIST=8
ALLOWED_ZONES=available_timezones() | {'UTC'}
OP_META={
 '۞':('DEVICE CLOCK','Client-reported wall-clock reading; if unavailable, UNKNOWN.','clock_device'),
 '⊕':('UTC ORIGIN','A sampled server UTC instant; POSIX timestamp ignores leap-second labels.','clock_utc'),
 '⌛':('SERVER CLOCK','Server wall time sampled near this response; clock synchronization not assumed.','clock_server'),
 '◷':('MONOTONIC CLOCK','Elapsed time since GLASS Python process start; arbitrary epoch, never civil time.','clock_monotonic'),
 '∅':('NON-TIME','An explicitly unobserved interval or unavailable clock value, not mathematical zero.','clock_unknown'),
 '⟳':('CIVIL ZONE ROTOR','IANA political zone rules including DST and historical changes; not derived from longitude.','zones'),
 '⌖':('EARTH COORDINATE','Latitude/longitude point, unit-sphere vector and its 15° geometric wedge.','geo'),
 '☼':('SOLAR TIME','Mean solar time from longitude plus NOAA approximate equation of time and elevation.','solar'),
 '∆':('OFFSET DIFFERENCE','Difference between legal UTC offsets of two IANA zones at one instant.','difference'),
 'ϕ':('CYCLE PHASE','Phase 2π·((monotonic elapsed mod period)/period); logical periodic observable.','phase'),
 'λ':('SHELL GENERATOR','Compiles the following admitted clock operator into a safe teaching shell script; never runs it.','script'),
 '⟦':('FRAME BEGIN','Explicit group boundary; does not change clock values.','frame_open'),
 '⟧':('FRAME END','Closes a source-linked group.','frame_close'),
}
TUTORIAL=[
 ('۞','Read the client device clock'),('⊕','Read UTC at the host'),('⌛','Read the server wall clock'),
 ('◷','Inspect the monotonic process clock'),('⟳[America/New_York,Asia/Dubai]','Resolve two IANA zones'),
 ('⌖[0,45]','Place a point on Earth (latitude,longitude)'),('☼[0,45]','Approximate solar clock and sun altitude'),
 ('∆[America/New_York,Asia/Dubai]','Compare two legal zone offsets'),
 ('ϕ[60]','Represent a one-minute cycle as a phase'),
 ('λ⟳[Asia/Dubai]','Learn a safe shell script for one operator'),('∅','Represent an unavailable clock value'),
]
ZONE_SHOWCASE=['UTC','America/Los_Angeles','America/New_York','Europe/London',
 'Africa/Cairo','Asia/Dubai','Asia/Kolkata','Asia/Kathmandu','Asia/Tokyo',
 'Australia/Sydney','Pacific/Auckland','Pacific/Chatham']

class ClockRefusal(ValueError):pass

@dataclass(frozen=True)
class Expr:
 op:str
 args:tuple[str,...]
 source:str
 start:int
 end:int
 child:'Expr|None'=None
 def as_dict(self,whole:str)->dict:
  return {'op':self.op,'label':OP_META[self.op][0], 'args':list(self.args),'source':self.source,
          'char_span':[self.start,self.end],
          'byte_span':[len(whole[:self.start].encode()),len(whole[:self.end].encode())],
          'child':self.child.as_dict(whole) if self.child else None}

class Parser:
 def __init__(self,source:str):
  if not isinstance(source,str) or len(source)>MAX_INPUT:raise ClockRefusal('Source budget: at most 2048 characters')
  self.source=source;self.i=0;self.n=len(source)
 def skip(self)->None:
  while self.i<self.n and (self.source[self.i].isspace() or self.source[self.i] in ';·'):
   self.i+=1
 def parse(self)->list[Expr]:
  out=[];frames=0
  while True:
   self.skip()
   if self.i==self.n:break
   e=self.parse_one(0)
   if e.op=='⟦':frames+=1
   if e.op=='⟧':frames-=1
   if frames<0 or frames>8:raise ClockRefusal('Unmatched ⟦/⟧ frame')
   out.append(e)
   if len(out)>MAX_OPS:raise ClockRefusal('Maximum 24 operators per program')
  if frames:raise ClockRefusal('Unclosed ⟦ frame')
  return out
 def parse_one(self,depth:int)->Expr:
  if depth>3:raise ClockRefusal('Generator nesting limit')
  self.skip()
  start=self.i
  if self.i>=self.n:raise ClockRefusal('Missing symbol operand')
  op=self.source[self.i]
  if op not in OP_META:raise ClockRefusal('GLASS takes operator symbols only. Tap ۞, ⟳ or λ; use names/numbers inside [ ].')
  self.i+=1
  if op=='λ':
   child=self.parse_one(depth+1)
   if child.op in ('λ','⟦','⟧','∅'):
    raise ClockRefusal('λ accepts one executable clock/coordinate operator, not a frame or λ itself')
   return Expr(op,(),self.source[start:self.i],start,self.i,child)
  args=()
  if op in ('⟳','⌖','☼','∆','ϕ'):
   if self.i>=self.n or self.source[self.i]!='[':
    raise ClockRefusal(f'{op} requires [operands]')
   self.i+=1;begin=self.i
   while self.i<self.n and self.source[self.i]!=']':
    if self.source[self.i] in '[\x00\r\n':raise ClockRefusal('Nested or control characters in operand')
    self.i+=1
    if self.i-begin>512:raise ClockRefusal('Operand budget 512 characters')
   if self.i>=self.n:raise ClockRefusal('Missing closing ]')
   raw=self.source[begin:self.i];self.i+=1
   args=tuple(a.strip() for a in raw.split(','))
   if not args or any(not a for a in args):raise ClockRefusal('Empty operand in brackets')
   self.check(op,args)
  return Expr(op,args,self.source[start:self.i],start,self.i)
 @staticmethod
 def check(op:str,args:tuple[str,...])->None:
  if op=='⟳':
   if len(args)>MAX_ZONE_LIST:raise ClockRefusal('At most 8 zones per rotor')
   for a in args:check_zone(a)
  if op=='∆':
   if len(args)!=2:raise ClockRefusal('∆ needs two zone names')
   for a in args:check_zone(a)
  if op in ('⌖','☼'):
   if len(args)!=2:raise ClockRefusal('Coordinates require [latitude,longitude]')
   coords(args)
  if op=='ϕ':
   if len(args)!=1:raise ClockRefusal('ϕ requires one period in seconds')
   value=number(args[0]);
   if not .1<=value<=86400:raise ClockRefusal('Period must be 0.1..86400 seconds')

def check_zone(zone:str)->None:
 if not re.fullmatch(r'[A-Za-z0-9_.+/-]{1,96}',zone) or zone.startswith('/') or '..' in zone or zone not in ALLOWED_ZONES:
  raise ClockRefusal('Unknown or invalid IANA zone: '+zone[:60])

def number(s:str)->float:
 if not re.fullmatch(r'[+-]?\d{1,3}(?:\.\d{1,6})?',s):raise ClockRefusal('Coordinates must be decimal numbers')
 v=float(s)
 if not math.isfinite(v):raise ClockRefusal('Nonfinite coordinate')
 return v

def coords(args:tuple[str,...])->tuple[float,float]:
 lat,lon=number(args[0]),number(args[1])
 if not(-90<=lat<=90 and -180<=lon<=180):raise ClockRefusal('Latitude must be -90..90; longitude -180..180')
 return lat,lon

def local_time(dt:datetime,zone:str)->dict:
 check_zone(zone)
 current=dt.astimezone(ZoneInfo(zone))
 return {'zone':zone,'local_iso':current.isoformat(timespec='seconds'),
         'time':current.strftime('%H:%M:%S'), 'date':current.date().isoformat(),
         'abbrev':current.tzname(), 'offset_seconds':int(current.utcoffset().total_seconds()),
         'fold':current.fold,'source':'IANA zoneinfo civil rules; device/server tzdata version applies'}

def equation_of_time(when:datetime)->tuple[float,float]:
 # NOAA fractional year approximation. One snapshot, UTC day/hour; not an ephemeris.
 year_days=366 if when.year%4==0 and (when.year%100!=0 or when.year%400==0) else 365
 day=when.timetuple().tm_yday
 hour=when.hour+when.minute/60+when.second/3600
 gamma=2*math.pi/year_days*(day-1+(hour-12)/24)
 eq=229.18*(.000075+.001868*math.cos(gamma)-.032077*math.sin(gamma)-.014615*math.cos(2*gamma)-.040849*math.sin(2*gamma))
 decl=.006918-.399912*math.cos(gamma)+.070257*math.sin(gamma)-.006758*math.cos(2*gamma)+.000907*math.sin(2*gamma)-.002697*math.cos(3*gamma)+.00148*math.sin(3*gamma)
 return eq,decl

def solar(dt:datetime,lat:float,lon:float)->dict:
 if dt.tzinfo is None:raise ClockRefusal('Solar calculation requires aware UTC instant')
 dt=dt.astimezone(timezone.utc)
 eq,decl=equation_of_time(dt)
 utc_minutes=(dt.hour*60+dt.minute+dt.second/60+dt.microsecond/60000000)
 mean_offset=lon*4  # minutes, east-positive
 mean_total=utc_minutes+mean_offset
 apparent_total=mean_total+eq
 angle_rad=math.radians((apparent_total%1440)/4-180)
 latrad=math.radians(lat)
 sin_alt=math.sin(latrad)*math.sin(decl)+math.cos(latrad)*math.cos(decl)*math.cos(angle_rad)
 elevation=math.degrees(math.asin(max(-1,min(1,sin_alt))))
 def solar_label(minutes):
  v=dt+timedelta(minutes=minutes)
  return v.strftime('%Y-%m-%d %H:%M:%S')
 wedge=min(23,max(0,int(math.floor((lon+180)/15))))
 return {'latitude_deg':lat,'longitude_deg':lon,'mean_solar_offset_minutes':round(mean_offset,4),
         'mean_solar_label':solar_label(mean_offset),'apparent_solar_label':solar_label(mean_offset+eq),
         'equation_of_time_minutes':round(eq,4),'declination_deg':round(math.degrees(decl),4),
         'solar_hour_angle_deg':round(math.degrees(angle_rad),4),'solar_elevation_deg':round(elevation,4),
         'longitude_wedge_15deg':wedge,
         'daylight_geometry':'sun_center_above_geometric_horizon' if elevation>=0 else 'sun_center_below_geometric_horizon',
         'model':'NOAA fractional-year solar approximation (not sunrise/refraction/official legal time)'}

def sphere(lat:float,lon:float)->dict:
 phi=math.radians(lat);theta=math.radians(lon)
 return {'longitude_rad':round(theta,9),'latitude_rad':round(phi,9),
         'unit_xyz':[round(math.cos(phi)*math.cos(theta),9),round(math.cos(phi)*math.sin(theta),9),round(math.sin(phi),9)],
         'unit_vector':'Earth unit sphere; not a GPS position estimate'}

def exact_posix_ns(dt:datetime)->int:
 utc=dt.astimezone(timezone.utc)
 delta=utc-datetime(1970,1,1,tzinfo=timezone.utc)
 return ((delta.days*86400+delta.seconds)*1_000_000_000+delta.microseconds*1000)

def format_offset(seconds:int)->str:
 sign='+' if seconds>=0 else '-'
 sec=abs(seconds)
 return f'{sign}{sec//3600:02d}:{(sec%3600)//60:02d}' + (f':{sec%60:02d}' if sec%60 else '')

def teach(expr:Expr)->str:
 if expr.op=='λ':return shell_source(expr.child)
 if expr.op=='۞':return 'Device date: the browser reads new Date(). This field is client-observed, not remotely authenticated.'
 if expr.op=='⊕':return "UTC (host): date -u '+%Y-%m-%dT%H:%M:%SZ'"
 if expr.op=='⌛':return 'Server wall clock: python3 -c "import time; print(time.time_ns())"'
 if expr.op=='◷':return 'Monotonic: python3 -c "import time; print(time.monotonic_ns())" (arbitrary epoch)'
 if expr.op=='∅':return 'UNKNOWN: make missing observations explicit. Do not substitute 0 or interpolate unobserved wall time.'
 if expr.op=='⟳':return 'Civil time: zoneinfo.ZoneInfo(name) handles DST transitions; longitude alone cannot select legal zones.'
 if expr.op=='⌖':return '15° longitude per geometric hour; longitude × 4 minutes/degree, but latitude does not set legal UTC offset.'
 if expr.op=='☼':return 'NOAA approximation: apparent solar minutes ≈ UTC minutes + 4×longitude + equation_of_time.'
 if expr.op=='∆':return 'Subtract UTC offset at one common instant; civil time rules can change with DST.'
 if expr.op=='ϕ':return 'Phase = 2π × fractional_part(monotonic_elapsed_seconds / period_seconds).'
 return 'Group boundary: parser records the frame; it does not run an OS command.'

def shell_source(expr:Expr)->str:
 """Emit instructional, copyable shell sources. Never run generated strings."""
 if expr is None:raise ClockRefusal('Missing shell child')
 op=expr.op
 if op=='۞':return "# Device clock when run on your phone's terminal\ndate '+%Y-%m-%d %H:%M:%S %z'"
 if op=='⊕':return "# UTC wall time, host\ndate -u '+%Y-%m-%dT%H:%M:%SZ'"
 if op=='⌛':return "# Local host clock; remote GLASS server requires its /api/time endpoint\npython3 -c 'import time; print(time.time_ns())'"
 if op=='◷':return "# Monotonic epoch is implementation-defined\npython3 -c 'import time; print(time.monotonic_ns())'"
 if op in ('⟳','∆'):
  zones=list(expr.args)
  return ('# GLASS civil time operator — Python standard library zoneinfo\n'
   "python3 - <<'PY'\nfrom datetime import datetime, timezone\nfrom zoneinfo import ZoneInfo\n"
   f'zones = {json.dumps(zones,ensure_ascii=False)}\n'
   'instant = datetime.now(timezone.utc)\n'
   'for name in zones:\n'
   '    local = instant.astimezone(ZoneInfo(name))\n'
   "    print(name, local.isoformat(timespec='seconds'), local.utcoffset())\nPY")
 if op in ('⌖','☼'):
  lat,lon=coords(expr.args)
  return ('# GLASS coordinate / solar clock reference\n'
    "python3 - <<'PY'\nfrom datetime import datetime, timezone, timedelta\n"
    f'lat, lon = {lat!r}, {lon!r}\n'
    'utc = datetime.now(timezone.utc)\n'
    'print("mean solar clock", (utc + timedelta(minutes=4 * lon)).strftime("%Y-%m-%d %H:%M:%S"))\n'
    'print("wedge", min(23, max(0, int((lon + 180) // 15))))\n'
    'print("For apparent solar correction and elevation, use GLASS ☼ NOAA reference")\nPY')
 if op=='ϕ':
  p=number(expr.args[0])
  return ('# Clock phase; your process start defines zero\n'
   f"python3 - <<'PY'\nimport math, time\nperiod = {p!r}\n"
   'reference = time.monotonic()\n'
   'print("phase radians", (time.monotonic()-reference) % period * 2 * math.pi / period)\nPY')
 raise ClockRefusal('No shell generator registered for '+op)

def eval_one(expr:Expr,instant:datetime,mono_ns:int,device_time_ms:float|None,elapsed_ns:int)->dict:
 op=expr.op;result={'operator':op,'title':OP_META[op][0],
                     'kind':OP_META[op][2], 'source':expr.source,
                     'lesson':teach(expr),'status':'OK'}
 if op=='λ':
  result.update(kind='shell_program',title='λ / SHELL PROGRAM',status='GENERATED_NOT_EXECUTED',
                values={'child_operator':expr.child.op,'shell':shell_source(expr.child)})
 elif op=='۞':
  result['values']={'device_reported_iso':datetime.fromtimestamp(device_time_ms/1000,timezone.utc).isoformat(timespec='milliseconds') if device_time_ms is not None else None,
                    'device_reported_ms':device_time_ms,'observed_from':'client supplied via browser Date.now; not authenticated','status':'CLIENT_REPORTED' if device_time_ms is not None else 'UNKNOWN'}
 elif op=='⊕':result['values']={'utc_iso':instant.isoformat(timespec='milliseconds'),'posix_epoch_seconds':instant.timestamp(),'source':'server UTC wall snapshot'}
 elif op=='⌛':result['values']={'server_wall_utc':instant.isoformat(timespec='milliseconds'),'server_wall_posix_ns':str(exact_posix_ns(instant)),'observed_from':'GLASS host'}
 elif op=='◷':result['values']={'process_elapsed_seconds':round(elapsed_ns/1e9,6),'server_monotonic_ns':str(mono_ns),'comparable_to_device_monotonic':False}
 elif op=='∅':result.update(status='UNKNOWN_BY_DESIGN',values={'clock':'UNOBSERVED','numeric_zero':False,'note':'No timestamp inferred'})
 elif op=='⟳':result['values']={'zones':[local_time(instant,name) for name in expr.args],'instant_utc':instant.isoformat()}
 elif op=='∆':
  left,right=[local_time(instant,z) for z in expr.args]
  diff=right['offset_seconds']-left['offset_seconds']
  result['values']={'from':left,'to':right,'offset_difference_seconds':diff,
                    'to_minus_from':format_offset(diff),'same_utc_instant':True}
 elif op in ('⌖','☼'):
  lat,lon=coords(expr.args)
  values=solar(instant,lat,lon)
  values.update(sphere(lat,lon))
  if op=='⌖':values={'latitude_deg':lat,'longitude_deg':lon,
                      'longitude_wedge_15deg':values['longitude_wedge_15deg'],
                      'mean_solar_offset_minutes':values['mean_solar_offset_minutes'],
                      'spherical':sphere(lat,lon)}
  result['values']=values
 elif op=='ϕ':
  seconds=number(expr.args[0]);t=elapsed_ns/1e9
  fraction=(t%seconds)/seconds
  result['values']={'period_seconds':seconds,'fraction_of_cycle':round(fraction,9),
                    'angle_radians':round(2*math.pi*fraction,9),'monotonic_reference':'GLASS process start'}
 elif op in ('⟦','⟧'):result['values']={'source_frame_boundary':op}
 return result

def snapshot(now:datetime|None=None,mono_ns:int|None=None)->dict:
 dt=now if now is not None else datetime.now(timezone.utc)
 if dt.tzinfo is None:raise ClockRefusal('UTC aware clock required')
 dt=dt.astimezone(timezone.utc)
 mono=mono_ns if mono_ns is not None else time.monotonic_ns()
 return {'schema':VERSION,'utc_iso':dt.isoformat(timespec='milliseconds'),
         'server_epoch_ms':round(exact_posix_ns(dt)/1_000_000,3),
         'server_posix_ns':str(exact_posix_ns(dt)),
         'server_monotonic_ns':str(mono),'process_uptime_seconds':max(0,round((mono-START_MONO_NS)/1e9,6)),
         'zone_count_available':len(ALLOWED_ZONES),'source':'GLASS host clocks; no NTP synchronization claim'}

def evaluate(source:str,instant:datetime|None=None,mono_ns:int|None=None,client_epoch_ms:float|None=None)->dict:
 if client_epoch_ms is not None:
  if not isinstance(client_epoch_ms,(int,float)) or not math.isfinite(client_epoch_ms) or not 946684800000<=client_epoch_ms<=4102444800000:
   raise ClockRefusal('Client clock sample invalid/outside 2000..2100')
 exprs=Parser(source).parse()
 dt=instant or datetime.now(timezone.utc)
 dt=dt.astimezone(timezone.utc)
 mono=time.monotonic_ns() if mono_ns is None else mono_ns
 elapsed=max(0,mono-START_MONO_NS)
 result=[eval_one(x,dt,mono,client_epoch_ms,elapsed) for x in exprs]
 return {'schema':VERSION,'read_only':True,'source':source,
         'ast':[x.as_dict(source) for x in exprs],
         'operators':[x.op for x in exprs], 'recorded_at_utc':dt.isoformat(timespec='milliseconds'),
         'results':result,'event_trace':[{'seq':i+1,'type':'EVALUATE_PURE','operator':x.op,'clock_domain':'process_logical_tick','source_span':[x.start,x.end]} for i,x in enumerate(exprs)],
         'warning':'No shell execution, external search, geolocation or physical-clock measurement from this grammar'}

if __name__=='__main__':
 import sys
 if len(sys.argv)<2:
  print('Type one or more GLASS operator symbols. Examples:')
  for code,lesson in TUTORIAL:print(code,'—',lesson)
  raise SystemExit(0)
 try:print(json.dumps(evaluate(' '.join(sys.argv[1:])),ensure_ascii=False,indent=2))
 except ClockRefusal as exc:print('GLASS REFUSAL:',exc,file=sys.stderr);sys.exit(2)
