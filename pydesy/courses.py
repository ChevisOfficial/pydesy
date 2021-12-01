#Сторонние библиотеки
import matplotlib.pyplot as plt

from pydesy.gmath import *
from pydesy.basic import *

from enum import Enum
from datetime import datetime

class Scales(Enum):
    S1_5000 = 1
    S1_2000 = 2
    S1_1000 = 3
    S1_500 = 4

class TheodoliteRequirement:
    requirement = {
        Scales.S1_5000 : {
            "maximum_length" : 1200,
            "maximum_number_of_sides" : 6,
            "limiting_side_length" : 300,
            "limit_relative_error": 1 / 2000,
            "limit_horizontal_discrepancy": lambda x: 1 * sqrt(x)
        },
        
        Scales.S1_2000 : {
            "maximum_length" : 600,
            "maximum_number_of_sides" : 5,
            "limiting_side_length" : 200,
            "limit_relative_error": 1 / 2000,
            "limit_horizontal_discrepancy": lambda x: 1 * sqrt(x)
        },
        
        Scales.S1_1000 : {
            "maximum_length" : 300,
            "maximum_number_of_sides" : 3,
            "limiting_side_length" : 150,
            "limit_relative_error": 1 / 2000,
            "limit_horizontal_discrepancy": lambda x: 1 * sqrt(x)
        },
        
        Scales.S1_500 : {
            "maximum_length" : 100,
            "maximum_number_of_sides" : 2,
            "limiting_side_length" : 100,
            "limit_relative_error": 1 / 2000,
            "limit_horizontal_discrepancy": lambda x: 1 * sqrt(x)
        }
        
    }
    
    def setScaleRequirement(typeScale, values):
        TheodoliteRequirement.requirement[typeScale] = values
                                          
class TheodoliteCourse: 
    def __init__(self, scale=Scales.S1_500):
        self.scale = scale
    
    def set_scale(self, scale : float):
        self.scale = scale
    
    def set_points(self, startPoint : Point, endPoint : Point):
        self.startPoint =  startPoint
        self.endPoint = endPoint
        
    def set_direction_angles(self, startDirectionAngle : list, endDirectionAngle : list):
        self.startDirectionAngle = startDirectionAngle
        self.endDirectionAngle = endDirectionAngle

    def set_horizontal_angles(self, horizontalAngles : list):
        self.horizontalAngles = horizontalAngles
        
    def set_side_lenghts(self, sideLenghts : list):
        self.sideLenghts = sideLenghts
        
    def set_average_excess(self, averageExcess : list):
        self.averageExcess = averageExcess
        
    def calculate_course(self) -> dict:
        self.errors = []
        self.horizontalDiscrepancy = (angle(sum(self.horizontalAngles)) - angle(self.endDirectionAngle - self.startDirectionAngle) - 180) * 60
        self.limitHorizontalDiscrepancy = TheodoliteRequirement.requirement[self.scale]["limit_horizontal_discrepancy"](len(self.horizontalAngles))
        
        if abs(self.horizontalDiscrepancy) > self.limitHorizontalDiscrepancy:
            self.errors.append(f"Horizontal angle residual is exceeded residual limit: {abs(self.horizontalDiscrepancy)} > {self.limitHorizontalDiscrepancy}")

        self.sumSideLenghts = sum(self.sideLenghts)
        if self.sumSideLenghts > TheodoliteRequirement.requirement[self.scale]["maximum_length"]:
            self.errors.append(f"The sum lengths of the theodolite course is greater than the specified value: {self.sumSideLenghts} > {TheodoliteRequirement.requirement[self.scale]['maximum_length']}")

        self.angleCorrection = -self.horizontalDiscrepancy / len(self.horizontalAngles)
        self.directionAngles = [angle(self.startDirectionAngle + 180 + angle(self.horizontalAngles[0], s = self.angleCorrection))]
        self.incrementsX, self.incrementsY = list(), list()
        for i in range(1, len(self.horizontalAngles)):
            self.directionAngles.append(angle(self.directionAngles[i-1] + 180 + angle(self.horizontalAngles[i], s = self.angleCorrection)))
            self.incrementsX.append(-cos(self.directionAngles[i-1]) * self.sideLenghts[i-1])
            self.incrementsY.append(-sin(self.directionAngles[i-1]) * self.sideLenghts[i-1])

        self.incrementXDiscrepancy = sum(self.incrementsX) - (self.endPoint.x - self.startPoint.x)
        self.incrementYDiscrepancy = sum(self.incrementsY) - (self.endPoint.y - self.startPoint.y)
        self.incrementXY = sqrt(self.incrementXDiscrepancy ** 2 + self.incrementYDiscrepancy ** 2)
        self.relativeError = self.incrementXY / self.sumSideLenghts
        
        if  self.relativeError > TheodoliteRequirement.requirement[self.scale]["limit_relative_error"]:
            self.errors.append(f"The relative distance error is greater than the allowable value: {self.relativeError} > {TheodoliteRequirement.requirement[self.scale]['limit_relative_error']}")
        
        self.incrementXCorrections = [-self.incrementXDiscrepancy * self.sideLenghts[i] / self.sumSideLenghts for i in range(len(self.sideLenghts))]
        self.incrementYCorrections = [-self.incrementYDiscrepancy * self.sideLenghts[i] / self.sumSideLenghts for i in range(len(self.sideLenghts))]
        self.points = [Point(self.startPoint.x + self.incrementsX[0] + self.incrementXCorrections[0], self.startPoint.y + self.incrementsY[0] + self.incrementYCorrections[0])]
        for i in range(1, len(self.sideLenghts)-1):
            self.points.append(Point(self.points[i-1].x + self.incrementsX[i] + self.incrementXCorrections[i], self.points[i-1].y + self.incrementsY[i] + self.incrementYCorrections[i]))
            if self.sideLenghts[i-1] > TheodoliteRequirement.requirement[self.scale]["limiting_side_length"]:
                self.errors.append(f"Side length is greater than the specified value: {self.sideLenghts[i-1]} > {TheodoliteRequirement.requirement[self.scale]['limiting_side_length']}")
        self.averageExcessDiscrepancy = sum(self.averageExcess) - (self.endPoint.h - self.startPoint.h)
        self.limitAverageExcessDiscrepancy = (0.04 * self.sumSideLenghts) / (100 * sqrt(len(self.sideLenghts)))

        if len(self.sideLenghts) > TheodoliteRequirement.requirement[self.scale]["maximum_number_of_sides"]:
            self.errors.append(f"Sides count is greater than the specified value: {len(self.sideLenghts)} > {TheodoliteRequirement.requirement[self.scale]['maximum_number_of_sides']}")

        if abs(self.averageExcessDiscrepancy) > self.limitAverageExcessDiscrepancy:
            self.errors.append(f"The discrepancy of excess is greater than the admissible discrepancy: {abs(self.averageExcessDiscrepancy)} > {self.limitAverageExcessDiscrepancy}")
        
        self.averageExcessCorrections = [-self.averageExcessDiscrepancy * self.sideLenghts[i] / self.sumSideLenghts for i in range(len(self.sideLenghts))]
        self.points[0].z = self.startPoint.h + self.averageExcess[0] + self.averageExcessCorrections[0]
        for i in range(1, len(self.averageExcess)-1):
            self.points[i].z = self.points[i-1].z + self.averageExcess[i] + self.averageExcessCorrections[i]
        return {
            "points" : self.points,
            "relativeError" : self.relativeError,
            "errors" : self.errors
        }
    
    def save_report(self, fileName : str):
        with open(fileName, "w") as report:
            report.write(f"Report at {datetime.now()}\n")
            report.write("Points:\n\tName\tX\tY\tH\n")
            report.write(f"\tstart\t{self.startPoint.x}\t{self.startPoint.y}\t{self.startPoint.h}\n")
            for i, point in enumerate(self.points):
                report.write(f"\t{i}\t{point.x}\t{point.y}\t{point.z}\n")
            report.write(f"\tend\t{self.endPoint.x}\t{self.endPoint.y}\t{self.endPoint.h}\n")
            report.write(f"Relative distance error: {self.relativeError}\n")
            report.write(f"Errors:\n\tID\tText\n")
            for i, error in enumerate(self.errors):
                report.write(f"\t{i}\t{error}\n")

    def draw_cource(self):
        plt.figure("Theodolite course")
        plt.text(self.startPoint.y, self.startPoint.x,  f"start, h: {self.startPoint.h}")
        plt.text(self.endPoint.y, self.endPoint.x,  f"end, h: {self.endPoint.h}")
        for i, point in enumerate(self.points):
            plt.text(point.y, point.x, f"{i}, h: {point.z}")

        plt.plot([self.startPoint.y] + [point.y for point in self.points] +  [self.endPoint.y], [self.startPoint.x] + [point.x for point in self.points] + [self.endPoint.x], marker=".")
        plt.xlabel("y")
        plt.ylabel("x")
        plt.title("Theodolite course")
        plt.show()