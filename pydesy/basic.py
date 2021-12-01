from pydesy.gmath import *


class Point:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x = x
        self.y = y
        self.z = z

    def get_dict(self):
        return {"x": self.x, "y": self.y, "h": self.z}

    def get_list_h(self):
        return [self.x, self.y, self.z]

    def get_list_v(self):
        return [
            [self.x],
            [self.y],
            [self.z]
        ]

    def from_list(self, array):
        self.x, self.y, self.z = array[0], array[1], array[2]

    def dgt(self, d: float, a: float):
        return direct_geo_task(self, d, a)

    def igt(self, point) -> list[float]:
        return inverse_geo_task(self, point)

    def dist2(self, point) -> float:
        return distance2d(self, point)

    def dist3(self, point) -> float:
        return distance3d(self, point)

    def reverse(self):
        self.x, self.y = self.y, self.x

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(other.x + self.x, other.y + self.y, other.z + self.z)
        else:
            return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Point):
            return Point(other.x * self.x, other.y * self.y, other.z * self.z)

        elif isinstance(other, int) or isinstance(other, float):
            return Point(other * self.x, other * self.y, other * self.z)

        else:
            return NotImplemented

    def __pow__(self, power, modulo=None):
        return Point(self.x ** power, self.y ** power, self.z ** power)

    def __neg__(self):
        return Point(-self.x, -self.y, -self.z)

    def __pos__(self):
        return Point(self.x, self.y, self.z)

    def __repr__(self):
        return f"<x: {self.x}, y: {self.y}, h: {self.z}>"

    def __str__(self):
        return f"<x: {self.x}, y: {self.y}, h: {self.z}>"


# Direct geodetic task
def direct_geo_task(point: Point, d, a) -> Point:
    return Point(point.x + d * cos(a), point.y + d * sin(a))


# Inverse geodetic task
def inverse_geo_task(point1: Point, point2: Point) -> list[float]:
    dx, dy = point2.x - point1.x, point2.y - point1.y
    d = point1.dist2(point2)
    r = atan(abs(dy / dx))

    a = 0
    if dx > 0 and dy > 0:
        a = r
    elif dx < 0 < dy:
        a = 180 - r
    elif dx < 0 and dy < 0:
        a = 180 + r
    elif dx > 0 > dy:
        a = 360 - r
    elif dx == 0:
        if dy > 0:
            a = 90
        elif dy < 0:
            a = 270
    elif dy == 0:
        if dx > 0:
            a = 0
        elif dx < 0:
            a = 180
    else:
        a = None

    return d, a


# Horizontal distance
def horizontal_distance(s: float = 0, v: float = 0) -> float:
    return s * cos(v)

# Distance between Point1 and Point2
def distance2d(point1: Point, point2: Point) -> float:
    return math.sqrt((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2)

def distance3d(point1: Point, point2: Point) -> float:
    return math.sqrt((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2 + (point2.z - point1.z) ** 2)