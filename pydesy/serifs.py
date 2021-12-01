import matplotlib.pyplot as plt

from pydesy.basic import *
from pydesy.gmath import *
from pydesy.geometry import *

class PolarSerif:
    def __init__(self, A, B):
        self.A = A
        self.B = B
        self.directionAngle = A.igt(B)[1]

    def set_side_lengths(self, sideLengths: list[float]):
        self.sideLengths = sideLengths

    def set_horizontal_angles(self, horizontalAngles: list[float]):
        self.horizontalAngles = horizontalAngles

    def set_points(self, points: list):
        self.points = points

    def calculate_serif(self) -> list[Point]:
        self.points = list()
        for i in range(len(self.sideLenghts)):
            directionAngle = revs(self.directionAngle + self.horizontalAngles[i])
            print(directionAngle)
            dx = self.sideLengths[i] * cos(directionAngle)
            dy = self.sideLengths[i] * sin(directionAngle)
            self.points.append(Point(self.A.x + dx, self.A.y + dy))
        return self.points

    def calculate_accuracy_score(self, lenghtError: float, angleError: float) -> list[float]:
        self.errors = list()
        for i in range(len(self.points)):
            self.errors.append(self.sideLengths[i] ** 2 * angleError ** 2 / r ** 2 + lenghtError ** 2)
        return self.errors

    def draw_serif(self):
        plt.figure("Polar serif")
        plt.text(self.A.y, self.A.x, "A")
        plt.text(self.B.y, self.B.x, "B")
        for i, point in enumerate(self.points):
            plt.plot([self.A.y, point.y], [self.A.x, point.x], linestyle="--", color="blue", marker=".")
            plt.text(point.y, point.x, f"{i}")

        plt.plot([self.A.y, self.B.y], [self.A.x, self.B.x], color="red", marker="^")
        plt.xlabel("y")
        plt.ylabel("x")
        plt.title("Polar serif")
        plt.show()


class LinearSerif:
    def __init__(self, points: list[Point]):
        self.points = points

    def set_side_lengths(self, sideLengths: list[float]):
        self.sideLengths = sideLengths

    def calculate_serif(self) -> Point:
        self.calculatedPoints = list()
        self.gammas = list()
        for i in range(1, len(self.points)):
            basis, directionAngle = self.points[i-1].igt(self.points[i])
            gamma, sigma, betta = three_sides(basis, self.sideLengths[i-1], self.sideLengths[i])
            correctedDirectionAngle = revs(directionAngle - betta)
            self.calculatedPoints.append(self.points[i-1].dgt(self.sideLengths[i-1], correctedDirectionAngle))
            self.gammas.append(gamma)
            if i == len(self.points):
                correctedDirectionAngle = revs(directionAngle + sigma)
                self.calculatedPoints.append(self.points[i].dgt(self.sideLengths[i], correctedDirectionAngle))

        self.calculatedPoint = Point()
        for point in self.calculatedPoints:
            self.calculatedPoint += point * (1 / len(self.calculatedPoints))
        return self.calculatedPoint

    def calculate_accuracy_score(self, lenghtError: float) -> list[float]:
        self.errors = list()
        for gamma in self.gammas:
            self.errors.append(lenghtError * sqrt(2) / sin(gamma))
        return sum(self.errors) / len(self.errors)

    def draw_serif(self):
        plt.figure("Linear serif")
        plt.text(self.calculatedPoint.y, self.calculatedPoint.x, "?")
        for i, point in enumerate(self.points):
            plt.plot([point.y, self.calculatedPoint.y], [point.x, self.calculatedPoint.x], linestyle="--", color="blue", marker=".")
            plt.text(point.y, point.x, f"{i}")
        for i in range(1, len(self.points)):
            plt.plot([self.points[i-1].y, self.points[i].y], [self.points[i-1].x, self.points[i].x], color="red", marker="^")
        plt.xlabel("y")
        plt.ylabel("x")
        plt.title("Linear serif")
        plt.show()