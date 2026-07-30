import serial.tools.list_ports


def available_ports():

    ports = []

    for port in serial.tools.list_ports.comports():
        ports.append(port.device)

    return sorted(ports)