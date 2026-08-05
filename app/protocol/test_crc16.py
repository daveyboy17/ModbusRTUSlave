import unittest
# from .crc16 import calculate
import crc16


class TestCrc16(unittest.TestCase):
    def TestValidFrames(self):
        frame = bytes([1, 3, 0, 1, 12])
        response = crc16.calculate(frame)
        self.assertEqual(response, 123)