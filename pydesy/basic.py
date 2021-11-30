import numpy as np
from pydesy.gmath import *

class Point:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
        
    def get_dict(self):
        return {"x" : self.x, "y" : self.y, "h" : self.z}

    def get_list_h(self):
        return [self.x, self.y, self.z]

    def get_list_v(self):
        return [
            [self.x],
            [self.y],
            [self.z]
        ]

    def get_array_h(self):
        return np.array(self.getList())

    def get_array_v(self):
        return np.array([
            [self.x],
            [self.y],
            [self.z]
        ])

    def dgt(self, d=0, a=0):
        return direct_geo_task(self.x, self.y, d, a)
    
    def igt(self, point):
        return inverse_geo_task(self.x, self.y, point.x, point.y)


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
        
    def __neg__(self):
        return Point(-self.x, -self.y, -self.z)

    def __pos__(self):
        return Point(self.x, self.y, self.z)
    
    def __repr__(self):
        return f"x: {self.x}, y: {self.y}, h: {self.z}"
    
    def __str__(self):
        return f"x: {self.x}, y: {self.y}, h: {self.z}"


#Direct geodetic problem
def direct_geo_task(x=0, y=0, d=0, a=0):
    return {"x" : x + d * cos(a), "y" : y + d * sin(a)}


#Invert geodetic problem
def inverse_geo_task(x1=0, y1=0, x2=0, y2=0):
    dx, dy = x2 - x1, y2 - y1
    d = sqrt(pow(dx,2)+pow(dy,2))
    r = atan(abs(dy / dx))
    
    if dx > 0 and dy > 0:
        a = r
    elif dx < 0 and dy > 0:
        a = 180 - r
    elif dx < 0 and dy < 0:
        a = 180 + r
    elif dx > 0 and dy < 0:
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
        
    return {"d" : d, "a" : a}


#Horizontal distance
def horizontal_distance(s=0, v=0):
    return s * cos(v)