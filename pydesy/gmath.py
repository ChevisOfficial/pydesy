import math

r = 180 / math.pi * 3600

def angle(d : float = 0, m : float = 0, s : float = 0) -> float:
    return revs(d + m / 60 + s / 3600)

def angdms(degrees : float = 0):
    degrees = revs(degrees)
    d = int(degrees)
    m = int((degrees - int(degrees)) * 60)
    s = ((degrees - int(degrees)) * 60 - m) * 60
    return {"d" : d, "m" : m, "s" : s}

def revs(degrees : float) -> float:
    while degrees > 360:
        degrees -= 360
    while degrees < 0:
        degrees += 360
    return degrees

def rad(a : float = 1) -> float:
    return a * math.pi / 180

def deg(a : float = 1) -> float:
    return a * 180 / math.pi

def dirang(direction : float, horizontalAngle : float) -> float:
    return revs(angle(direction + horizontalAngle) + (-180 if angle(direction + horizontalAngle) >= 180 else 180))

def change_angle(a : float) -> float:
    return revs(angle(360 - a))

def sin(a : float = 0) -> float:
    return math.sin(rad(a))

def cos(a : float = 0) -> float:
    return math.cos(rad(a))

def tan(a : float = 0) -> float:
    return math.tan(rad(a))

def cot(a : float = 0) -> float:
    return 1 / math.tan(rad(a))

def asin(x : float) -> float:
    return deg(math.asin(x))

def acos(x : float) -> float:
    return deg(math.acos(x))

def atan(x : float) -> float:
    return deg(math.atan(x))

def acot(x : float) -> float:
    return deg(math.atan(1 / x))

def sqrt(x : float) -> float:
    return math.sqrt(x)