"""Loopback-only backend acceptance including refused effects and privacy headers."""
import json
from pathlib import Path
import sys
import threading
import unittest
from urllib.request import urlopen, Request
from urllib.error import HTTPError
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from server import ClockServer,Handler

class ServerTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.s=ClockServer(('127.0.0.1',0),Handler)
  cls.thread=threading.Thread(target=cls.s.serve_forever,daemon=True);cls.thread.start()
  cls.url='http://127.0.0.1:'+str(cls.s.server_port)
 @classmethod
 def tearDownClass(cls):cls.s.shutdown();cls.s.server_close();cls.thread.join(timeout=3)
 def call(self,path,method='GET',data=None,headers=None):
  r=Request(self.url+path,method=method,data=data,headers=headers or {})
  with urlopen(r,timeout=3) as x:return x.status,x.headers,x.read()
 def test_clock_observation(self):
  status,headers,data=self.call('/api/time')
  item=json.loads(data)
  self.assertEqual(status,200)
  self.assertEqual(item['schema'],'glass.clock-oracle/0.1')
  self.assertGreater(item['server_epoch_ms'],1780000000000)
  self.assertIn('no-store',headers['Cache-Control'])
 def test_grammar_and_page(self):
  _,_,data=self.call('/api/grammar')
  self.assertEqual(len(json.loads(data)['operators']),13)
  _,_,html=self.call('/')
  self.assertIn(b'id="expression"',html)
  self.assertNotIn(b'<button',html)
 def test_eval_program(self):
  body=json.dumps({'source':'⟳[Asia/Kathmandu] ☼[0,45] λ⊕','client_epoch_ms':1780000000000},ensure_ascii=False).encode()
  status,_,data=self.call('/api/eval','POST',body,{'Content-Type':'application/json'})
  obj=json.loads(data)
  self.assertEqual(status,200)
  self.assertEqual([p['operator'] for p in obj['results']],['⟳','☼','λ'])
  self.assertEqual(obj['results'][0]['values']['zones'][0]['offset_seconds'],20700)
 def test_malformed_queries_refuse(self):
  raw=json.dumps({'source':'rm -rf /'}).encode()
  with self.assertRaises(HTTPError) as h:self.call('/api/eval','POST',raw,{'Content-Type':'application/json'})
  self.assertEqual(h.exception.code,422)
  with self.assertRaises(HTTPError) as h:self.call('/api/eval','POST',b'{}',{'Content-Type':'text/plain'})
  self.assertEqual(h.exception.code,415)
  with self.assertRaises(HTTPError) as h:self.call('/api/eval','POST',b'{}'*5000,{'Content-Type':'application/json'})
  self.assertEqual(h.exception.code,422)
 def test_no_cross_origin_or_mutation(self):
  with self.assertRaises(HTTPError) as h:self.call('/api/time',headers={'Origin':'https://evil.example'})
  self.assertEqual(h.exception.code,403)
  with self.assertRaises(HTTPError) as h:self.call('/api/clock','PUT',b'{}')
  self.assertEqual(h.exception.code,405)
  with self.assertRaises(HTTPError) as h:self.call('/../../etc/passwd')
  self.assertEqual(h.exception.code,404)
if __name__=='__main__':unittest.main()
