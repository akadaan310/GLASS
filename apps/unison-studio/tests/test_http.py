import json
from pathlib import Path
import socket
import subprocess
import time
import unittest
from urllib.request import urlopen, Request
from urllib.error import HTTPError

ROOT=Path(__file__).resolve().parents[1]

class SwiftServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        exe=ROOT/'server/unison-server'
        if not exe.exists():raise unittest.SkipTest('Swift server executable not built')
        with socket.socket() as s:
            s.bind(('127.0.0.1',0));port=s.getsockname()[1]
        cls.origin=f'http://127.0.0.1:{port}'
        cls.proc=subprocess.Popen([str(exe),str(port)],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
        for _ in range(50):
            try:
                with urlopen(cls.origin+'/api/status',timeout=.3) as r:cls.start=json.load(r);break
            except Exception:time.sleep(.1)
        else:raise RuntimeError('server did not start')
    @classmethod
    def tearDownClass(cls):
        if hasattr(cls,'proc'):
            cls.proc.terminate();cls.proc.wait(timeout=5)
    def test_swift_http(self):
        self.assertEqual(self.start['mode'],'Swift/Linux HTTP')
        self.assertFalse(self.start['native_iOS_emulation'])
        with urlopen(self.origin+'/') as r:
            self.assertIn('GLASS',r.read(2000).decode())
    def test_market_deterministic_and_labeled(self):
        with urlopen(self.origin+'/api/market?seed=24681357') as r:a=json.load(r)
        with urlopen(self.origin+'/api/market?seed=24681357') as r:b=json.load(r)
        self.assertEqual(a,b)
        self.assertEqual(a['event_count'],768)
        self.assertEqual(a['provider'],'NONE')
        self.assertEqual(a['orders'],0)
        self.assertEqual(a['ranking'][0]['symbol'],'ORCA')
        self.assertGreater(a['ranking'][0]['burst_score'],5)
    def test_no_arbitrary_file_or_mutation(self):
        for path in ['/../../etc/passwd','/api/trade','/data/secrets.json']:
            with self.assertRaises(HTTPError) as cm:
                urlopen(self.origin+path,timeout=1)
            self.assertIn(cm.exception.code,[400,404,405])
        with self.assertRaises(HTTPError) as cm:
            urlopen(Request(self.origin+'/api/market',data=b'{}',method='POST'),timeout=1)
        self.assertEqual(cm.exception.code,405)
    def test_bad_seed(self):
        with self.assertRaises(HTTPError) as cm:urlopen(self.origin+'/api/market?seed=abc',timeout=1)
        self.assertEqual(cm.exception.code,400)

if __name__=='__main__':unittest.main()
