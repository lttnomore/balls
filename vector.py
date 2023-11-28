import math
import random


class Vector:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Vector(self.x + other.x, self.y + other.y)
        return Vector(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return Vector(self.x - other.x, self.y - other.y)
        return Vector(self.x - other, self.y - other)

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return Vector(self.x * other.x, self.y * other.y)
        return Vector(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            return Vector(self.x / other.x, self.y / other.y)
        return Vector(self.x / other, self.y / other)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y
        return self.x == other and self.y == other

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def make_int_tuple(self):
        return int(self.x), int(self.y)

    def set(self, vec):
        self.x = vec.x
        self.y = vec.y

@staticmethod
def dot(vec1, vec2):
    return vec1.x * vec2.x + vec1.y * vec2.y

@staticmethod
def angle_between(vec1, vec2):
    return math.acos(dot(vec1, vec2))

@staticmethod
def length_sqr(vec):
    return vec.x ** 2 + vec.y ** 2

@staticmethod
def dist_sqr(vec1, vec2):
    return length_sqr(vec1 - vec2)

@staticmethod
def length(vec):
    return math.sqrt(length_sqr(vec))

@staticmethod
def dist(vec1, vec2):
    return math.sqrt(length_sqr(vec1 - vec2))

@staticmethod
def normalize(vec):
    leng = length(vec)
    if leng < 0.00001:
        return Vector(0, 1)
    return Vector(vec.x / leng, vec.y / leng)

@staticmethod
def reflect(incident, normal):
    return incident - dot(normal, incident) * 2.0 * normal

@staticmethod
def right(vec):
    return Vector(-vec.y, vec.x)

@staticmethod
def left(vec):
    return -right(vec)

@staticmethod
def random_vector():
    return Vector(abs(random.random()) * 760.0 + 100.0, abs(random.random()) * 520.0 + 100.0)

@staticmethod
def random_direction():
    return normalize(random_vector())

@staticmethod
def copy(vec):
    return Vector(vec.x, vec.y)

