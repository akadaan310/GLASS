import copy
import json
from pathlib import Path
import shutil
import unittest

from compiler.unison_ir import analyze, Refusal
from compiler.strategy import parse_strategy, signal, StrategyRefusal
from compiler.unibet import codebook, unpack, CodebookError

ROOT=Path(__file__).resolve().parents[1]

class UnisonPipelineTests(unittest.TestCase):
    def test_python_ast_is_structural(self):
        src='def f(a):\n    return a + 1\n'
        a=analyze('python',src)
        self.assertEqual(a['nodes'][0]['kind'],'Module')
        self.assertIn('FunctionDef',[x['kind'] for x in a['nodes']])
        self.assertEqual(len(a['edges']),len(a['nodes'])-1)
        self.assertEqual(a['source_sha256'],analyze('python',src)['source_sha256'])
        self.assertNotEqual(a['source_sha256'],analyze('python',src+'\n')['source_sha256'])
    def test_source_is_not_executed(self):
        src='import os\nos.system("exit 99")\n'
        a=analyze('python',src)
        self.assertEqual(a['status'],'SYNTAX_ONLY')
        self.assertIn('Call',[x['kind'] for x in a['nodes']])
    @unittest.skipUnless(shutil.which('swiftc'),'Swift compiler unavailable')
    def test_swift_compiler_real_parser(self):
        text=(ROOT/'examples/CounterUI.swift').read_text()
        result=analyze('swift',text)
        self.assertGreater(len(result['nodes']),4)
        self.assertIn('swiftc -frontend',result['parser'])
        self.assertTrue(any('Apple' in w for w in result['warnings']))
    @unittest.skipUnless(shutil.which('node'),'Node unavailable')
    def test_typescript_real_parser(self):
        text=(ROOT/'examples/Strategy.ts').read_text()
        result=analyze('typescript',text)
        self.assertIn('TypeScript compiler',result['parser'])
        self.assertIn('ClassDeclaration',[x['kind'] for x in result['nodes']])
    @unittest.skipUnless(shutil.which('java'),'JDK unavailable')
    def test_android_java_native_parser(self):
        data=analyze('java',(ROOT/'examples/AndroidActivity.java').read_text())
        self.assertIn('JavacTask.parse',data['parser'])
        self.assertIn('CLASS',[n['kind'] for n in data['nodes']])
        self.assertTrue(any('Android framework' in w for w in data['warnings']))

    def test_html_parse(self):
        result=analyze('html','<div id="x"><b>test</b></div>')
        self.assertEqual(result['nodes'][1]['kind'],'element')
        self.assertIn('attribute',[x['kind'] for x in result['nodes']])
    def test_budgets_and_unknown_adapter(self):
        with self.assertRaises(Refusal):analyze('kotlin','class A {}')
        with self.assertRaises(Refusal):analyze('html','x'*32769)
    def test_codebook_roundtrip_and_integrity(self):
        sequence=['FunctionDef','Call','Call','FunctionDef','Name']
        c=codebook(sequence)
        self.assertEqual(unpack(c),sequence)
        bad=copy.deepcopy(c);bad['glyphs']='E003'
        with self.assertRaises(CodebookError):unpack(bad)
        self.assertTrue(c['utf8_bytes_with_codebook']>0)
    def test_codebook_has_no_magic_compression(self):
        c=codebook(['A','B','C'])
        self.assertGreater(c['utf8_bytes_with_codebook'],c['raw_token_json_bytes'])
    def test_strategy_parse_and_bounded_signal(self):
        s=parse_strategy('WHEN SMA(3) CROSS_ABOVE SMA(9) THEN SIGNAL BUY')
        self.assertTrue(signal(s,[10]*10+[1]*9+[30]))
        self.assertFalse(signal(s,[10]*10+[1]*9))
        self.assertEqual(s['executed_orders'],0)
        with self.assertRaises(StrategyRefusal):parse_strategy('BUY AAPL MARKET')
        with self.assertRaises(StrategyRefusal):parse_strategy('WHEN SMA(3) CROSS_ABOVE SMA(3) THEN SIGNAL BUY')

if __name__=='__main__':unittest.main()
