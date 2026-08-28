import math


class Finger:

    def __init__(self, tip, base, palm_size):
        self.tip = tip
        self.base = base
        self.palm_size = palm_size

    def get_angle(self):
        distance = math.hypot(self.tip.x - self.base.x, self.tip.y - self.base.y)
        ratio = ratio = max(0.3, min(1.0, distance / self.palm_size))
        return int((ratio - 0.3) / (1.0 - 0.3) * 180)

class FakePoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

test_finger = Finger(
    tip=FakePoint(0.5, 0.2),
    base=FakePoint(0.5, 0.5),
    palm_size=0.3
)

print(test_finger.get_angle())

