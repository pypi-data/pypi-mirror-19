from PyImage3D.Image import renderer


class ImageRendererPerspective(renderer.ImageRenderer):
    def _calculate_screen_coordinates(self, point):
        viewpoint = 40000.
        distance = 50000.

        sc_coord = (viewpoint * point.x / (distance + point.z) + self._size[0],
                    viewpoint * point.y / (distance + point.z) + self._size[1],)

        point.set_screen_coordinates(*sc_coord)

    def _sort_polygons(self):
        polygon_depth = []
        for polygon in self._polygons:
            polygon_depth.append(polygon.get_mid_z())

        # Sort self._polygons using the indexes sorted from polygon_depth
        sorted_keys = sorted(range(len(polygon_depth)), key=lambda x: int(polygon_depth[x]), reverse=True)
        self._polygons[:] = [self._polygons[i] for i in sorted_keys]
