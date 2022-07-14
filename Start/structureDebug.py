from itertools import islice

IN = [
    [0, 1, 2, 3],
    [0, 1, 2, 3],
    [0, 1, 2, 3]
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
    points.append([xCoords[i], yCoords[i], zCoords[i]])

# Generate vertical surfaces

surfacesV = []
nFlor = len(IN[0]) * len(IN[1])
nLine = len(IN[0])
nColumn = len(IN[1])
nLevel = len(IN[2])
nStructure = len(IN[0]) * len(IN[1]) * len(IN[2])

# Front surfaces
# Front surfaces
frontSurfaces = []
skipFrom = nLine - 1
skipFrom = nLine - 1
florIncrement = 1
for i, val in enumerate(points[0:nStructure - nFlor]):
    if i >= skipFrom:
        if i == nFlor * florIncrement - 1:
            skipFrom = i + nLine
            florIncrement += 1
        continue
    if i < skipFrom:
        frontSurfaces.append(
           # Surface.ByPerimeterPoints(
                [
                    points[i],
                    points[i + 1],
                    points[i + nFlor + 1],
                    points[i + nFlor]
                ]
           # )
        )

surfacesV.append(frontSurfaces)

# Right surfaces
rightSurfaces = []
skipFrom = nLine - 1
skipFrom = nLine - 1


surfacesV.append(rightSurfaces)

# Assign your output to the OUT variable.
for i, val in enumerate(surfacesV, 0):
    print(val)

OUT = [points, surfacesV]
