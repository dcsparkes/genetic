"""
For the moment I am depositing the vector code here.  It seems that it might just be easier to think in terms of
complex numbers and not use this incomplete or untested code.

Whether or not I use a Vector class I'm collecting all of the vector helper functions here,
"""
import math


class Vector():
    """
    Class that encapsulates Caretesian coordinates as a vector
    """

    def __init__(self, coefficients=None):
        if type(coefficients) is complex:
            self.coefficients = (coefficients.real, coefficients.imag)
        else:
            self.coefficients = tuple(coefficients)

    @classmethod
    def unit(cls, direction):
        return cls(coefficients=unitVector(direction))

    def __iter__(self):
        for c in self.coefficients:
            yield c

    def __len__(self):
        return len(self.coefficients)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.coefficients)

    def __str__(self):
        return "{}".format(self.coefficients)

    def __add__(self, other):
        return Vector([a + b for a, b in zip(self.coefficients, other)])

    __radd__ = __add__

    def __iadd__(self, other):
        self.coefficients = tuple([a + b for a, b in zip(self.coefficients, other)])
        return self

    def __sub__(self, other):
        return Vector([a - b for a, b in zip(self.coefficients, other)])

    def __isub__(self, other):
        self.coefficients = tuple([a - b for a, b in zip(self.coefficients, other)])
        return self

    def __rsub__(self, other):
        return Vector([b - a for a, b in zip(self.coefficients, other)])

    def __mul__(self, other):
        if type(other) is float or type(other) is int:
            return Vector([other * c for c in self.coefficients])
        else:
            return dotProduct(self, other)

    __rmul__ = __mul__

    def __neg__(self, other):
        return Vector([-c for c in self.coefficients])

    def magnitude(self):
        """
        :return: Calculated magnitude of vector using Pythagorus.
        """
        return math.sqrt(sum([c ** 2 for c in self.coefficients]))

    def unitVector(self):
        """
        :return: Vector instance of the unit vector in the direction of self.
        """
        return Vector.unit(self)


class Vector2D(Vector):
    def polar(self):
        """
        :return: vector in polar form
        """
        return cmath.polar(complex(*self.coefficients[:2]))


def unitVector(direction):
    """
    Calculate the unit vector: 0 = increasing x (or real), 90 = increasing y (or complex)
    Questionable whether it should operate in degrees or radians or some hybrid (e.g. ints=degrees, floats=radians)
    For now everything is in degrees.
    Direction can take a number of forms:
        Numbers (int, float) = angle
        tuple, list, (iterable) = vector
        Complex = 2D vector: treat accordingly
    :param angle:
    :return: tuple of coefficients (float)
    """
    if type(direction) is tuple or type(direction) is list:
        length = _vectorLength(direction)
        return [c / length for c in direction]
    elif type(direction) is int or type(direction) is float:  # Number is angle in degrees
        rad = math.radians(direction)
        return (math.cos(rad), math.sin(rad))
    elif type(direction) is complex:
        return unitVector((direction.real, direction.imag))
    # Check iterable?: https://stackoverflow.com/questions/1952464/in-python-how-do-i-determine-if-an-object-is-iterable
    return None


def dotProduct(v1, v2):
    """
    Dot product of two vectors is the sum of the product of the corresponding cartesian coordinates
    :param v1:
    :param v2:
    :return:
    """
    return sum([a * b for a, b in zip(v1, v2)])


def _vectorAngle(v1, v2):
    """
    Calculate angle between two vectors.
    :param v1:
    :param v2:
    :return:
    """
    return math.degrees(math.acos(dotProduct(v1, v2) / (_vectorLength(v1) * _vectorLength(v2))))


def _vectorLength(v):
    """
    Calculate magnitude of vector using Pythagorus.
    :param v: vector (iterable)
    :return:
    """
    if type(v) is complex:
        return _vectorLength((v.real, v.imag))
    return math.sqrt(sum([i ** 2 for i in v]))


def radialIntersection(dims, angle):
    """
    :param dims: image dimensions as tuple
    :param angle: 0 = +ve x-axis. 90 = +ve y-axis
    :return: intersection point with a frame of a line drawn from the centre point at the given angle.
    """
    theta = angle % 360
    xdim, ydim = dims
    xmax = xdim - 1
    ymax = ydim - 1
    x = None
    y = None
    if 0 < theta < 180:  # angle uppish, intersection top half
        rads = math.radians(theta - 90)
        x = round((xmax - math.tan(rads) * ymax) / 2)
        if 0 <= x <= xmax:
            return (x, ymax)
    elif 180 < theta:  # angle downish, origin bottom half
        rads = math.radians(theta - 270)
        x = round((xmax + math.tan(rads) * ymax) / 2)
        if 0 <= x <= xmax:
            return (x, 0)

    if 90 < theta < 270:  # angle leftish, origin right half
        rads = math.radians(theta - 180)
        y = round((ymax - math.tan(rads) * xmax) / 2)
        if 0 <= y <= ymax:
            return (0, y)
    elif 270 < theta or theta < 90:  # angle rightish, origin left half
        rads = math.radians((theta + 90) % 360 - 90)
        y = round((ymax + math.tan(rads) * xmax) / 2)
        if 0 <= y <= ymax:
            return (xmax, y)
