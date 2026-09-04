from dataclasses import dataclass
import time


@dataclass
class CommunicationStatistics:
    """
    Statistics for showing in a floating dock,
    updated every 250ms by a QTimer.
    """

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
    uptime_ms: float = 0.0
    last_rx_time: float = 0.0
    connected_at: float = 0.0

    # Status
    connected: bool = False
    port_name: str = ""
    baudrate: int = 9600

    def received(self, count):
        self.rx_frames += 1
        self.rx_bytes += count
        self.last_rx_time = time.perf_counter()


    def transmitted(self, count):
        self.tx_frames += 1
        self.tx_bytes += count

        response_time_ms = time.perf_counter() - self.last_rx_time
        self.response_time(response_time_ms)


    def reset(self):
        self.rx_frames = 0
        self.tx_frames = 0

        self.rx_bytes = 0
        self.tx_bytes = 0

        self.crc_errors = 0
        self.exceptions = 0
        self.ignored_frames = 0
        self.dropped_responses = 0

        self.total_response_time_ms = 0.0
        self.max_response_time_ms = 0.0
        self.ave_response_time_ms = 0.0
        self.uptime_ms = 0.0
        self.last_rx_time = 0.0
        self.connected_at = 0.0

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
        if self.connected == False and status == True:
            self.connected_at = time.perf_counter()
        self.connected = status

    def port(self, name: str):
        self.port_name = name

    def baud(self, rate: int):
        self.baudrate = rate

    def refresh(self) -> str:
        if self.connected == True:
            self.uptime_ms = time.perf_counter() - self.connected_at
        text = (
            f"Comms\nPort: {self.port_name}\nBaud: {self.baudrate}\nConnected: {self.connected}\n\n"
            f"Traffic\nRX\nFrames: {self.rx_frames}\nBytes: {self.rx_bytes}\n"
            f"TX\nFrames: {self.tx_frames}\nBytes: {self.tx_bytes}\n\n"
            f"Protocol\nCRC Errors: {self.crc_errors}\nExceptions: {self.exceptions}\n"
            f"Ignored: {self.ignored_frames}\nDropped: {self.dropped_responses}\n\n"
            f"Performance\nMax Response Time: {self.max_response_time_ms:.2f}\nAve Response Time: {self.ave_response_time_ms:.2f}\n"
            f"Uptime: {self.uptime_ms:.1f}\n"
        )
        return text