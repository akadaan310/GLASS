import unittest
from unison_ast import SPACE,decode,ast,execute_integer
class UnisonGeneratorTests(unittest.TestCase):
 def test_cardinality(self):
  self.assertEqual(SPACE,100000)
 def test_unique_addresses(self):
  self.assertEqual(len({(decode(i).operator,decode(i).width,decode(i).context,decode(i).strategy,decode(i).phase) for i in range(SPACE)}),SPACE)
 def test_digest_determinism(self):
  self.assertEqual(ast(12345),ast(12345))
  self.assertNotEqual(ast(12345)["digest"],ast(12346)["digest"])
 def test_finite_arithmetic(self):
  self.assertEqual(execute_integer(0,1,1),0) # width=1
  self.assertEqual(execute_integer(10000,0,1),1) # sub modulo 2
if __name__=="__main__":unittest.main()
