import numpy as np
from pydesy.basic import Point
from pydesy.gmath import *

class Ellipsoid:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.e2 = (sqrt(self.a ** 2 - self.b ** 2) / self.a) ** 2

    def geodetic_to_rectangle(self, B, L, H):
        N = self.a / sqrt(1 - self.e2 * sin(B) ** 2)
        return {
            "X": (N + H) * cos(B) * cos(L),
            "Y": (N + H) * cos(B) * sin(L),
            "Z": ((1 - self.e2) * N + H) * sin(B)
        }

    def Bessel_inverse_geo_task(self, B1, L1, B2, L2):
        w1, w2 = sqrt(1 - self.e2 * sin(B1) ** 2), sqrt(1 - self.e2 * sin(B2) ** 2) #БВ
        sinu1, sinu2 = sin(B1) * sqrt(1 - self.e2) / w1, sin(B2) * sqrt(1 - self.e2) / w2 #БВ
        cosu1, cosu2 = cos(B1) / w1, cos(B2) / w2 #БВ
        l = L2 - L1 #Градусы
        a1, a2 = sinu1 * sinu2, cosu1 * cosu2 #БВ
        b1, b2 = cosu1 * sinu2, sinu1 * cosu2 #БВ

        A12 = 0
        preSigma = 0
        sigma, eps = 0, 0
        while abs(eps) > 1 / 10000 or eps != 0:
            lam = l + sigma
            p = cosu2 * sin(lam) #БВ
            q = B1 - B2 * cos(lam) #Градусы
            A12 = abs(atan(p / q)) #Градусы

            if p > 0 and q < 0: A12 = 180 - A12
            elif p < 0 and q < 0: A12 = 180 + A12
            elif p < 0 and q > 0: A12 = 360 - A12
            elif p == 0:
                if q > 0: A12 = 90
                else: A12 = 270
            elif q == 0:
                if p > 0: A12 = 0
                else: A12 = 180

            sind, cosd = p * sin(A12) + q * cos(A12), a1 + a2 * cos(lam)
            d = abs(atan(sind / cosd)) #Degrees

            if cosd < 0:
                d = 180 - d

            sinA0 = cosu1 * sin(A12)
            cos2A0 = 1 - sinA0 ** 2
            x = 2 * a1 - cos2A0 * cosd
            a = (e2 / 2 + e2 ** 2 / 8 + e2 ** 3 / 16) - (e2 ** 2 / 16 + e2 ** 3 / 16) * cos2A0 + 3 * e2 ** 3 / 128 * cos2A0 ** 2
            b = e2 ** 2  / 16 + e2 ** 3 / 16 - e2 ** 3 / 32 * cos2A0
            sigma = deg((a * rad(d) - b * x * sind) * sinA0)
            eps = sigma - preSigma
            preSigma = sigma

        print(A12)
        
class Helmert:
    def __init__(self, points1 : list, points2 : list):
        self.points1 = points1
        self.points2 = points2
        
    def calculate_params(self) -> dict:
        assert len(self.points1) == len(self.points2) and len(self.points1) >= 3 and len(self.points2) >= 3
        matrixL = list()
        for i in range(len(self.points1)):
            matrixL.append([self.points2[i].x - self.points1[i].x])
            matrixL.append([self.points2[i].y - self.points1[i].y])
            matrixL.append([self.points2[i].z - self.points1[i].z])
        self.matrixL = np.array(matrixL)

        matrixA = list()
        for i in range(len(self.points1)):
            matrixA.append([1, 0, 0, self.points2[i].x, 0, self.points2[i].z, -self.points2[i].y])
            matrixA.append([0, 1, 0, self.points2[i].y, -self.points2[i].z, 0, self.points2[i].x])
            matrixA.append([0, 0, 1, self.points2[i].z, self.points2[i].y, -self.points2[i].x, 0])
        self.matrixA = np.array(matrixA)
        self.matrixX = -np.linalg.inv(np.transpose(self.matrixA) @ self.matrixA) @ np.transpose(self.matrixA) @ self.matrixL

        return {
            "x": self.matrixX[0,0],
            "y": self.matrixX[1,0],
            "z": self.matrixX[2,0],
            "m": 1 + self.matrixX[3,0],
            "ex\"": deg(self.matrixX[4,0]) * 3600,
            "ey\"": deg(self.matrixX[5,0]) * 3600,
            "ez\"": deg(self.matrixX[6,0]) * 3600
        }

    def calculate_accuracy_score(self) -> dict:
        self.matrixV = self.matrixA @ self.matrixX + self.matrixL
        sigma0 = sqrt(np.sum(np.power(self.matrixV, 2)) / (3 * len(self.points1) - 7))
        self.matrixQ = np.linalg.inv(np.transpose(self.matrixA) @ self.matrixA)

        return {
            "σ0": sigma0,
            "σx" : sigma0 * sqrt(self.matrixQ[0, 0]),
            "σy" : sigma0 * sqrt(self.matrixQ[1, 1]),
            "σz" : sigma0 * sqrt(self.matrixQ[2, 2]),
            "σm" : sigma0 * sqrt(self.matrixQ[3, 3]),
            "σex" : deg(sigma0 * sqrt(self.matrixQ[4, 4])) * 3600,
            "σey" : deg(sigma0 * sqrt(self.matrixQ[5, 5])) * 3600,
            "σez" : deg(sigma0 * sqrt(self.matrixQ[6, 6])) * 3600
        }

    def calculate_divergences(self) -> dict:
        divX, divY, divZ = list(), list(), list()

        for i in range(len(self.points1)):
            matrixB = np.array([
                [1, -self.matrixX[6, 0], self.matrixX[5, 0]],
                [self.matrixX[6, 0], 1, -self.matrixX[4, 0]],
                [-self.matrixX[5, 0], self.matrixX[4, 0], 1]
            ])

            move = Point(self.matrixX[0, 0], self.matrixX[1, 0], self.matrixX[2, 0]).getArrayV()
            controlPoint = (1 + self.matrixX[3, 0]) * matrixB @ self.points2[i].getArrayV() + move

            divX.append([controlPoint[0, 0] - self.points1[i].x])
            divY.append([controlPoint[1, 0] - self.points1[i].y])
            divZ.append([controlPoint[2, 0] - self.points1[i].z])

        return {
            "dx" : divX,
            "dy" : divY,
            "dz" : divZ
        }