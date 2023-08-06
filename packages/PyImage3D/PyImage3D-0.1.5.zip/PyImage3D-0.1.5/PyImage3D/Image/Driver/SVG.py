from PyImage3D import POLY_WIRE_NO, POLY_WIRE_ONLY
from PyImage3D.Image import driver, renderer


class ImageDriverSVG(driver.ImageDriver):
    def __init__(self):
        self._x = None
        self._y = None

        self._image = ''
        self._id = 1

        self._gradients = []
        self._polygons = []

    def create_image(self, x, y):
        self._x = x
        self._y = y

        self._image = \
"""<?xml version="1.0" ?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
         "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">

<svg xmlns="http://www.w3.org/2000/svg" x="0" y="0" width="{}" height="{}">
""".format(self._x, self._y)
        self._image += '\n\n'

    def set_color(self, color):
        self._add_polygon('\t<polygon id="background{}" points="0,0 {},0 {},{} 0,{}" style="{}" />\n'.
                          format(self._id, self._x, self._x, self._y, self._y, self._get_style(color)))
        self._id += 1

    def _get_style(self, color):
        values = color.get_values()

        values[0] = int(values[0] * 255)
        values[1] = int(values[1] * 255)
        values[2] = int(values[2] * 255)
        values[3] = 1 - values[3]

        return "fill: #{:02x}{:02x}{:02x}; fill-opacity: {:.2f}; stroke: none;".format(*values[:4])

    def _get_wire(self, color):
        values = color.get_values()

        values[0] = int(values[0] * 255)
        values[1] = int(values[1] * 255)
        values[2] = int(values[2] * 255)
        values[3] = 1 - values[3]

        return "fill: none; stroke: #{:02x}{:02x}{:02x}; stroke-opacity: {:.2f};".format(*values[:4])

    def _get_both(self, color):
        values = color.get_values()

        values[0] = int(values[0] * 255)
        values[1] = int(values[1] * 255)
        values[2] = int(values[2] * 255)
        values[3] = 1 - values[3]

        return "fill: #{:02x}{:02x}{:02x}; fill-opacity: {:.2f}; stroke: #000000; stroke-opacity: 1.0;"\
            .format(*values[:4])

    def _get_stop(self, color, offset=0, alpha=None):
        values = color.get_values()

        values[0] = int(values[0] * 255)
        values[1] = int(values[1] * 255)
        values[2] = int(values[2] * 255)
        if alpha is None:
            values[3] = 1 - values[3]
        else:
            values[3] = alpha

        r_str = '\t\t<stop id="stop{}" offset="{:.1f}" style="stop-color: rgb({}, {}, {}); stop-opacity: {:.4f};" />\n'\
            .format(self._id, offset, *values)
        self._id += 1
        return r_str

    def _add_gradient(self, g_str):
        g_id = 'linearGradient' + str(self._id)
        self._id += 1

        self._gradients.append(g_str.replace('[id]', g_id))

        return g_id

    def _add_polygon(self, p_str):
        p_id = 'polygon' + str(self._id)
        self._id += 1

        self._polygons.append(p_str.replace('[id]', p_id))

        return p_id

    def draw_polygon(self, polygon):
        lst = ''
        points = polygon.get_points()
        for point in points:
            lst += "{:.2f},{:.2f} ".format(*point.get_screen_coordinates())

        if polygon.wireframe == POLY_WIRE_NO:
            style = self._get_style(polygon.get_color())
        elif polygon.wireframe == POLY_WIRE_ONLY:
            style = self._get_wire(polygon.get_color())
        else:
            style = self._get_both(polygon.get_color())

        self._add_polygon("\t<polygon points=\"{}\" style=\"{}\" />\n".format(lst[0:-1], style))

    def draw_gradient_polygon(self, polygon):
        lst = ''
        points = polygon.get_points()
        point_dict = {}
        np = 0
        for point in points:
            point_dict[np] = point.get_screen_coordinates()
            lst += "{:.2f},{:.2f} ".format(*point_dict[np])
            np += 1

        xoffs = min(point_dict[0][0], point_dict[1][0], point_dict[2][0])
        yoffs = min(point_dict[0][1], point_dict[1][1], point_dict[2][1])

        xsize = max(abs(point_dict[0][0] - point_dict[1][0]),
                    abs(point_dict[0][0] - point_dict[2][0]),
                    abs(point_dict[1][0] - point_dict[2][0]))
        ysize = max(abs(point_dict[0][1] - point_dict[1][1]),
                    abs(point_dict[0][1] - point_dict[2][1]),
                    abs(point_dict[1][1] - point_dict[2][1]))

        # Base polygon
        lg = self._add_gradient('\t\t<linearGradient id="[id]" x1="{:.2f}" y1="{:.2f}" x2="{:.2f}" y2="{:.2f}">\n{}\t\t</linearGradient>\n'
                                .format(
            (point_dict[0][0] - xoffs) / xsize,
            (point_dict[0][1] - yoffs) / ysize,
            (point_dict[1][0] - xoffs) / xsize,
            (point_dict[1][1] - yoffs) / ysize,
            self._get_stop(points[0].get_color() + self._get_stop(points[1].get_color(), 1))
        ))
        self._add_polygon('\t<polygon id="[id]" points="{}" style="fill: url(#{}); stroke: none; fill-opacity: 1;" />\n'
                          .format(lst, lg))

        # Overlay polygon
        lg = self._add_gradient('\t\t<linearGradient id="[id]" x1="{:.2f}" y1="{:.2f}" x2="{:.2f}" y2="{:.2f}">\n{}\t\t</linearGradient>\n'
                                .format(
            (point_dict[2][0] - xoffs) / xsize,
            (point_dict[2][1] - yoffs) / ysize,
            (((point_dict[0][0] + point_dict[1][0]) / 2) - xoffs) / xsize,
            (((point_dict[0][1] + point_dict[1][1]) / 2) - yoffs) / ysize,
            self._get_stop(points[2].get_color() + self._get_stop(points[2].get_color(), 1, 1))
        ))
        self._add_polygon('\t<polygon id="[id]" points="{}" style="fill: url(#{}); stroke: none; fill-opacity: 1;" />\n'
                          .format(lst, lg))

    def save(self, file_pointer):
        self._image += "\t<defs id=\"defs{}\">\n".format(self._id)
        self._image += "".join(self._gradients)
        self._image += "\t</defs>\n\n"

        self._image += "".join(self._polygons)
        self._image += "</svg>\n"

        super(ImageDriverSVG, self).save(file_pointer)

    def destroy(self):
        self._image = ''
        return True

    def get_supported_shading(self):
        return renderer.ImageRenderer.SHADE_NO, renderer.ImageRenderer.SHADE_FLAT, renderer.ImageRenderer.SHADE_GOURAUD,
