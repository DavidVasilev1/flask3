from math import sqrt, floor, exp
def calcPoints(Ux, Uy, x, y):
    distance = sqrt((x-Ux)**2 + (y-Uy)**2)
    points = int(floor(5314.0934613321*exp(-0.002*distance)-314.093461332))
    if points >= 0:
        return points
    return 0

print(calcPoints(0,0,1000,1000))