import math

r = 180 / math.pi * 3600

def angle(d=0, m=0, s=0):
    return revs(d + m / 60 + s / 3600)

def angdms(degrees=0):
    degrees = revs(degrees)
    d = int(degrees)
    m = int((degrees - int(degrees)) * 60)
    s = ((degrees - int(degrees)) * 60 - m) * 60
    return {"d" : d, "m" : m, "s" : s}

def revs(degrees):
    while degrees > 360:
        degrees -= 360
    while degrees < 0:
        degrees += 360
    return degrees

def rad(a=1):
    return a * math.pi / 180

def deg(a=1):
    return a * 180 / math.pi

def dirang(direction, horizontalAngle):
    return revs(angle(direction + horizontalAngle) + (-180 if angle(direction + horizontalAngle) >= 180 else 180))

def change_angle(a):
    return revs(angle(360 - a))

def sin(a=0):    
    return math.sin(rad(a))

def cos(a=0):
    return math.cos(rad(a))

def tan(a=0):
    return math.tan(rad(a))

def cot(a=0):
    return 1 / math.tan(rad(a))

def asin(x):
    return deg(math.asin(x))

def acos(x):
    return deg(math.acos(x))

def atan(x):
    return deg(math.atan(x))

def acot(x):
    return deg(math.atan(1 / x))

def sqrt(x):
    return math.sqrt(x)