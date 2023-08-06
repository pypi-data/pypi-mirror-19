from PyImage3D.Image import helper


class Image3D(object):
    def __init__(self):
        self._objects = []
        self._lights = []

        self._renderer = None
        self._driver = None
        self._color = None

        self._option_set = []

        self._start = helper.to_timestamp()

    def create_object(self, ob_type, ob_params=()):
        obj = ob_type(*ob_params)
        self._objects.append(obj)

        return obj

    def create_light(self, ob_type, ob_params=()):
        obj = ob_type(*ob_params)
        self._lights.append(obj)

        return obj

    def create_matrix(self, ob_type, ob_params=()):
        return ob_type(*ob_params)

    def create_renderer(self, ob_type, ob_params=()):
        self._renderer = ob_type(*ob_params)

        return self._renderer

    def create_driver(self, ob_type, ob_params=()):
        self._driver = ob_type(*ob_params)

        return self._driver

    def set_color(self, color):
        self._color = color

    def set_option(self, option, value):
        self._option_set[option] = value

        for obj in self._objects:
            obj.set_option(option, value)

    def transform(self, matrix, tid=None):
        if tid is None:
            tid = helper.unique_id()

        for obj in self._objects:
            obj.transform(matrix, tid)

    def render(self, x, y, filename):
        self._renderer.set_size(x, y)
        self._renderer.set_color(self._color)
        self._renderer.add_objects(*self._objects)
        self._renderer.add_lights(*self._lights)
        self._renderer.set_driver(self._driver)

        return self._renderer.render(filename)
