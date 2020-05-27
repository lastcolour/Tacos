import unittest

class TestTwo(unittest.TestCase):

    def testOne(self):
        x = 1
        y = 2
        res = x / y
        self.assertEqual(res, 0.5)

if __name__ == "__main__":
    unittest.main()