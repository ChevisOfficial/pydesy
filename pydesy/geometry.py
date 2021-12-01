from pydesy.gmath import *
from pydesy.basic import *
def polygon_area(polygon : list) -> float:
    countPolygons = len(polygon)    
    if countPolygons < 3:
        raise Exception("To solve this problem, you need at least 3 points")
        
    firstSum = sum([polygon[i].x * polygon[i+1].y for i in range(countPolygons - 1)]) +  polygon[countPolygons - 1].x * polygon[0].y
    secondSum = sum([polygon[i+1].x * polygon[i].y for i in range(countPolygons - 1)]) +  polygon[countPolygons - 1].y * polygon[0].x
    return (firstSum - secondSum) / 2

def three_sides(a : float, b : float, c : float) -> list[float]:
    A = acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))
    B = acos((a ** 2 + c ** 2 - b ** 2) / (2 * a * c))
    C = acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))

    return [A, B, C]