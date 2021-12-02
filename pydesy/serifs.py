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
    def __init__(self, pointGroups: list[list[Point]]):
        self.pointGroups = pointGroups

    def set_side_lengths(self, sideLengthGroups: list[list[float]]):
        self.sideLengthGroups = sideLengthGroups

    def calculate_serif(self) -> Point:
        self.calculatedPoints = list()
        self.gammas = list()
        for i, points in enumerate(self.pointGroups):
            basis, directionAngle = points[0].igt(points[1])
            gamma, sigma, betta = three_sides(basis, self.sideLengthGroups[i][0], self.sideLengthGroups[i][1])
            correctedDirectionAngle = revs(directionAngle - betta)
            self.calculatedPoints.append(points[0].dgt(self.sideLengthGroups[i][0], correctedDirectionAngle))
            self.gammas.append(gamma)
            if i == len(self.pointGroups):
                correctedDirectionAngle = revs(directionAngle + sigma)
                self.calculatedPoints.append(points[1].dgt(self.sideLengthGroups[i][1], correctedDirectionAngle))

        self.calculatedPoint = Point()
        for point in self.calculatedPoints:
            self.calculatedPoint += point * (1 / len(self.calculatedPoints))
        return self.calculatedPoint

    def calculate_accuracy_score(self, lenghtError: float) -> list[float]:
        self.errors = list()
        for gamma in self.gammas:
            self.errors.append((lenghtError * sqrt(2) / sin(gamma))**2)
        return sqrt(sum(self.errors)) / len(self.errors)

    def draw_serif(self):
        plt.figure("Linear serif")
        plt.text(self.calculatedPoint.y, self.calculatedPoint.x, "P")
        for i, points in enumerate(self.pointGroups):
            plt.plot([points[0].y, self.calculatedPoint.y], [points[0].x, self.calculatedPoint.x], linestyle="--", color="blue", marker=".")
            plt.text(points[0].y, points[0].x, f"{i}")
            if i == len(self.pointGroups) - 1:
                plt.plot([points[1].y, self.calculatedPoint.y], [points[1].x, self.calculatedPoint.x], linestyle="--", color="blue", marker=".")
                plt.text(points[1].y, points[1].x, f"{i}")
            plt.plot([points[0].y, points[1].y], [points[0].x, points[1].x], color="red", marker="^")
        plt.xlabel("y")
        plt.ylabel("x")
        plt.title("Linear serif")
        plt.show()

