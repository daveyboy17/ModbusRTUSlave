from enum import Enum
import time


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


    def apply(
        self,
        response: bytes | None
    ) -> bytes | None:
        if response is None:
            return None

        if self.mode == ResponseMode.DROP:
            return None

        if self.mode == ResponseMode.DELAY:
            time.sleep(
                self.delay_ms / 1000
            )

        if self.mode == ResponseMode.CORRUPT_CRC:
            response = bytearray(response)
            response[-1] ^= 0xFF
            return bytes(response)

        return response