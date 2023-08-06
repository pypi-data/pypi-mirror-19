import unittest
import py_cupom


class PyCupomTest(unittest.TestCase):
    def test_default_encode(self):
        result = py_cupom.encode(1234, 4)
        self.assertEqual("A16J", result);

        result = py_cupom.encode(234412342312556, 10)
        self.assertEqual("6N69G69ZKC", result);

        result = py_cupom.decode("A16J")
        self.assertEqual(1234, result)

        result = py_cupom.decode("6N69G69ZKC")
        self.assertEqual(234412342312556, result)