import unittest
from .crc16 import calculate


class TestCrc16(unittest.TestCase):
    def test_ValidFrames(self):
        frame = bytes([1, 3, 0, 1, 12])
        response = calculate(frame)
        self.assertEqual(response, 4376)