from PySide6.QtCore import QThread, Signal
import serial


class SerialWorker(QThread):
    """
    This controls the serial port.
    """

    received = Signal(bytes)
    transmitted = Signal(bytes)
    error = Signal(str)
    connected = Signal()
    disconnected = Signal()

    def __init__(self):
        super().__init__()

        self.serial = None
        self.running = False

    def configure(self, port, baudrate=9600):
        self.port = port
        self.baudrate = baudrate

    def run(self):
        try:
            self.serial = serial.Serial(
                port = self.port,
                baudrate = self.baudrate,
                bytesize = 8,
                parity = serial.PARITY_NONE,
                stopbits = serial.STOPBITS_ONE,
                timeout = 0.05
            )
        except Exception as e:
            self.error.emit(
                str(e)
            )

            return

        self.running = True
        self.connected.emit()


        import time

        INTER_FRAME_DELAY = 0.004

        last_byte_time = None
        buffer = bytearray()

        while self.running:
            if self.serial.in_waiting:
                data = self.serial.read(
                    self.serial.in_waiting
                )

                buffer.extend(data)

                last_byte_time = time.monotonic()

            if buffer and last_byte_time:
                elapsed = (
                    time.monotonic()
                    -
                    last_byte_time
                )

                if elapsed >= INTER_FRAME_DELAY:
                    frame = bytes(buffer)

                    buffer.clear()

                    last_byte_time = None

                    self.received.emit(
                        frame
                    )

        self.serial.close()

        self.disconnected.emit()


    def send(self, data):
        if self.serial:
            self.serial.write(data)
            self.transmitted.emit(data)


    def stop(self):
        self.running = False