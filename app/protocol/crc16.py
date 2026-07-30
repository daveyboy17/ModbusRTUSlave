def calculate(data: bytes) -> int:
    """
    Calculate Modbus RTU CRC16.
    """

    crc = 0xFFFF

    for byte in data:

        crc ^= byte

        for _ in range(8):

            if crc & 0x0001:
                crc >>= 1
                crc ^= 0xA001

            else:
                crc >>= 1

    return crc



def append_crc(data: bytes) -> bytes:

    crc = calculate(data)

    return data + bytes(
        [
            crc & 0xFF,
            (crc >> 8) & 0xFF
        ]
    )



def verify(data: bytes) -> bool:

    if len(data) < 4:
        return False

    received = (
        data[-2]
        |
        (data[-1] << 8)
    )

    calculated = calculate(
        data[:-2]
    )

    return received == calculated