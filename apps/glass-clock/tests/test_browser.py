"""Headless browser acceptance. Uses actual localhost server if allowed, otherwise injected
same-origin captured responses from the tested Python backend and reports that limit.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import sys
import threading
import time
import unittest
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from oracle import evaluate,snapshot
from server import ClockServer,Handler

class BrowserTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.s=ClockServer(('127.0.0.1',0),Handler)
  cls.t=threading.Thread(target=cls.s.serve_forever,daemon=True);cls.t.start()
  cls.url=f'http://127.0.0.1:{cls.s.server_port}/'
  cls.pw=sync_playwright().start()
  cls.browser=cls.pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu'],timeout=15000)
 @classmethod
 def tearDownClass(cls):
  cls.browser.close();cls.pw.stop();cls.s.shutdown();cls.s.server_close();cls.t.join(timeout=2)
 def page(self,width,height):
  page=self.browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  mode='live_http'
  try:page.goto(self.url,wait_until='load',timeout=9000)
  except Exception as e:
   # Some container environments forbid localhost/URL navigation at policy level.
   mode='isolated_web_renderer_backend_mock'
   page.close()
   page=self.browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
   errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
   html=(ROOT/'index.html').read_text()
   html=html.replace('<link rel="stylesheet" href="style.css"/>','<style>'+(ROOT/'style.css').read_text()+'</style>')
   html=html.replace('<script defer src="client.js"></script>','')
   page.set_content(html,wait_until='domcontentloaded',timeout=9000)
   def mock(path,options=None):
    key=str(path)
    if key=='/api/time':return snapshot()
    if key=='/api/eval':
     obj=json.loads(options['body']);return evaluate(obj['source'],client_epoch_ms=obj.get('client_epoch_ms'))
    return {'error':'not found'}
   def wrap(src):
    return '''window.fetch=async function(path,opts={}){const val=await window.__mockClock(path,opts);return new Response(JSON.stringify(val),{status:val.error?422:200,headers:{'Content-Type':'application/json'}})};'''+src
   page.expose_function('__mockClock',mock)
   page.add_script_tag(content=wrap((ROOT/'client.js').read_text()))
  page.wait_for_timeout(750)
  return page,mode,errors
 def test_desktop_mobile_symbol_typing(self):
  summary=[]
  for name,size in [('desktop',(1440,960)),('mobile',(390,844))]:
   page,mode,errors=self.page(*size)
   self.assertEqual(page.locator('textarea').count(),1)
   self.assertEqual(page.locator('button').count(),0)
   self.assertEqual(page.locator('#operators .operator').count(),12)
   self.assertIn('⟳',page.locator('#expression').input_value())
   self.assertGreaterEqual(page.locator('#lessons .result').count(),4)
   page.locator('#expression').fill('☼[0,45] ∆[Asia/Dubai,Asia/Kathmandu] λ⟳[Asia/Dubai]')
   page.wait_for_timeout(350)
   self.assertEqual(page.locator('#lessons .result').count(),3)
   self.assertIn('+01:45',page.locator('#lessons').inner_text())
   self.assertIn('python3 -',page.locator('#lessons').inner_text())
   s=page.evaluate('({scrollW:document.documentElement.scrollWidth,clientW:document.documentElement.clientWidth,clock:document.getElementById("localTime").innerText,server:document.getElementById("serverTime").innerText})')
   self.assertLessEqual(s['scrollW'],s['clientW']+2)
   self.assertNotIn('--:--',s['clock'])
   self.assertFalse(errors,f'browser errors: {errors}')
   path=ROOT/'evidence'/f'{name}-preview.png';path.parent.mkdir(exist_ok=True)
   page.screenshot(path=str(path),full_page=True,timeout=12000)
   summary.append({'layout':name,'mode':mode,'width':size[0],'source_operator_count':3,'clock':s['clock'],'server':s['server']})
   page.close()
  (ROOT/'evidence'/'browser.json').write_text(json.dumps({'schema':'glass.clock.browser-evidence/0.1','screens':summary,'status':'PASS','limitations': 'HTTP server separately exercised; if mode=mock, browser renderer used backend fixtures rather than live HTTP'},indent=2)+'\n')
if __name__=='__main__':unittest.main()
