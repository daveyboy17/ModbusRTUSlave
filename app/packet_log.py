from PySide6.QtWidgets import QTextEdit


class PacketMonitor(QTextEdit):

    def __init__(self):
        super().__init__()

        self.setReadOnly(True)


    def add_packet(self, packet):
        text = (
            f"{packet.timestamp} "
            f"{packet.direction}\n"
            f"{packet.hex_string()}\n"
        )

        if packet.description:
            text += (
                f"{packet.description}\n"
            )

        text += "\n"

        self.append(text)


    def add_description(self, description):
        text = (
            f"{description}\n"
        )

        text += "\n"

        self.append(text)