from dataclasses import dataclass, asdict
import decoder


@dataclass
class Register:
    """
    Represents a Modbus register.

    Addresses are internally zero-based.
    """

    address: int
    value: int = 0
    name: str = ""
    description: str = ""

    def set_value(self, value: int):
        value = int(value)

        if not 0 <= value <= 65535:
            raise ValueError(
                "Register value must be between 0 and 65535"
            )

        self.value = value

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(
            address = data["address"],
            value = data.get("value", 0),
            name = data.get("name", ""),
            description = data.get("description", "")
        )
        

from datetime import datetime


@dataclass
class PacketLogEntry:

    timestamp: str
    direction: str
    data: bytes
    description: str = ""

    @classmethod
    def create(
        cls,
        direction,
        data,
        description=""
    ):
        return cls(
            timestamp=datetime.now().strftime(
                "%H:%M:%S.%f"
            )[:-3],
            direction = direction,
            data = data,
            # description = description
            description = decoder.describe(data)
        )

    def hex_string(self):
        return " ".join(
            f"{b:02X}"
            for b in self.data
        )
