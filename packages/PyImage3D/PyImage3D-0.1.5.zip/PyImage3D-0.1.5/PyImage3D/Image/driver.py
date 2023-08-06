import abc
import io

from PyImage3D.Image import renderer


class ImageDriver(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._image = None

    @abc.abstractmethod
    def create_image(self, x, y):
        return

    @abc.abstractmethod
    def set_color(self, color):
        return

    @abc.abstractmethod
    def draw_polygon(self, polygon):
        return

    @abc.abstractmethod
    def draw_gradient_polygon(self, polygon):
        return

    def save(self, file_pointer):
        if isinstance(file_pointer, io.BufferedIOBase) or isinstance(file_pointer, file):
            file_pointer.write(self._image)
        elif isinstance(file_pointer, basestring):
            with open(file_pointer, 'w') as fp:
                fp.write(self._image)
        else:
            raise ValueError("Unknown file pointer format")

    def get_supported_shading(self):
        return renderer.ImageRenderer.SHADE_NO,

    def destroy(self):
        return True
