import math

from PyImage3D.Image import coordinate


class ImageVector(coordinate.ImageCoordinate):
    @property
    def length(self):
        if self._length is None:
            self._length = math.sqrt(math.pow(self._x, 2) + math.pow(self._y, 2) + math.pow(self._z, 2))

        return self._length

    def __init__(self, x, y, z):
        super(ImageVector, self).__init__(x, y, z)

        self._length = None

    def get_angle(self, vector):
        p_length = vector.length * self.length
        if p_length < 0.0001:
            return 1

        return abs(math.acos(self.scalar(vector) / p_length) / math.pi - .5) * 2

    def get_side(self, vector):
        return self.scalar(vector)

    def unify(self):
        if self.length == 0:
            return None
        if self.length == 1:
            return self

        new_v = ImageVector(self._x / self.length, self._y / self.length, self._z / self.length)
        new_v._length = 1

        return new_v

    def add(self, vector):
        return ImageVector(self.x + vector.x, self.y + vector.y, self.z + vector.z)

    def sub(self, vector):
        return ImageVector(self.x - vector.x, self.y - vector.y, self.z - vector.z)

    def multiply(self, scalar):
        return ImageVector(self.x * scalar, self.y * scalar, self.z * scalar)

    def scalar(self, vector):
        return self.x * vector.x + self.y * vector.y + self.z * vector.z

    def cross_product(self, vector):
        return ImageVector(self.y * vector.z - self.z * vector.y,
                           self.z * vector.x - self.x * vector.z,
                           self.x * vector.y - self.y * vector.x)
