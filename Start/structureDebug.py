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

# Generate horizontal surfaces
surfacesH = []
endLine = len(IN[0])
startColumn = len(IN[0]) * len(IN[1]) - len(IN[0])
endColumn = len(IN[0]) * len(IN[1])
endList = len(points) - len(IN[0]) - 1
lineCounter = 0
columnCounter = 0

for i, p in enumerate(points[0:endList]):
    lineCounter += 1
    columnCounter += 1
    if lineCounter >= endLine:
        lineCounter = 0
        continue

surfacesH.append(
    #        Surface.ByPerimeterPoints(
    [
        points[i],
        points[i + 1],
        points[i + len(IN[0]) + 1],
        points[i + len(IN[0])]
    ]
    #        )
)
# Assign your output to the OUT variable.
for i, val in enumerate(surfacesH, 0):
    print(val)

OUT = [points, surfacesH]
