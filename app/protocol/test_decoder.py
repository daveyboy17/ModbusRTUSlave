import unittest
# from .decoder import describe
import decoder


class TestDecoder(unittest.TestCase):
    def TestValidFrames(self):
        frame = bytes([1, 3, 0, 1, 12])
        response = decoder.describe(frame)
        self.assertEqual(response, "Slave: 1\nFunction: 3 (Read Holding Registers)")
        
        frame = bytes([2, 4, 0, 1, 12])
        response = decoder.describe(frame)
        self.assertEqual(response, "Slave: 2\nFunction: 4 (Read Input Registers)")
        
        frame = bytes([3, 6, 0, 1, 12])
        response = decoder.describe(frame)
        self.assertEqual(response, "Slave: 3\nFunction: 6 (Write Single Register)")
        
        frame = bytes([4, 16, 0, 1, 12])
        response = decoder.describe(frame)
        self.assertEqual(response, "Slave: 4\nFunction: 6 (Write Multiple Registers)")

    def TestInvalidFrames(self):
        frame = bytes([5])
        response = decoder.describe(frame)
        self.assertEqual(response, "")
        
        frame = bytes([6, 11, 0, 1, 12])
        response = decoder.describe(frame)
        self.assertEqual(response, "Slave: 6\nFunction: 11 (Unknown Function)")