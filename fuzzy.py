from typing import List, Union

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
    def __init__(self, input_sets: List[Union[M1, M2, M3]], output_sets: List[Union[M1, M2, M3]], output_upper_bound: int): 
        self.input_sets = input_sets
        self.output_sets = output_sets
        self.output_upper_bound = output_upper_bound
    
    def aggregate(self, input_val):
        infs = [m(input_val) for m in self.input_sets]
        x, y = [], []
        for i in range(0, self.output_upper_bound + 1):
            x.append(i)
            y.append(max([min(inf, out_set(i)) for inf, out_set in zip(infs, self.output_sets)]))

        return (x, y), infs


class Defuzzy():
    def centroid(self, x: List[Union[int, float]], y: List[Union[int, float]]):
        return sum(y * x for x, y in zip(x, y)) / sum(y)