import inspect

import sys

from array import append
from array import extend
from array import indexByValue
from array import pop
from comparison import equalTo
from comparison import greaterThan
from comparison import greaterThanOrEqualTo
from comparison import ifCondition
from comparison import inRange
from comparison import lessThan
from comparison import lessThanOrEqualTo
from comparison import notEqualTo
from constants import boolean
from constants import dict
from constants import halfPi
from constants import integer
from constants import orderedDict
from constants import pi
from constants import scalar
from conversion import toArray
from dict import add
from dict import get
from dict import remove
from directories import copyFiles
from directories import filesInDirectories
from directories import rename
from directories import subDirectories
from math.basic import add
from math.basic import absolute
from math.basic import divide
from math.basic import floor
from math.basic import invert
from math.basic import modulo
from math.basic import multiply
from math.basic import power
from math.basic import squareRoot
from math.basic import subtract
from math.trigonometry import arccos
from math.trigonometry import arcsin
from math.trigonometry import arctan
from math.trigonometry import sin
from math.trigonometry import cos
from math.trigonometry import tan
from string import search
from string import split
from string import string
from string import subString


def getNode(name):
    """Helper method for retrieving a node by string
    :param name: str, the name of the module
    :return:
    """
    return getattr(sys.modules[__name__], name).getNode()
