import tempfile
import unittest
from unison_predicate import HIJAI, ABJAD, Evidence, Rolodex, encode_predicate, identity

class Tests(unittest.TestCase):
    def test_alphabet_cardinality(self):
        self.assertEqual(len(HIJAI),28)
        self.assertEqual(len(ABJAD),28)
    def test_open_world_evidence(self):
        e=Evidence()
        self.assertEqual(e.ask("member","x")["truth"],"UNKNOWN")
        e.assert_fact("member","x",provenance="w1")
        self.assertEqual(e.ask("member","x")["witnesses"],["w1"])
    def test_lazy_restore(self):
        with tempfile.TemporaryDirectory() as d:
            r=Rolodex(d)
            source=b"abc"*1000
            r.admit("fixture",source)
            self.assertEqual(r.open("fixture"),source)
            self.assertLess(r.report()["stored_bytes"],r.report()["raw_bytes"])
    def test_symbols(self):
        self.assertEqual(encode_predicate("∀x∃y⊢Π")[0]["op"],"forall")
    def test_identity_stable(self):
        self.assertEqual(identity("۞",{"k":1}),identity("۞",{"k":1}))

if __name__=="__main__":unittest.main()
