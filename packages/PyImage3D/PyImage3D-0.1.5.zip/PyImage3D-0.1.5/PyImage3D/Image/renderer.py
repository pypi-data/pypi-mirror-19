import abc


class ImageRenderer(object):
    __metaclass__ = abc.ABCMeta

    SHADE_NO = 0
    SHADE_FLAT = 1
    SHADE_GOURAUD = 2
    SHADE_PHONG = 3

    def __init__(self):
        self._polygons = []
        self._lights = []
        self._points = []

        self._driver = None
        self._size = (0, 0,)
        self._color = None
        self._shading = self.SHADE_NO

    @abc.abstractmethod
    def _calculate_screen_coordinates(self, point):
        return

    @abc.abstractmethod
    def _sort_polygons(self, point):
        return

    def _fetch_polygons(self, obj):
        polygons = obj.get_polygons()
        self._polygons += polygons

        for polygon in polygons:
            points = polygon.get_points()
            for point in points:
                if not point.processed:
                    point.processed = True
                    self._points.append(point)

    def add_objects(self, *objects):
        for obj in objects:
            self._fetch_polygons(obj)

    def add_lights(self, *lights):
        self._lights += lights

    def set_size(self, x, y):
        self._size = (x / 2, y / 2,)

    def set_color(self, color):
        self._color = color

    def set_shading(self, shading):
        self._shading = shading

    def set_driver(self, driver):
        self._driver = driver

        self.set_shading(min(self._shading, max(driver.get_supported_shading())))

    def get_polygon_count(self):
        return len(self._polygons)

    def get_light_count(self):
        return len(self._lights)

    def _calculate_polygon_colors(self):
        for polygon in self._polygons:
            polygon.calculate_color(self._lights)

    def _calculate_point_colors(self):
        for polygon in self._polygons:
            normal = polygon.get_normal()
            color = polygon.get_color()

            points = polygon.get_points()
            for point in points:
                point.add_vector(normal)
                point.add_color(color)

        for point in self._points:
            point.calculate_color(self._lights)

    def _shade(self):
        if self._shading == self.SHADE_FLAT:
            self._calculate_polygon_colors()
        elif self._shading == self.SHADE_GOURAUD:
            self._calculate_point_colors()
        elif self._shading != self.SHADE_NO:
            raise ValueError("Shading not supported")

        for polygon in self._polygons:
            self._driver.draw_polygon(polygon)

    def render(self, filename):
        if self._driver is None:
            return

        for point in self._points:
            self._calculate_screen_coordinates(point)

        self._sort_polygons()

        self._driver.create_image(self._size[0] * 2, self._size[1] * 2)
        self._driver.set_color(self._color)

        self._shade()

        self._driver.save(filename)

    def destroy(self):
        if self._driver is not None:
            return self._driver.destroy()
