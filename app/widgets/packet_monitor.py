from PySide6.QtWidgets import QTextEdit

from ..models import PacketLogEntry


class PacketMonitor(QTextEdit):
    def __init__(self) -> None:
        super().__init__()
        self.setReadOnly(True)

    def add_packet(self, packet: PacketLogEntry) -> None:
        text = (
            f"{packet.timestamp} "
            f"{packet.direction}\n"
            f"{packet.hex_string()}\n"
        )

        if packet.description:
            text += f"{packet.description}\n"

        self.append(f"{text}\n")

    def add_description(self, description: str) -> None:
        self.append(f"{description}\n\n")