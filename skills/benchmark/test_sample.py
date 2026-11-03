import unittest
from sample import calculate_total
class TestTotal(unittest.TestCase):
    def test_normal(self): self.assertEqual(calculate_total([(120,2),(50,1)]),290)
    def test_empty(self): self.assertEqual(calculate_total([]),0)
    def test_invalid(self):
        with self.assertRaises(ValueError): calculate_total([(20,-1)])
if __name__ == '__main__': unittest.main()
