from PySide6.QtWidgets import QMessageBox
from .models import Register

from app.services.serial_worker import SerialWorker
from app.services.ports import available_ports
from app.protocol.modbus_rtu import ModbusRTUSlave

from .packet_log import PacketMonitor
from .models import PacketLogEntry

from app.services.response_controller import (
    ResponseController
)

from app.statistics import (
    CommunicationStatistics
)


from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QGroupBox,
    QCheckBox,
    QFormLayout
)

from .register_bank import RegisterBank
from .configuration import Configuration


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Modbus RTU Slave Simulator"
        )

        self.resize(
            900,
            800
        )

        self.registers = RegisterBank()

        self.config = Configuration()
        self.config.load()

        self.build_ui()

        self.modbus = ModbusRTUSlave(
            self.slave.value(),
            self.registers
        )
        
        # Serial worker panel
        self.serial_worker = SerialWorker()

        self.serial_worker.received.connect(
            self.process_frame
        )

        self.serial_worker.error.connect(
            self.serial_error
        )
        
        self.serial_worker.received.connect(
            self.record_rx
        )

        self.serial_worker.transmitted.connect(
            self.record_tx
        )
        
        self.response_controller = ResponseController()

        self.statistics = CommunicationStatistics()


    def build_ui(self):
        """
        As the name suggests this builds the GUI.
        """
        
        root = QWidget()
        layout = QVBoxLayout()  # Vertical Box layout

        root.setLayout(layout)

        self.setCentralWidget(root)

        # Start with the serial port settings at the top.
        serial_box = QGroupBox(
            "Serial Settings"
        )

        serial_layout = QHBoxLayout()  # Horizontal Box layout

        self.port = QComboBox()
        self.port.addItems(
            available_ports()
        )

        self.baud = QComboBox()
        self.baud.addItems(
            [
                "9600",
                "19200",
                "38400"
            ]
        )

        self.slave = QSpinBox()
        self.slave.setRange(
            1,
            247
        )

        self.slave.setValue(
            self.config.data["slave_address"]
        )

        self.connect_button = QPushButton(
            "Connect"
        )

        self.connect_button.clicked.connect(
            self.toggle_serial
        )

        serial_layout.addWidget(
            self.port
        )

        serial_layout.addWidget(
            QLabel("Port")
        )

        serial_layout.addWidget(
            self.baud
        )

        serial_layout.addWidget(
            QLabel("Baud")
        )

        serial_layout.addWidget(
            self.slave
        )

        serial_layout.addWidget(
            QLabel("Slave")
        )
        
        serial_layout.addWidget(
            self.connect_button
        )

        serial_layout.addWidget(
            QLabel("connect")
        )

        serial_box.setLayout(
            serial_layout
        )

        layout.addWidget(
            serial_box
        )

        # Add the Holding register settings.
        self.holding_table = self.create_register_table("Holding Registers")

        add = QPushButton("Add Holding")
        delete = QPushButton("Delete Holding")

        add.clicked.connect(
            self.add_holding_register
        )

        delete.clicked.connect(
            self.delete_holding_register
        )

        # holding_button_layout = QHBoxLayout()  # Horizontal Box layout

        layout.addWidget(add)
        layout.addWidget(delete)
        # holding_button_layout.addWidget(add)
        # holding_button_layout.addWidget(delete)

        # self.holding_table.setLayout(
        #     holding_button_layout
        # )

        layout.addWidget(
            self.holding_table
        )

        # Add the Input register settings.
        self.input_table = self.create_register_table("Input Registers")

        add = QPushButton("Add Input")
        delete = QPushButton("Delete Input")

        add.clicked.connect(
            self.add_input_register
        )

        delete.clicked.connect(
            self.delete_input_register
        )

        layout.addWidget(add)
        layout.addWidget(delete)

        layout.addWidget(
            self.input_table
        )

        self.refresh_tables()

        # Add the packet monitor window
        self.packet_monitor = PacketMonitor()

        layout.addWidget(
            self.packet_monitor
        )
        
        # Add the simulator settings.
        simulation_box = QGroupBox(
            "Simulation"
        )

        simulation_layout = QFormLayout()

        self.delay_enable = QCheckBox(
            "Delay Response"
        )

        self.delay_value = QSpinBox()

        self.delay_value.setRange(
            0,
            5000
        )

        self.delay_value.setValue(
            100
        )

        self.drop_response = QCheckBox(
            "Drop Response"
        )

        self.bad_crc = QCheckBox(
            "Corrupt CRC"
        )

        simulation_layout.addRow(
            self.delay_enable
        )

        simulation_layout.addRow(
            "Delay (ms)",
            self.delay_value
        )

        simulation_layout.addRow(
            self.drop_response
        )

        simulation_layout.addRow(
            self.bad_crc
        )

        simulation_box.setLayout(
            simulation_layout
        )

        layout.addWidget(
            simulation_box
        )

    # Register Table Controls.
    
    def create_register_table(self, title):
        """Used to create both Holding and Input
        Register tables."""
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(
            [
                "Register",
                "Name",
                "Value",
                "Description"
            ]
        )

        table.setRowCount(0)

        return table


    def refresh_tables(self):
        self.populate(
            self.holding_table,
            self.registers.holding,
            40001
        )

        self.populate(
            self.input_table,
            self.registers.input,
            30001
        )


    def populate(self, table, registers, offset):
        table.setRowCount(
            len(registers)
        )

        for row, reg in enumerate(
            registers.values()
        ):
            table.setItem(
                row,
                0,
                QTableWidgetItem(
                    str(offset + reg.address)
                )
            )

            table.setItem(
                row,
                1,
                QTableWidgetItem(
                    reg.name
                )
            )

            table.setItem(
                row,
                2,
                QTableWidgetItem(
                    str(reg.value)
                )
            )

            table.setItem(
                row,
                3,
                QTableWidgetItem(
                    reg.description
                )
            )
            
    def add_holding_register(self):
        address = self.registers.next_holding_address()

        self.registers.add_holding(
            Register(
                address=address,
                value=0
            )
        )

        self.refresh_tables()


    def add_input_register(self):
        address = self.registers.next_input_address()

        self.registers.add_input(
            Register(
                address=address,
                value=0
            )
        )

        self.refresh_tables()


    def delete_holding_register(self):
        row = self.holding_table.currentRow()

        if row < 0:
            return

        address = (
            int(
                self.holding_table.item(row,0).text()
            )
            -
            40001
        )

        self.registers.remove_holding(address)
        self.refresh_tables()


    def delete_input_register(self):
        row = self.input_table.currentRow()

        if row < 0:
            return

        address = (
            int(
                self.input_table.item(row,0).text()
            )
            -
            30001
        )

        self.registers.remove_input(address)
        self.refresh_tables()
        
        
    # Serial Port Controls.
    
    def toggle_serial(self):
        if self.serial_worker.running:
            self.serial_worker.stop()

            self.connect_button.setText(
                "Connect"
            )

            return

        self.serial_worker.configure(
            self.port.currentText(),
            int(self.baud.currentText())
        )

        self.modbus.address = (
            self.slave.value()
        )

        self.serial_worker.start()

        self.connect_button.setText(
            "Disconnect"
        )

    # Packet Monitor Controls.
    
    def process_frame(self, frame):
        """Process a received frame and
        generate a response if required."""
        response = self.modbus.process(frame)
        
        # Modify the response if needed.
        response = self.response_controller.apply(response)

        # Send the response.
        if response:
            self.serial_worker.send(response)


    def serial_error(self, message):
        print(
            "Serial error:",
            message
        )
        
        
    def record_rx(self, frame):
        self.statistics.received(len(frame))

        self.packet_monitor.add_packet(
            PacketLogEntry.create(
                "RX",
                frame
            )
        )


    def record_tx(self, frame):
        self.statistics.transmitted(len(frame))

        self.packet_monitor.add_packet(
            PacketLogEntry.create(
                "TX",
                frame
            )
        )


    def update_simulation(self):
        if self.drop_response.isChecked():
            self.response_controller.mode = (
                ResponseMode.DROP
            )

        elif self.bad_crc.isChecked():
            self.response_controller.mode = (
                ResponseMode.CORRUPT_CRC
            )

        elif self.delay_enable.isChecked():
            self.response_controller.mode = (
                ResponseMode.DELAY
            )

            self.response_controller.delay_ms = (
                self.delay_value.value()
            )

        else:
            self.response_controller.mode = (
                ResponseMode.NORMAL
            )