from dataclasses import dataclass


@dataclass
class CommunicationStatistics:

    # Traffic
    rx_frames: int = 0
    tx_frames: int = 0

    rx_bytes: int = 0
    tx_bytes: int = 0

    # Errors
    crc_errors: int = 0
    exceptions: int = 0
    ignored_frames: int = 0
    dropped_responses: int = 0

    # Timing
    total_response_time_ms: float = 0.0
    max_response_time_ms: float = 0.0
    ave_response_time_ms: float = 0.0

    # Status
    connected: bool = False
    port_name: str = ""
    baudrate: int = 9600

    def received(self, count):
        self.rx_frames += 1
        self.rx_bytes += count


    def transmitted(self, count):
        self.tx_frames += 1
        self.tx_bytes += count


    def reset(self):
        self.rx_frames = 0
        self.tx_frames = 0

        self.rx_bytes = 0
        self.tx_bytes = 0

        self.crc_errors = 0
        self.exceptions = 0
        ignored_frames = 0
        dropped_responses = 0

        total_response_time_ms = 0.0
        max_response_time_ms = 0.0
        ave_response_time_ms = 0.0

    def crc_error(self):
        self.crc_errors += 1

    def exception(self):
        self.exceptions += 1

    def ignored(self):
        self.ignored_frames += 1

    def dropped(self):
        self.dropped_responses += 1

    def response_time(self, response_time_ms):
        self.total_response_time_ms += response_time_ms

        if response_time_ms > self.max_response_time_ms:
            self.max_response_time_ms = response_time_ms

        self.ave_response_time_ms = self.total_response_time_ms / self.tx_frames

    def connection(self, status: bool):
        self.connected = status

    def port(self, name: str):
        self.port_name = name

    def baud(self, rate: int):
        self.baudrate = rate