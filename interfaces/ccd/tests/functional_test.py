import unittest

from interfaces.ccd.sbig import ccd

class CCDFunctionalTest(unittest.TestCase):

    def test_capture(self):
        c = ccd
        c.capture(2, 10, (1, 1), 1, 1, 'light')

if __name__ == '__main__':
    unittest.main()
