from enum import Enum
import time
from ..statistics import CommunicationStatistics


class ResponseMode(Enum):
    NORMAL = "normal"
    DELAY = "delay"
    DROP = "drop"
    CORRUPT_CRC = "corrupt_crc"
    EXCEPTION = "exception"


class ResponseController:
    """
    Controls simulated device behaviour.

    This layer intentionally sits outside the
    Modbus protocol engine.
    """

    def __init__(self):
        self.mode = ResponseMode.NORMAL
        self.delay_ms = 0
        self.exception_code = None

        self.statistics = CommunicationStatistics()


    def apply(self, response: bytes | None) -> bytes | None:
        if response is None:
            return None

        print(response)
        print(self.mode)
        print(self.delay_ms)

        if self.mode == ResponseMode.DROP:
            self.statistics.ignored()
            return None

        if self.mode == ResponseMode.DELAY:
            time.sleep(
                self.delay_ms / 1000
            )

        if self.mode == ResponseMode.CORRUPT_CRC:
            response = bytearray(response)
            response[-1] ^= 0xFF
            self.statistics.crc_error()
            return bytes(response)

        if self.mode == ResponseMode.EXCEPTION:
            response = bytearray(response)
            response[1] |= 0x80
            return bytes(response)

        return response