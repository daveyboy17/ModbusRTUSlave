from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem

from ..models import PacketLogEntry
from ..protocol.crc16 import verify


class PacketMonitor(QTreeWidget):
    columns = ("Time", "Dir", "Slave", "Function", "Bytes", "Status")

    def __init__(self) -> None:
        super().__init__()
        self.setColumnCount(len(self.columns))
        self.setHeaderLabels(self.columns)
        self.setAlternatingRowColors(True)

    def add_entry(self, packet: PacketLogEntry) -> None:
        frame = packet.data
        values = (
            packet.timestamp,
            packet.direction,
            str(frame[0]) if frame else "",
            f"{frame[1]:02X}" if len(frame) > 1 else "",
            packet.hex_string(),
            "Valid" if verify(frame) else "Invalid",
        )

        item = QTreeWidgetItem(self)
        for column, value in enumerate(values):
            item.setText(column, value)