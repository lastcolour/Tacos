import unittest

class TestOne(unittest.TestCase):

    def testOne(self):
        x = 1
        y = 2
        res = x + y
        self.assertEqual(res, 3)

if __name__ == "__main__":
    unittest.main()