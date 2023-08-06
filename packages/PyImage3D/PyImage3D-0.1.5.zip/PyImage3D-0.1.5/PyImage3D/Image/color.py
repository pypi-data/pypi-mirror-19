class ImageColor(object):
    def __init__(self, red=0., green=0., blue=0., alpha=0., reflection=None):
        self._rgba_value = []
        self._lights = []
        self._light = [0., 0., 0.,]

        self._reflection = 0.

        values = (red, green, blue, alpha,)
        for v in values:
            if 0 < v < 1:
                self._rgba_value.append(min(1., max(0., v)))
            elif v > 1:
                self._rgba_value.append(min(1., max(0., v / 255.)))
            else:
                self._rgba_value.append(0.)

        self.set_reflection(reflection)

    def mix_alpha(self, alpha=0.):
        if 0 < alpha < 1:
            self._rgba_value[3] = min(1., max(0., alpha))
        elif alpha > 1:
            self._rgba_value[3] = min(1., max(0., alpha / 255.))
        else:
            self._rgba_value[3] = 0

    def get_reflection(self):
        return self._reflection

    def set_reflection(self, reflection=0.):
        self._reflection = min(1., max(0., reflection))

    def get_values(self):
        return list(self._rgba_value)

    def add_light(self, color, intensity):
        self._lights.append([intensity, color])

    def _calc_lights(self):
        for intensity, color in self._lights:
            color_arr = self.get_values()

            self._light[0] = color_arr[0] + intensity * color[0]
            self._light[1] = color_arr[1] + intensity * color[1]
            self._light[2] = color_arr[2] + intensity * color[2]

    def _mix_color(self):
        self._rgba_value[0] = min(1, self._rgba_value[0] * self._light[0])
        self._rgba_value[1] = min(1, self._rgba_value[1] * self._light[1])
        self._rgba_value[2] = min(1, self._rgba_value[2] * self._light[2])

    def calculate_color(self):
        if not self._lights:
            self._rgba_value = [0, 0, 0, self._rgba_value[3]]

            self._calc_lights()
            self._mix_color()

    def merge(self, colors):
        count = 0
        for color in colors:
            values = color.get_values()

            self._rgba_value[0] += values[0]
            self._rgba_value[1] += values[1]
            self._rgba_value[2] += values[2]
            self._rgba_value[3] += values[3]

            count += 1

        self._rgba_value[0] /= count
        self._rgba_value[1] /= count
        self._rgba_value[2] /= count
        self._rgba_value[3] /= count

    def __repr__(self):
        return "Color: r {:.2f} g {:.2f} b {:.2f} a {:.2f}".format(*self._rgba_value)
