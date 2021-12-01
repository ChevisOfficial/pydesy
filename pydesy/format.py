class TLE:
    def __init__(self, line1 : str, line2 : str):
        spline1 = line1.split()
        spline2 = line2.split()

        #Line 1
        self.satellite_number = int(spline1[1][:-1])
        self.classification = spline1[1][-1:]
        self.launch_year = int(spline1[2][:2])
        self.launch_number = int(spline1[2][2:5])
        self.launch_piece = spline1[2][-1:]
        self.epoch_year = int(spline1[3][:2])
        self.epoch = float(spline1[3][2:])
        self.first_derivative = float(("-0" if spline1[4][0] == "-" else "0") + spline1[4][1:])
        self.second_derivative = float(("-0." if spline1[5][0] == "-" else "0.") + spline1[5][1:].replace("-", "e-"))
        self.BSTAR = float(("-0." if spline1[6][0] == "-" else "0.") + spline1[6][1:].replace("-", "e-"))
        self.ephemeris_type = spline1[7]
        self.element_number = int(spline1[8][:-1])
        self.checksum1 = int(spline1[8][-1:])

        #Line 2
        self.inclination = float(spline2[2])
        self.right_ascension = float(spline2[3])
        self.eccentricity = float("0." + spline2[4])
        self.perigee = float(spline2[5])
        self.mean_anomaly = float(spline2[6])
        self.mean_motion = float(spline2[7][:-6])
        self.revolution_number = int(spline2[7][-6:-1])
        self.checksum2 = int(spline2[7][-1])

    def print(self):
        for var in list(vars(self)):
            if type(var) == int or float or str:
                print(f"{var.replace('_', ' ').title()} = {vars(self)[var]}")