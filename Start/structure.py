# Load the Python Standard and DesignScript Libraries
import sys
import clr

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# The inputs to this node will be stored as a list in the IN variables.
IN = [
    [0, 1, 2, 3],
    [0, 1, 2, 3],
    [0, 1, 2, 3],
]
dataEnteringNode = IN
xCoords = []
yCoords = []
zCoords = []
points = []
# Generate X coords
for i in range(len(IN[1] * len(IN[2]))):
    for j in IN[0]:
        xCoords.append(j)
# Generate Y coords
for k in range(len(IN[2])):
    for i in IN[1]:
        for j in range(len(IN[0])):
            yCoords.append(i)
# Generate Z coords
for k in IN[2]:
    for j in range(len(IN[0]) * len(IN[1])):
        zCoords.append(k)

# Generate points
for i in range(0, (len(IN[0]) * len(IN[1]) * len(IN[2]))):
    points.append(Point.ByCoordinates(xCoords[i], yCoords[i], zCoords[i]))

# Start points
startPoints = []

# X direction starting points
startStepX = len(IN[0])
startCounterX = 1
for i, val in enumerate(points[0:(len(points) - 1)]):
    if startCounterX == startStepX:
        startCounterX = 1
        continue
    startPoints.append(val)
    startCounterX += 1
# Y direction starting points
startStepY = len(IN[0]) * len(IN[1]) - len(IN[0])
finalStepY = len(IN[0]) * len(IN[1])
lastPoints = len(points) - len(IN[0])
startCounterY = 1
for i, val in enumerate(points[0:lastPoints]):
    if startStepY < startCounterY <= finalStepY:
        startCounterY += 1
        if startCounterY > finalStepY:
            startCounterY = 1
        continue
    startPoints.append(val)
    startCounterY += 1
# Z direction starting points
lastPointsZ = len(IN[0]) * len(IN[1]) * len(IN[2]) - len(IN[0]) * len(IN[1])
for i, val in enumerate(points[0:lastPointsZ]):
    startPoints.append(val)

# End points
endPoints = []

# X direction ending points
endStepX = len(IN[0])
endCounterX = 1
for i, val in enumerate(points[1:len(points)]):
    if endCounterX == endStepX:
        endCounterX = 1
        continue
    endPoints.append(val)
    endCounterX += 1
# Y direction ending points
endStepY = len(IN[0]) * len(IN[1]) - len(IN[0])
finalStepY = len(IN[0]) * len(IN[1])
firstPoints = len(IN[0])
endCounterY = 1
for i, val in enumerate(points[firstPoints:len(points)]):
    if startStepY < endCounterY <= finalStepY:
        endCounterY += 1
        if endCounterY > finalStepY:
            endCounterY = 1
        continue
    endPoints.append(val)
    endCounterY += 1
# Z direction ending points
firstPointsZ = len(IN[0]) * len(IN[1])
for i, val in enumerate(points[firstPointsZ:len(points)]):
    endPoints.append(val)

# Generate lines from points
lines = []

s = 0
e = 0
for i in range(0, len(startPoints)):
    lines.append(Line.ByStartPointEndPoint(startPoints[s], endPoints[e]))
    s += 1
    e += 1

# Generate horizontal surfaces
surfacesH = []
endLine = len(IN[0])
startColumn = len(IN[0]) * len(IN[1]) - len(IN[0])
endColumn = len(IN[0]) * len(IN[1])
endList = len(points) - len(IN[0]) - 1
lineCounter = 0
columnCounter = 0

for i, p in enumerate(points[0:endList]):

    if lineCounter < endLine:
        if lineCounter != 0:
            lineCounter += 1
    if columnCounter < endColumn:
        if columnCounter != 0:
            columnCounter += 1
    if lineCounter == endLine:
        lineCounter = 0
    if columnCounter == endColumn:
        columnCounter = 0
    if startColumn  <= columnCounter <= endColumn:
        continue

    surfacesH.append(
        Surface.ByPerimeterPoints(
            [
                points[i],
                points[i + 1],
                points[i + len(IN[0]) + 1],
                points[i + len(IN[0])]
            ]
        )
    )
# Assign your output to the OUT variable.
OUT = [
    points,
    lines,
    surfacesH,
]
