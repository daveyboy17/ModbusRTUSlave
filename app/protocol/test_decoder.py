import unittest
from .decoder import describe


class TestDecoder(unittest.TestCase):
    def test_valid_frames(self):
        frame = bytes([1, 3, 0, 1, 12])
        response = describe(frame)
        self.assertEqual(response, "Slave: 1\nFunction: 3 (Read Holding Registers)")
        
        frame = bytes([2, 4, 0, 1, 12])
        response = describe(frame)
        self.assertEqual(response, "Slave: 2\nFunction: 4 (Read Input Registers)")
        
        frame = bytes([3, 6, 0, 1, 12])
        response = describe(frame)
        self.assertEqual(response, "Slave: 3\nFunction: 6 (Write Single Register)")
        
        frame = bytes([4, 16, 0, 1, 12])
        response = describe(frame)
        self.assertEqual(response, "Slave: 4\nFunction: 16 (Write Multiple Registers)")

    def test_invalid_frames(self):
        frame = bytes([5])
        response = describe(frame)
        self.assertEqual(response, "")
        
        frame = bytes([6, 11, 0, 1, 12])
        response = describe(frame)
        self.assertEqual(response, "Slave: 6\nFunction: 11 (Unknown Function)")