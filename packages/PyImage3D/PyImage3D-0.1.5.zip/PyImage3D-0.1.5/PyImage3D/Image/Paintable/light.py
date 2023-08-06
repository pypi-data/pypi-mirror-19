import copy

from PyImage3D.Image import coordinate, vector


class ImagePaintableLight(coordinate.ImageCoordinate):
    def __init__(self, x, y, z):
        super(ImagePaintableLight, self).__init__(x, y, z)

        self._polygons = []

        self._color = None
        self._position = None

    def get_polygon_count(self):
        return len(self._polygons)

    def set_color(self, color):
        self._color = color

    def get_raw_color(self):
        return self._color

    def get_color(self, polygon):
        color = copy.copy(polygon.get_color())

        light = vector.ImageVector(self.x, self.y, self.z)
        light = light.sub(polygon.get_position())

        normal = polygon.get_normal()
        angle = normal.get_angle(light)

        color.add_light(self.get_raw_color(), angle)

        return color
