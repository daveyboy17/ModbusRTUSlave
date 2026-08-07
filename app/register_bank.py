from .models import Register


class RegisterBank:

    def __init__(self):
        self.holding = {}
        self.input = {}

    def add_holding(self, register):
        self.holding[register.address] = register

    def add_input(self, register):
        self.input[register.address] = register

    def remove_holding(self, address):
        self.holding.pop(address, None)

    def remove_input(self, address):
        self.input.pop(address, None)

    def next_holding_address(self):
        if not self.holding:
            return 0

        return max(self.holding.keys()) + 1

    def next_input_address(self):
        if not self.input:
            return 0

        return max(self.input.keys()) + 1

    def read_holding(self, address):
        print(f"Holding register: {address}")
        return self.holding[address].value
        # return 10

    def write_holding(self, address, value):
        self.holding[address].set_value(value)

    def export(self):
        return {
            "holding": [
                r.to_dict()
                for r in self.holding.values()
            ],

            "input": [
                r.to_dict()
                for r in self.input.values()
            ]
        }

    def import_data(self, data):
        self.holding.clear()
        self.input.clear()

        for item in data.get("holding", []):
            reg = Register.from_dict(item)
            self.add_holding(reg)

        for item in data.get("input", []):
            reg = Register.from_dict(item)
            self.add_input(reg)