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


def generate_horizontal_surfaces():
    # Generate horizontal surfaces
    surfaces_h = []
    start_column = nFlor - nLine
    end_list = len(points) - nLine - 1
    line_counter = 0
    column_counter = 0

    for i, p in enumerate(points[0:end_list]):

        # skip left nodes
        if column_counter == nFlor - 1:
            line_counter = 0
            column_counter = 0
            continue

        if line_counter == nLine - 1:
            line_counter = 0
            column_counter += 1
            continue

        # skip top nodes 0 ÷ end_line-1
        if line_counter >= 0 and start_column <= column_counter < nFlor:
            line_counter += 1
            column_counter += 1
            continue

        if column_counter <= nFlor:
            if line_counter < nLine:
                line_counter += 1
            if column_counter < nFlor:
                column_counter += 1
            if line_counter == nLine:
                line_counter = 0
            if column_counter == nFlor:
                column_counter = 0

        surfaces_h.append(
            # Surface.ByPerimeterPoints(
                [
                    points[i],
                    points[i + 1],
                    points[i + nLine + 1],
                    points[i + nLine]
                ]
            # )
        )
    stories = []
    start = 0
    step = int(len(surfaces_h)/nLevel)
    end = step
    for x in range(0, nLevel):
        stories.append(surfaces_h[start:end])
        start += step
        end += step

    return stories


slabs = generate_horizontal_surfaces()


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
    right_surfaces = []
    skip = nFlor - 1
    for i in range(nLine - 1, nStructure - nFlor - nLine, nLine):
        if i == skip:
            skip += nFlor
            continue
        right_surfaces.append([points[i],
                               points[i + nLine],
                               points[i + nFlor + nLine],
                               points[i + nFlor]]
                              )
    return right_surfaces


def generate_back_surfaces():
    back_surfaces = []
    skip_end_flor = nFlor - 1
    skip = nFlor - nLine
    for i, val in enumerate(points[skip:nStructure]):
        if i < skip:
            continue
        if i >= skip and not i == skip_end_flor:
            back_surfaces.append([points[i],
                                  points[i + 1],
                                  points[i + nFlor + 1],
                                  points[i + nFlor]]
                                 )

        if i == skip_end_flor:
            skip_end_flor += nFlor
            skip += nFlor

    return back_surfaces


def generate_left_surfaces():
    left_surfaces = []
    skip = nFlor - nLine
    for i in range(0, nStructure - nFlor, nLine):
        if i == skip:
            skip += nFlor
            continue
        left_surfaces.append([points[i],
                              points[i + nLine],
                              points[i + nFlor + nLine],
                              points[i + nFlor]]
                             )
    return left_surfaces


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
