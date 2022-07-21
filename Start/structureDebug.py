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


def generate_line_start_points():
    # Start points
    start_points = []
    # X direction starting points
    start_counter_x = 1
    for i, val in enumerate(points[0:(len(points) - 1)]):
        if start_counter_x == nLine:
            start_counter_x = 1
            continue
        start_points.append(val)
        start_counter_x += 1
    # Y direction starting points
    start_step_y = nFlor - nLine
    last_points = len(points) - nLine
    start_counter_y = 1
    for i, val in enumerate(points[0:last_points]):
        if start_step_y < start_counter_y <= nFlor:
            start_counter_y += 1
            if start_counter_y > nFlor:
                start_counter_y = 1
            continue
        start_points.append(val)
        start_counter_y += 1
    # Z direction starting points
    last_points_z = nStructure - nFlor
    for i, val in enumerate(points[0:last_points_z]):
        start_points.append(val)
    return start_points


def generate_line_end_points():
    # End points
    end_points = []

    # X direction ending points
    end_counter_x = 1
    for i, val in enumerate(points[1:len(points)]):
        if end_counter_x == nLine:
            end_counter_x = 1
            continue
        end_points.append(val)
        end_counter_x += 1
    # Y direction ending points
    end_step_y = nFlor - nLine
    end_counter_y = 1
    for i, val in enumerate(points[nLine:len(points)]):
        if end_step_y < end_counter_y <= nFlor:
            end_counter_y += 1
            if end_counter_y > nFlor:
                end_counter_y = 1
            continue
        end_points.append(val)
        end_counter_y += 1
    # Z direction ending points
    for i, val in enumerate(points[nFlor:len(points)]):
        end_points.append(val)
    return end_points


def generate_lines():
    # Generate lines from points
    line_list = []

    columns = []
    edge_columns = []
    central_columns = []

    beams = []
    central_x_beams = []
    central_y_beams = []
    edge_x_beams = []
    edge_y_beams = []

    start = generate_line_start_points()
    end = generate_line_end_points()
    k = 0
    for i in range(0, len(start)):
        line_list.append([(start[k], end[k])])
        k += 1

    counter = 0
    x_beams = (nFlor - nLine) * nLevel
    y_beams = x_beams + (nFlor - nColumn) * nLevel
    for i, val in enumerate(line_list):
        # x beams
        if i < x_beams:
            if 0 <= counter < nFlor - nLine:
                if 0 <= counter < nLine - 1 or nFlor - nLine - nLine < counter < nFlor - nLine :
                    edge_x_beams.append(val)
                else:
                    central_x_beams.append(val)
                if counter == nFlor - nLine - 1:
                    counter = 0
                else:
                    counter += 1
        # y beams
        if x_beams <= i < y_beams:
            if counter == 0 or counter == nLine-1:
                edge_y_beams.append(val)
            else:
                central_y_beams.append(val)
            if counter == nLine-1:
                counter = 0
            else:
                counter += 1

        # columns
        if y_beams <= i < len(line_list):
            pass

    beams.append(edge_x_beams)
    beams.append(edge_y_beams)
    beams.append(central_x_beams)
    beams.append(central_y_beams)
    columns.append(central_columns)
    columns.append(edge_columns)

    return [columns, beams]


lines = generate_lines()

# Assign your output to the OUT variable.
OUT = [points, lines]
