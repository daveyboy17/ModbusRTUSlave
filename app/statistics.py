from dataclasses import dataclass


@dataclass
class CommunicationStatistics:

    rx_frames: int = 0
    tx_frames: int = 0

    rx_bytes: int = 0
    tx_bytes: int = 0

    crc_errors: int = 0
    exceptions: int = 0


    def received(
        self,
        count
    ):
        self.rx_frames += 1
        self.rx_bytes += count


    def transmitted(
        self,
        count
    ):
        self.tx_frames += 1
        self.tx_bytes += count


    def reset(self):
        self.rx_frames = 0
        self.tx_frames = 0

        self.rx_bytes = 0
        self.tx_bytes = 0

        self.crc_errors = 0
        self.exceptions = 0