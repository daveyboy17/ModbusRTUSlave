from .crc16 import append_crc, verify
from .decoder import describe


class ModbusException(Exception):

    def __init__(self, code):
        self.code = code


class ModbusRTUSlave:

    def __init__(
        self,
        slave_address,
        register_bank
    ):
        self.address = slave_address
        self.registers = register_bank


    def process(self, frame: bytes) -> bytes | None:

        if not verify(frame):
            # print(f"Invalid CRC: {frame.hex()}")
            return None

        if frame[0] != self.address:
            return None
            
        # pass frame to the decoder to describe.
        # and send the description to the 
        # packet monitor.
        # self.packet.description = describe(frame)

        if frame[0] == self.address:
            print(f"Received: {frame.hex()}")

        # Build the response.
        function = frame[1]

        try:
            if function == 3:
                response = self.read_holding(frame)

            elif function == 4:
                response = self.read_input(frame)

            elif function == 6:
                response = self.write_single(frame)

            elif function == 16:
                response = self.write_multiple(frame)

            else:
                print(f"Unsupported function code: {function}")
                return self.exception(
                    function,
                    1
                )

        except KeyError:
            print(f"Invalid register address in frame: {frame.hex()}")
            return self.exception(
                function,
                2
            )

        if frame[0] == 1:
            print(f"Response: {response.hex()}")

        return append_crc(response)


    def read_holding(self, frame):
        start = int.from_bytes(
            frame[2:4],
            "big"
        )

        count = int.from_bytes(
            frame[4:6],
            "big"
        )

        print(f"Read Holding Registers: start={start}, count={count}")
        
        if count < 1 or count > 125:
            return self.exception(
                function,
                3
            )

        values = []

        for addr in range(
            start,
            start + count
        ):
            values.append(
                # self.registers.read_holding(addr)
                addr
            )

        response = bytes(
            [
                self.address,
                3,
                count * 2
            ]
        )

        for value in values:
            response += value.to_bytes(
                2,
                "big"
            )

        return response


    def read_input(self, frame):
        start = int.from_bytes(
            frame[2:4],
            "big"
        )

        count = int.from_bytes(
            frame[4:6],
            "big"
        )
        
        if count < 1 or count > 125:
            return self.exception(
                function,
                3
            )

        values = []

        for addr in range(
            start,
            start + count
        ):
            values.append(
                self.registers.input[addr].value
            )

        response = bytes(
            [
                self.address,
                4,
                count * 2
            ]
        )

        for value in values:
            response += value.to_bytes(
                2,
                "big"
            )

        return response


    def write_single(self, frame):
        address = int.from_bytes(
            frame[2:4],
            "big"
        )

        value = int.from_bytes(
            frame[4:6],
            "big"
        )

        self.registers.write_holding(
            address,
            value
        )

        return frame[:6]


    def write_multiple(self, frame):
        start = int.from_bytes(
            frame[2:4],
            "big"
        )

        count = int.from_bytes(
            frame[4:6],
            "big"
        )
        
        if count < 1 or count > 123:
            return self.exception(
                function,
                3
            )

        byte_count = frame[6]
        index = 7

        for address in range(
            start,
            start + count
        ):
            value = int.from_bytes(
                frame[index:index+2],
                "big"
            )

            self.registers.write_holding(
                address,
                value
            )

            index += 2

        return bytes(
            [
                self.address,
                16,
                frame[2],
                frame[3],
                frame[4],
                frame[5]
            ]
        )


    def exception(
        self,
        function,
        code
    ):
        return append_crc(
            bytes(
                [
                    self.address,
                    function | 0x80,
                    code
                ]
            )
        )