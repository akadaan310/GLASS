import hashlib
import json
import struct
import tempfile
import unittest
from pathlib import Path
from tools.verify_ledger import verify

class ChainTest(unittest.TestCase):
    def test_valid_chain_and_tamper(self):
        previous=bytes(32)
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'events.jsonl'
            lines=[]
            for i in range(3):
                record='{"seq":%d,"epoch":1,"kind":"%s"}'%(i+1,'CAPTURE_GAP' if i==1 else 'SCREEN_FRAME')
                body=record.encode()
                digest=hashlib.sha256(previous+struct.pack('>I',len(body))+body).hexdigest()
                previous=bytes.fromhex(digest)
                lines.append('{"hash":"'+digest+'","event":'+record+'}')
            path.write_text('\n'.join(lines)+'\n')
            out=verify(path)
            self.assertEqual((out['records'],out['gaps']),(3,1))
            path.write_text(path.read_text().replace('SCREEN_FRAME','CHANGED_FRAME',1))
            with self.assertRaises(ValueError):verify(path)

if __name__=='__main__':unittest.main()
