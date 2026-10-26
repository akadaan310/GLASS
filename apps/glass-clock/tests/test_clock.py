"""GLASS clock grammar mathematical and adversarial fixture tests."""
import hashlib
import json
import math
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import oracle

U=timezone.utc
STAMP=datetime(2026,10,26,12,45,30,tzinfo=U)
class ClockGrammarTests(unittest.TestCase):
 def test_program_unicode_spans(self):
  source='⟦ ۞ ⊕ ⟳[Asia/Dubai,America/New_York] ⟧'
  exp=oracle.Parser(source).parse()
  self.assertEqual([a.op for a in exp],['⟦','۞','⊕','⟳','⟧'])
  for node in exp:
   a,b=node.as_dict(source)['byte_span'];self.assertEqual(source.encode()[a:b],node.source.encode())
 def test_unicode_shell_compose(self):
  exp=oracle.Parser('λ⟳[Asia/Dubai]').parse()[0]
  self.assertEqual(exp.op,'λ');self.assertEqual(exp.child.op,'⟳')
  result=oracle.evaluate('λ⟳[Asia/Dubai]',instant=STAMP)
  code=result['results'][0]['values']['shell']
  self.assertIn('from zoneinfo import ZoneInfo',code)
  self.assertIn('Asia/Dubai',code)
  self.assertEqual(result['results'][0]['status'],'GENERATED_NOT_EXECUTED')
 def test_terminal_only_symbols(self):
  with self.assertRaises(oracle.ClockRefusal):oracle.Parser('run shell now').parse()
  with self.assertRaises(oracle.ClockRefusal):oracle.Parser('◷ && rm -rf /').parse()
  with self.assertRaises(oracle.ClockRefusal):oracle.Parser('λ⟳[UTC]; rm -rf /').parse()
 def test_unknown_non_time(self):
  item=oracle.evaluate('∅',instant=STAMP)['results'][0]
  self.assertFalse(item['values']['numeric_zero']);self.assertEqual(item['status'],'UNKNOWN_BY_DESIGN')
 def test_distinct_clock_domains(self):
  result=oracle.evaluate('۞ ⊕ ⌛ ◷',instant=STAMP,mono_ns=oracle.START_MONO_NS+12340000000,client_epoch_ms=1780000000000)
  vals=result['results']
  self.assertEqual(vals[0]['values']['status'],'CLIENT_REPORTED')
  self.assertEqual(vals[1]['values']['utc_iso'][:19],'2026-10-26T12:45:30')
  self.assertEqual(vals[2]['values']['observed_from'],'GLASS host')
  self.assertEqual(vals[3]['values']['process_elapsed_seconds'],12.34)
  self.assertFalse(vals[3]['values']['comparable_to_device_monotonic'])
 def test_solar_lon_not_civil(self):
  a=oracle.solar(STAMP,0,45)
  b=oracle.solar(STAMP,50,45)
  self.assertEqual(a['mean_solar_offset_minutes'],180)
  self.assertEqual(a['longitude_wedge_15deg'],15)
  self.assertEqual(a['mean_solar_label'],b['mean_solar_label'])
  self.assertNotEqual(a['solar_elevation_deg'],b['solar_elevation_deg'])
  self.assertAlmostEqual(sum(c*c for c in oracle.sphere(50,45)['unit_xyz']),1,places=6)
 def test_min_and_max_wedge(self):
  self.assertEqual(oracle.solar(STAMP,0,-180)['longitude_wedge_15deg'],0)
  self.assertEqual(oracle.solar(STAMP,0,180)['longitude_wedge_15deg'],23)
 def test_explicit_location_not_inferred(self):
  q=oracle.evaluate('⌖[0,45] ☼[0,45]',instant=STAMP)
  self.assertEqual(q['results'][0]['values']['longitude_deg'],45)
  self.assertIn('sun_center_',q['results'][1]['values']['daylight_geometry'])
 def test_dst_spring_and_fall(self):
  before=datetime(2026,3,8,6,59,59,tzinfo=U)
  after=datetime(2026,3,8,7,0,0,tzinfo=U)
  b=oracle.local_time(before,'America/New_York')
  a=oracle.local_time(after,'America/New_York')
  self.assertEqual(b['time'],'01:59:59')
  self.assertEqual(a['time'],'03:00:00')
  self.assertEqual(b['offset_seconds'],-18000)
  self.assertEqual(a['offset_seconds'],-14400)
  first=oracle.local_time(datetime(2026,11,1,5,30,tzinfo=U),'America/New_York')
  repeated=oracle.local_time(datetime(2026,11,1,6,30,tzinfo=U),'America/New_York')
  self.assertEqual(first['time'],repeated['time'])
  self.assertEqual((first['fold'],repeated['fold']),(0,1))
 def test_nonwhole_hour_zone(self):
  k=oracle.local_time(STAMP,'Asia/Kathmandu')
  self.assertEqual(k['offset_seconds'],20700)
  d=oracle.evaluate('∆[Asia/Dubai,Asia/Kathmandu]',instant=STAMP)['results'][0]['values']
  self.assertEqual(d['offset_difference_seconds'],6300)
  self.assertEqual(d['to_minus_from'],'+01:45')
 def test_period_and_zero(self):
  p=oracle.evaluate('ϕ[60]',instant=STAMP,mono_ns=oracle.START_MONO_NS+15000000000)['results'][0]
  self.assertAlmostEqual(p['values']['angle_radians'],math.pi/2,places=7)
 def test_bad_latlon(self):
  for bad in ['⌖[95,0]','☼[20,181]','☼[a,2]','⌖[1,2,3]','⌖[0,0];rm']:
   with self.subTest(expr=bad),self.assertRaises(oracle.ClockRefusal):oracle.Parser(bad).parse()
 def test_bad_zones(self):
  for bad in ['⟳[America/Atlantis]','⟳[../../etc/passwd]','⟳[]','⟳[UTC,]','∆[UTC]','⟳['+','.join(['UTC']*9)+']']:
   with self.subTest(expr=bad),self.assertRaises(oracle.ClockRefusal):oracle.Parser(bad).parse()
 def test_bad_periods(self):
  for bad in ['ϕ[0]','ϕ[-5]','ϕ[1000000]','ϕ[a]']:
   with self.subTest(expr=bad),self.assertRaises(oracle.ClockRefusal):oracle.Parser(bad).parse()
 def test_nested_and_unbalanced(self):
  for bad in ['⟦ ۞','⟧','λ','λλ⊕','λ⟦ ⊕ ⟧']:
   with self.subTest(expr=bad),self.assertRaises(oracle.ClockRefusal):oracle.Parser(bad).parse()
 def test_source_immutable(self):
  x='☼[0,45]';out=oracle.evaluate(x,instant=STAMP)
  self.assertEqual(out['source'],x)
  self.assertEqual(out['ast'][0]['source'],x)
  self.assertEqual(out['event_trace'][0]['source_span'],[0,len(x)])
 def test_budget(self):
  with self.assertRaises(oracle.ClockRefusal):oracle.Parser('۞'*25).parse()
  with self.assertRaises(oracle.ClockRefusal):oracle.Parser('۞'*2050).parse()
 def test_posix_resolution_metadata(self):
  s=oracle.snapshot(STAMP,mono_ns=oracle.START_MONO_NS+5000000000)
  self.assertEqual(s['utc_iso'][:19],'2026-10-26T12:45:30')
  self.assertEqual(s['process_uptime_seconds'],5)
  self.assertGreater(s['zone_count_available'],200)
 def test_no_global_geolocation(self):
  self.assertNotIn('GPS',json.dumps(oracle.evaluate('۞ ⊕',instant=STAMP)))
if __name__=='__main__':unittest.main()
