# Load the Python Standard and DesignScript Libraries
import sys
import clr

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# The inputs to this node will be stored as a list in the IN variables.

dataEnteringNode = IN

nFlor = len(IN[0]) * len(IN[1])
nLine = len(IN[0])
nColumn = len(IN[1])
nLevel = len(IN[2])
nStructure = len(IN[0]) * len(IN[1]) * len(IN[2])


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
        point_list.append(Point.ByCoordinates(x[i], y[i], z[i]))
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
    start = generate_line_start_points()
    end = generate_line_end_points()
    k = 0
    for i in range(0, len(start)):
        line_list.append(Line.ByStartPointEndPoint(start[k], end[k]))
        k += 1

    beams = []
    central_x_beams = []
    central_y_beams = []
    edge_x_beams = []
    edge_y_beams = []
    columns = []
    edge_columns = []
    central_columns = []
    counter = 0
    x_beams = (nFlor - nLine) * nLevel
    y_beams = x_beams + (nFlor - nColumn) * nLevel
    counter_y = 0
    for i, val in enumerate(line_list):
        # x beams
        if i < x_beams:
            if 0 <= counter < nFlor - nLine:
                if 0 <= counter < nLine - 1 or nFlor - nLine - nLine < counter < nFlor - nLine:
                    edge_x_beams.append(val)
                else:
                    central_x_beams.append(val)
                if counter == nFlor - nLine - 1:
                    counter = 0
                else:
                    counter += 1
        # y beams
        if x_beams <= i < y_beams:
            if counter == 0 or counter == nLine - 1:
                edge_y_beams.append(val)
            else:
                central_y_beams.append(val)
            if counter == nLine - 1:
                counter = 0
            else:
                counter += 1

        # columns
        if y_beams <= i < len(line_list):
            if 0 <= counter <= nLine or nFlor - nLine - 1 <= counter < nFlor or 0 == counter_y or nLine - 1 == counter_y:
                edge_columns.append(val)
            else:
                central_columns.append(val)
            if counter == nFlor - 1:
                counter = 0
            else:
                counter += 1
            if counter_y == nLine-1:
                counter_y = 0
            else:
                counter_y += 1

    beams.append(edge_x_beams)
    beams.append(edge_y_beams)
    beams.append(central_x_beams)
    beams.append(central_y_beams)
    columns.append(edge_columns)
    columns.append(central_columns)

    return [columns, beams]


lines = generate_lines()


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
            Surface.ByPerimeterPoints(
                [
                    points[i],
                    points[i + 1],
                    points[i + nLine + 1],
                    points[i + nLine]
                ]
            )
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
                Surface.ByPerimeterPoints(
                    [
                        points[i],
                        points[i + 1],
                        points[i + nFlor + 1],
                        points[i + nFlor]
                    ]
                )
            )

    return front_surfaces


def generate_right_surfaces():
    right_surfaces = []
    skip = nFlor - 1
    for i in range(nLine - 1, nStructure - nFlor - nLine, nLine):
        if i == skip:
            skip += nFlor
            continue
        right_surfaces.append(
            Surface.ByPerimeterPoints(
                [points[i],
                 points[i + nLine],
                 points[i + nFlor + nLine],
                 points[i + nFlor]]
            ))
    return right_surfaces


def generate_back_surfaces():
    back_surfaces = []
    skip_end_flor = nFlor - 1
    skip = nFlor - nLine
    for i, val in enumerate(points[skip:nStructure]):
        if i < skip:
            continue
        if i >= skip and not i == skip_end_flor:
            back_surfaces.append(
                Surface.ByPerimeterPoints(
                    [points[i],
                     points[i + 1],
                     points[i + nFlor + 1],
                     points[i + nFlor]]
                ))

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
        left_surfaces.append(
            Surface.ByPerimeterPoints(
                [points[i],
                 points[i + nLine],
                 points[i + nFlor + nLine],
                 points[i + nFlor]]
            ))
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
OUT = [
    #points,
    lines,
    #slabs,
    #walls

]
