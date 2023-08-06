from PyImage3D.Image import point
from PyImage3D.Image.Paintable import object, polygon


class ImagePaintableObjectZCube(object.ImagePaintableObject):
    def __init__(self, x=0, y=0, z=0):
        super(ImagePaintableObjectZCube, self).__init__()

        self._points = []

        self._points.append(point.ImagePoint(0, 0, 0))
        self._points.append(point.ImagePoint(0, 0, z))

        self._points.append(point.ImagePoint(0, y, 0))
        self._points.append(point.ImagePoint(0, y, z))

        self._points.append(point.ImagePoint(x, 0, 0))
        self._points.append(point.ImagePoint(x, 0, z))

        self._points.append(point.ImagePoint(x, y, 0))
        self._points.append(point.ImagePoint(x, y, z))

        # Upper and lower surfaces
        self._add_polygon(polygon.ImagePaintablePolygon(self._points[2], self._points[3], self._points[7], self._points[6]))
        self._add_polygon(polygon.ImagePaintablePolygon(self._points[1], self._points[0], self._points[4], self._points[5]))

        # Left and right surfaces
        self._add_polygon(polygon.ImagePaintablePolygon(self._points[2], self._points[0], self._points[1], self._points[3]))
        self._add_polygon(polygon.ImagePaintablePolygon(self._points[7], self._points[5], self._points[4], self._points[6]))

        # Back and front surfaces
        self._add_polygon(polygon.ImagePaintablePolygon(self._points[1], self._points[5], self._points[7], self._points[3]))
        self._add_polygon(polygon.ImagePaintablePolygon(self._points[0], self._points[2], self._points[6], self._points[4]))

    def get_point(self, index):
        if index < len(self._points):
            return self._points[index]
