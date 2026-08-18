from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem


class PacketMonitor():
    columns = {
            0: "Time",
            1: "Dir",
            2: "Slave",
            3: "Function",
            4: "Bytes",
            5: "Status"
    }
    
    def __init__(self) -> None:
        super().__init__()
        
        self.tree = QTreeWidget()
        self.tree.setColumnCount(6)
        names = []
        for _idx, name in self.columns:
            names.append(name)
        # tree.setHeaderLabels(["Time", "Dir", "Slave", "Function", "Bytes", "Status"])
        self.tree.setHeaderLabels(names)


    def add_entry(self, entry: dict):
        item = QTreeWidgetItem(self.tree)
        item.setText(0, entry[0])
        item.setText(1, entry[1])
        item.setText(2, entry[2])
        item.setText(3, entry[3])
        item.setText(4, entry[4])
        item.setText(5, entry[5])