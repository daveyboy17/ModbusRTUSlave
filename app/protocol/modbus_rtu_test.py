import unittest
from .modbus_rtu import *


class TestModbusRTU(unittest.TestCase):
    def test_ValidFrame(self):
        modbus_slave = modbus_rtu.ModbusRTUSlave(1, register_bank)
        frame = bytes([1, 3, 0, 1, 12])
        response = modbus_slave.process(frame)
        self.assertEqual(response, None)
