

class M1:
    def __init__(self, x1, x2):
        self.x1 = x1
        self.x2 = x2

    def __call__(self, input_val: int) -> float:
        if input_val < self.x1:
            return 1
        if input_val > self.x2:
            return 0
        return 1 - (1 / (self.x2 - self.x1)) * (input_val - self.x1)

class M2:
    def __init__(self, x1, x2):
        self.x1 = x1
        self.x2 = x2
        self.centerx = (x1 + x2) / 2

    def __call__(self, input_val: int) -> float:
        if input_val == self.centerx:
            return 1
        if input_val < self.x1 or input_val > self.x2:
            return 0
        if input_val < self.centerx:
            return 1 + (1 / (self.centerx - self.x1)) * (input_val - self.centerx)
        else:
            return 1 - (1 / (self.x2 - self.centerx)) * (input_val - self.centerx)

class M3:
    def __init__(self, x1, x2):
        self.x1 = x1
        self.x2 = x2

    def __call__(self, input_val: int) -> float:
        if input_val < self.x1:
            return 0
        if input_val > self.x2:
            return 1
        return (1 / (self.x2 - self.x1)) * (input_val - self.x1)


class Aggregator:
    pass