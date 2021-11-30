import matplotlib.pyplot as plt

from pydesy.basic import *
from pydesy.gmath import *

class PolarSerif:
    def __init__(self, A, B):
        self.A = A
        self.B = B
        self.directionAngle = A.igt(B)["a"]

    def set_side_lenghts(self, sideLenghts):
        self.sideLenghts = sideLenghts

    def set_horizontal_angles(self, horizontalAngles):
        self.horizontalAngles = horizontalAngles

    def set_points(self, points):
        self.points = points

    def calculate_serif(self):
        self.points = []
        for i in range(len(self.sideLenghts)):
            directionAngle = revs(self.directionAngle + self.horizontalAngles[i])
            print(directionAngle)
            dx = self.sideLenghts[i] * cos(directionAngle)
            dy = self.sideLenghts[i] * sin(directionAngle)
            self.points.append(Point(self.A.x + dx, self.A.y + dy))
        return self.points

    def calculate_accuracy_score(self, lenghtError, angleError):
        self.errors = []
        for i in range(len(self.points)):
            self.errors.append(self.sideLenghts[i] ** 2 * angleError ** 2 / r ** 2 + lenghtError ** 2)
        return self.errors

    def draw_serif(self):
        plt.figure("Polar serif")
        plt.text(self.A.y, self.A.x, "A")
        plt.text(self.B.y, self.B.x, "B")
        for i, point in enumerate(self.points):
            plt.plot([self.A.y, point.y], [self.A.x, point.x], linestyle="--", color="red", marker=".")
            plt.text(point.y, point.x, f"{i}")

        plt.plot([self.A.y, self.B.y], [self.A.x, self.B.x], color="blue", marker="^")
        plt.xlabel("y")
        plt.ylabel("x")
        plt.title("Polar serif")
        plt.show()