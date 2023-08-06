from PyImage3D import POLY_WIRE_NO
from PyImage3D.Image import helper, vector


class ImagePaintablePolygon(object):
    @property
    def wireframe(self):
        return self._wireframe

    @wireframe.setter
    def wireframe(self, value):
        self._wireframe = value

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value

    def __init__(self, *points):
        self._points = []
        self._options = []

        self._normal = None
        self._position = None

        self._color = None
        self._color_calculated = None

        self._visible = True
        self._wireframe = POLY_WIRE_NO

        self._bounding_rect = [None, None, None, None, None, None]

        if points:
            for point in points:
                self.add_point(point)

    def calculate_color(self, lights):
        for light in lights:
            self._color = light.get_color(self)

        self._color.calculate_color()

    def get_color(self):
        return self._color

    def _calculate_normal(self):
        if len(self._points) < 3:
            self._normal = vector.ImageVector(0, 0, 0)
            return

        a1 = self._points[0].x - self._points[1].x
        a2 = self._points[0].y - self._points[1].y
        a3 = self._points[0].z - self._points[1].z
        b1 = self._points[2].x - self._points[1].x
        b2 = self._points[2].y - self._points[1].y
        b3 = self._points[2].z - self._points[1].z

        self._normal = vector.ImageVector(
            a2 * b3 - a3 * b2,
            a3 * b1 - a1 * b3,
            a1 * b2 - a2 * b1
        )

        if self._normal.z <= 0:
            self.visible = False

    def get_normal(self):
        if self._normal is None:
            self._calculate_normal()

        return self._normal

    def _calculate_position(self):
        position = [0, 0, 0]
        for point in self._points:
            position[0] += point.x / len(self._points)
            position[1] += point.y / len(self._points)
            position[2] += point.z / len(self._points)

        self._position = vector.ImageVector(*position)

    def get_position(self):
        if self._position is None:
            self._calculate_position()

    def get_polygon_count(self):
        return 1

    def set_color(self, color):
        self._color = color

    def set_option(self, option, value):
        self._options[option] = value

        for point in self._points:
            point.set_option(option, value)

    def add_point(self, point):
        self._points.append(point)

        if not self._bounding_rect[0] or point.x < self._bounding_rect[0]:
            self._bounding_rect[0] = point.x
        if not self._bounding_rect[1] or point.y < self._bounding_rect[1]:
            self._bounding_rect[1] = point.y
        if not self._bounding_rect[2] or point.z < self._bounding_rect[2]:
            self._bounding_rect[2] = point.z

        if not self._bounding_rect[3] or point.x < self._bounding_rect[3]:
            self._bounding_rect[3] = point.x
        if not self._bounding_rect[4] or point.y < self._bounding_rect[4]:
            self._bounding_rect[4] = point.y
        if not self._bounding_rect[5] or point.z < self._bounding_rect[5]:
            self._bounding_rect[5] = point.z

    def get_points(self):
        return list(self._points)

    def _calculate_bounds(self):
        self._bounding_rect = [None, None, None, None, None, None]

        for point in self._points:
            if not self._bounding_rect[0] or point.x < self._bounding_rect[0]:
                self._bounding_rect[0] = point.x
            if not self._bounding_rect[1] or point.y < self._bounding_rect[1]:
                self._bounding_rect[1] = point.y
            if not self._bounding_rect[2] or point.z < self._bounding_rect[2]:
                self._bounding_rect[2] = point.z

            if not self._bounding_rect[3] or point.x < self._bounding_rect[3]:
                self._bounding_rect[3] = point.x
            if not self._bounding_rect[4] or point.y < self._bounding_rect[4]:
                self._bounding_rect[4] = point.y
            if not self._bounding_rect[5] or point.z < self._bounding_rect[5]:
                self._bounding_rect[5] = point.z

    def transform(self, matrix, tid=None):
        if tid is None:
            tid = helper.unique_id()

        for point in self._points:
            point.transform(matrix, tid)

    def get_mid_z(self):
        if self._points:
            z = 0
            for point in self._points:
                z += point.z

            return z / len(self._points)

    def get_max_z(self):
        if self._points:
            z = self._points[0].z
            for point in self._points:
                z = max(z, point.z)

            return z

    def distance(self, line):
        normal = self.get_normal()

        A = normal.x
        B = normal.y
        C = normal.z
        D = -(
            A * self._points[0].x +
            B * self._points[0].y +
            C * self._points[0].z
        )

        direction = line.direction
        denominator = -(
            A * line.x +
            B * line.y +
            C * line.z +
            D
        )
        numerator = (
            A * direction.x +
            B * direction.y +
            C * direction.z
        )

        if not denominator or not numerator:
            return

        t = denominator / numerator
        if t <= 0:
            return

        cut_point = line.calculate_point(t)
        if (cut_point.x < self._bounding_rect[0] or
                cut_point.y < self._bounding_rect[1] or
                cut_point.z < self._bounding_rect[2] or
                cut_point.x > self._bounding_rect[3] or
                cut_point.y > self._bounding_rect[4] or
                cut_point.z > self._bounding_rect[5]):
            return

        last_scalar = 0
        np = 0
        for point in self._points:
            next = self._points[(np + 1) % len(self._points)]
            edge = vector.ImageVector(
                next.x - point.x,
                next.y - point.y,
                next.z - point.z
            )
            v = vector.ImageVector(
                cut_point.x - point.x,
                cut_point.y - point.y,
                cut_point.z - point.z
            )

            scalar = edge.cross_product(v).scalar(normal)
            if scalar * last_scalar >= 0:
                last_scalar = scalar
            else:
                return

            np += 1

    def __repr__(self):
        repr_str = "Polygon: points {:d}\n".format(len(self._points))
        for point in self._points:
            repr_str += "\t" + str(point) + "\n"

        return repr_str