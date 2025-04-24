import numpy as np
from typing import Mapping
class HSVColor:
    def __init__(self, h: int, s: int, v: int):
        self.hsv = np.array([h, s, v], dtype=np.uint16)

    @property
    def h(self):
        return self.hsv[0]
    @h.setter
    def h(self, value: int):
        self.hsv[0] = value
    @property
    def s(self):
        return self.hsv[1]
    @s.setter
    def s(self, value: int):
        self.hsv[1] = value
    @property
    def v(self):
        return self.hsv[2]
    @v.setter
    def v(self, value: int):
        self.hsv[2] = value

class HSVColorRange:
    def __init__(self, lower: HSVColor, upper: HSVColor):
        self.lower = lower
        self.upper = upper
    def get_lower(self):
        return self.lower.hsv
    def get_upper(self):
        return self.upper.hsv
    
DetectorDict = Mapping[str, list[HSVColorRange] | HSVColorRange]
    