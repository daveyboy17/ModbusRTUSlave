import unittest
from .decoder import describe


class TestDecoder(unittest.TestCase):
    def TestValidFrames(self):
        frame = bytes([1, 3, 0, 1, 12])
        response = describe(frame)
        self.assertEqual(response, "Slave: 1\nFunction: 3 (Read Holding Registers)")
        
        frame = bytes([2, 4, 0, 1, 12])
        response = describe(frame)
        self.assertEqual(response, "Slave: 2\nFunction: 4 (Read Input Registers)")