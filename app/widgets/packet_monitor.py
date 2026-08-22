from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem


class PacketMonitor():
    """
    This is the Tree Widget panel for the packet monitor.
    """
    
    columns = {
            "Time": 0,
            "Dir": 1,
            "Slave": 2,
            "Function": 3,
            "Bytes": 4,
            "Status": 5
    }
    
    def __init__(self) -> None:
        super().__init__()
        
        self.tree = QTreeWidget()
        self.tree.setColumnCount(6)
        names = []
        for name,  _idx in self.columns:
            names.append(name)
        # tree.setHeaderLabels(["Time", "Dir", "Slave", "Function", "Bytes", "Status"])
        self.tree.setHeaderLabels(names)
        self.tree.setAlternatingRowColors(True)


    def add_entry(self, entry: dict):
        item = QTreeWidgetItem(self.tree)
        item.setText(0, entry[0])
        item.setText(1, entry[1])
        item.setText(2, entry[2])
        item.setText(3, entry[3])
        item.setText(4, entry[4])
        item.setText(5, entry[5])