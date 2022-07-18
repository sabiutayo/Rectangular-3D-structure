IN = [
    [0, 1, 2, 3],
    [0, 1, 2, 3],
    [0, 1, 2, 3]
]
dataEnteringNode = IN

nFlor = len(IN[0]) * len(IN[1])
nLine = len(IN[0])
nColumn = len(IN[1])
nLevel = len(IN[2])
nStructure = len(IN[0]) * len(IN[1]) * len(IN[2])

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


def generate_points():
    x = []
    y = []
    z = []
    point_list = []
    # Generate X coords
    for i in range(nColumn * nLevel):
        for j in IN[0]:
            x.append(j)
    # Generate Y coords
    for k in range(nLevel):
        for i in IN[1]:
            for j in range(nLine):
                y.append(i)
    # Generate Z coords
    for k in IN[2]:
        for j in range(nFlor):
            z.append(k)
    # Generate points
    for i in range(0, nStructure):
        point_list.append([x[i], y[i], z[i]])
    return point_list


points = generate_points()


# Generate vertical surfaces
def generete_front_surfaces():
    # Front surfaces
    front_surfaces = []
    skip_from = nLine - 1
    flor_increment = 1
    for i, val in enumerate(points[0:nStructure - nFlor]):
        if i >= skip_from:
            if i == nFlor * flor_increment - 1:
                skip_from = i + nLine
                flor_increment += 1
            continue
        if i < skip_from:
            front_surfaces.append(
                # Surface.ByPerimeterPoints(
                [
                    points[i],
                    points[i + 1],
                    points[i + nFlor + 1],
                    points[i + nFlor]
                ]
                # )
            )

    return front_surfaces


def generate_right_surfaces():
    return


def generate_back_surfaces():
    return


def generate_left_surfaces():
    return


def generate_vertical_surfaces():
    # Generate vertical surfaces
    surfaces = [
        generete_front_surfaces(),
        generate_right_surfaces(),
        generate_back_surfaces(),
        generate_left_surfaces()
    ]
    return surfaces


walls = generate_vertical_surfaces()

# Assign your output to the OUT variable.
OUT = [points, walls]
