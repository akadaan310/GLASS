#!/usr/bin/env python3
"""Small local-only server for GLASS symbolic time terminal.

No third-party packages, credentials, cross-origin access, uploads, or shell eval.
By default listens on 127.0.0.1; intended for Termux/other owner's terminal.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import time
from urllib.parse import urlsplit
from oracle import ClockRefusal, OP_META, TUTORIAL, ZONE_SHOWCASE, evaluate, snapshot

ROOT=Path(__file__).resolve().parent
ASSETS={'/':('index.html','text/html; charset=utf-8'),
        '/index.html':('index.html','text/html; charset=utf-8'),
        '/style.css':('style.css','text/css; charset=utf-8'),
        '/client.js':('client.js','application/javascript; charset=utf-8')}
MAX_BODY=8192

class Handler(BaseHTTPRequestHandler):
 server_version='GLASS-CLOCK/0.1'
 sys_version=''
 def _origin_valid(self)->bool:
  # Host and Origin must both remain local in this first iteration.
  host=self.headers.get('Host','')
  valid_hosts=(f'127.0.0.1:{self.server.server_port}',f'localhost:{self.server.server_port}',
               '127.0.0.1','localhost')
  origin=self.headers.get('Origin','')
  return host in valid_hosts and (not origin or origin in (f'http://127.0.0.1:{self.server.server_port}',f'http://localhost:{self.server.server_port}'))
 def _send(self,code:int,data:bytes,mime='application/json; charset=utf-8')->None:
  self.send_response(code)
  self.send_header('Content-Type',mime)
  self.send_header('Content-Length',str(len(data)))
  self.send_header('Cache-Control','no-store, max-age=0')
  self.send_header('X-Content-Type-Options','nosniff')
  self.send_header('Referrer-Policy','no-referrer')
  self.send_header('Cross-Origin-Resource-Policy','same-origin')
  self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; connect-src 'self'; img-src 'self'; style-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'")
  self.end_headers()
  if self.command!='HEAD':self.wfile.write(data)
 def _json(self,code:int,item:dict)->None:
  self._send(code,(json.dumps(item,ensure_ascii=False,separators=(',',':'))+'\n').encode('utf-8'))
 def do_GET(self)->None:
  if not self._origin_valid():self._json(403,{'error':'local-origin-only'});return
  if '?' in self.path and urlsplit(self.path).query:self._json(400,{'error':'query-string not allowed on this route'});return
  path=urlsplit(self.path).path
  if path=='/api/time':
   self._json(200,snapshot());return
  if path=='/api/grammar':
   self._json(200,{'schema':'glass.clock.grammar/0.1','operators':[
    {'glyph':k,'title':v[0],'lesson':v[1],'kind':v[2]} for k,v in OP_META.items()],
    'tutorial':[{'expression':c,'meaning':m} for c,m in TUTORIAL],
    'showcase_zones':ZONE_SHOWCASE,'effects':'read-only; shell code generation is inert text'})
   return
  if path in ASSETS:
   name,mime=ASSETS[path]
   try:self._send(200,(ROOT/name).read_bytes(),mime)
   except OSError:self._json(500,{'error':'missing static asset'})
   return
  self._json(404,{'error':'unregistered route'})
 def do_POST(self)->None:
  if not self._origin_valid():self._json(403,{'error':'local-origin-only'});return
  if self.path!='/api/eval':self._json(404,{'error':'unregistered route'});return
  if self.headers.get('Content-Type','').split(';')[0].strip()!='application/json':
   self._json(415,{'error':'application/json required'});return
  try:
   length=int(self.headers.get('Content-Length','0'))
   if not 1<=length<=MAX_BODY:raise ClockRefusal('POST budget 1..8192 bytes')
   obj=json.loads(self.rfile.read(length))
   if not isinstance(obj,dict) or set(obj)-{'source','client_epoch_ms'} or 'source' not in obj:
    raise ClockRefusal('Expected {source,client_epoch_ms?}')
   result=evaluate(obj['source'],client_epoch_ms=obj.get('client_epoch_ms'))
  except (ValueError,ClockRefusal,UnicodeError,TypeError,json.JSONDecodeError) as exc:
   self._json(422,{'schema':'glass.clock.refusal/0.1','error':str(exc)[:260]});return
  self._json(200,result)
 def do_OPTIONS(self):self._json(405,{'error':'cross-origin requests disabled'})
 def do_PUT(self):self._json(405,{'error':'write operations disabled'})
 def do_DELETE(self):self._json(405,{'error':'write operations disabled'})
 def log_message(self,fmt,*args):
  # Never log typed program input; log only method+status and peer IP for errors.
  # This server is localhost only.
  return

class ClockServer(ThreadingHTTPServer):
 daemon_threads=True
 allow_reuse_address=True

def start(host='127.0.0.1',port=8765)->None:
 if host not in ('127.0.0.1','localhost'):
  raise SystemExit('Refused: v0.1 deliberately serves localhost only. Use a reviewed authenticated tunnel for remote use.')
 if not (0<=port<=65535):raise SystemExit('Invalid TCP port')
 with ClockServer((host,port),Handler) as server:
  print(f'GLASS Clock Oracle · http://127.0.0.1:{server.server_port}/ · ⊕ ⟳ ☼ λ',flush=True)
  print('Local-only; typing never executes generated shell commands. Stop with Ctrl+C.',flush=True)
  try:server.serve_forever(poll_interval=.2)
  except KeyboardInterrupt:pass

def main():
 parser=argparse.ArgumentParser(description='GLASS native Termux-compatible clock bridge')
 parser.add_argument('--host',default='127.0.0.1')
 parser.add_argument('--port',type=int,default=8765)
 options=parser.parse_args()
 start(options.host,options.port)

if __name__=='__main__':main()
