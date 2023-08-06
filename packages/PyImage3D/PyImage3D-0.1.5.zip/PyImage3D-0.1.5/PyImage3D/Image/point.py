from PyImage3D.Image import coordinate, color, vector


class ImagePoint(coordinate.ImageCoordinate):
    def __init__(self, x, y, z):
        super(ImagePoint, self).__init__(x, y, z)

        self._options = {}
        self._colors = []
        self._vectors = []

        self._normal = None
        self._color = None

    def set_option(self, option, value):
        self._options[option] = value

    def calculate_color(self, lights):
        if not lights:
            self._color = color.ImageColor(0, 0, 0, self.get_color().get_values()[3])

        for light in lights:
            self._color = light.get_color(self)

        if self._color:
            self._color.calculate_color()

    def add_vector(self, vector):
        self._vectors.append(vector)

    def _calculate_normal(self):
        self._normal = vector.ImageVector(0, 0, 0)
        for n_vector in self._vectors:
            self._normal = self._normal.add(n_vector)
        self._normal.unify()

    def get_normal(self):
        if not self._normal:
            self._calculate_normal()
        return self._normal

    def get_position(self):
        return vector.ImageVector(self.x, self.x, self.z)

    def add_color(self, color):
        self._colors.append(color)

    def _mix_colors(self):
        i = 0
        end_color = [0, 0, 0, 0]
        for c_color in self._colors:
            values = c_color.get_values()
            end_color[0] += values[0]
            end_color[1] += values[1]
            end_color[2] += values[2]
            end_color[3] += values[3]

            i += 1

        self._color = color.ImageColor(end_color[0] / i, end_color[1] / i, end_color[2] / i, end_color[3] / i)

    def get_color(self):
        if not self._color:
            self._mix_colors()
        return self._color

    def __repr__(self):
        return "Point: x {:.2f} y {:.2f} z {:.2f}".format(self.x, self.y, self.z)
