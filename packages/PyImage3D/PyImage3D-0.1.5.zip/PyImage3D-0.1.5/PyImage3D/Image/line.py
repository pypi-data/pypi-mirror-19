from PyImage3D.Image import coordinate, vector


class ImageLine(vector.ImageVector):
    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = value

    def __init__(self, x, y, z, direction):
        super(ImageLine, self).__init__(x, y, z)

        self._direction = direction

    def calculate_point(self, t):
        return coordinate.ImageCoordinate(
            self.x + t * self._direction.x,
            self.y + t * self._direction.y,
            self.z + t * self._direction.z,
        )

    def __repr__(self):
        return super(ImageLine, self).__repr__() + ' -> ' + self._direction.__repr__()
