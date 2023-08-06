import copy


from PyImage3D.Image.Paintable import light


class ImagePaintableLightAmbient(light.ImagePaintableLight):
    def __init__(self, x=0, y=0, z=0, parameter=()):
        super(ImagePaintableLightAmbient, self).__init__(0, 0, 0)

    def get_color(self, polygon):
        color = copy.copy(polygon.get_color())

        color.add_light(self.get_raw_color(), 1)

        return color
