class ImageCoordinate(object):
    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    @property
    def processed(self):
        return self._processed

    @processed.setter
    def processed(self, value):
        self._processed = value

    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

        self._processed = False

        self._last_transformation = None
        self._screen_coordinates = None

    def transform(self, matrix, tid=None):
        if tid is not None and self._last_transformation == tid:
            return

        self._last_transformation = tid

        point = (self.x, self.y, self.z,)
        self._x = point[0] * matrix.get_value(0, 0) + \
            point[1] * matrix.get_value(1, 0) + \
            point[2] * matrix.get_value(2, 0) + \
            matrix.get_value(3, 0)
        self._y = point[0] * matrix.get_value(0, 1) + \
            point[1] * matrix.get_value(1, 1) + \
            point[2] * matrix.get_value(2, 1) + \
            matrix.get_value(3, 1)
        self._z = point[0] * matrix.get_value(0, 2) + \
            point[1] * matrix.get_value(1, 2) + \
            point[2] * matrix.get_value(2, 2) + \
            matrix.get_value(3, 2)

        self._screen_coordinates = None

    def set_screen_coordinates(self, x, y):
        self._screen_coordinates = (x, y,)

    def get_screen_coordinates(self):
        return self._screen_coordinates

    def __repr__(self):
        return "Coordinate: x {:.2f} y {:.2f} z {:.2f}".format(self.x, self.y, self.z)
