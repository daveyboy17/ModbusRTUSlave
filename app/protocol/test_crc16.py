import unittest
from .crc16 import calculate


# request 01 03 00 00 00 02 C4 0B
# response 01 03 04 00 64 00 C8 BA 7A


class TestCrc16(unittest.TestCase):
    def test_ValidFrames(self):
        frame = bytes([1, 3, 0, 1, 12])
        response = calculate(frame)
        self.assertEqual(response, 4376)
        
        frame = bytes([1, 3, 0, 0, 0, 2])
        response = calculate(frame)
        self.assertEqual(response, 50187)
        
        frame = bytes([1, 3, 4, 0, 100, 0, 200])
        response = calculate(frame)
        self.assertEqual(response, 47738)