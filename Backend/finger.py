import math


class Finger:

    def __init__(self, tip, base, palm_size):
        self.tip = tip
        self.base = base
        self.palm_size = palm_size

    def get_angle(self):
        distance = math.hypot(self.tip.x - self.base.x, self.tip.y - self.base.y)
        ratio = max(0.3, min(1.0, distance / self.palm_size))
        return int((ratio - 0.3) / (1.0 - 0.3) * 180)



