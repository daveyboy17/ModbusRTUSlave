import json
from pathlib import Path


class Configuration:

    def __init__(self, filename="configs/default.json"):
        self.filename = Path(filename)

        self.data = {
            "slave_address": 1,
            "baudrate": 9600,
            "parity": "N",
            "stop_bits": 1,
            "registers": {}
        }

    def load(self):
        if self.filename.exists():
            with open(
                self.filename,
                "r"
            ) as f:
                self.data.update(
                    json.load(f)
                )

    def save(self):
        self.filename.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            self.filename,
            "w"
        ) as f:
            json.dump(
                self.data,
                f,
                indent=4
            )