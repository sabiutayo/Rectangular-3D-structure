import sys
import clr

clr.AddReference(
    r"C:\Program Files\Autodesk\Autodesk Robot Structural Analysis Professional 2022\Exe\Interop.RobotOM.dll")

from RobotOM import RobotApplicationClass

app = RobotApplicationClass()