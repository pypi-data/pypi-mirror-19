from PyImage3D.Image import helper, point
from PyImage3D.Image.Paintable import polygon


class ImagePaintableObject(object):
    @property
    def wireframe(self):
        return self._wireframe

    @wireframe.setter
    def wireframe(self, value):
        self._wireframe = value

        for polygon in self._polygons:
            polygon.wireframe = value

    def __init__(self):
        self._polygons = []

        self._wireframe = False

    def get_polygon_count(self):
        return len(self._polygons)

    def set_color(self, color):
        for polygon in self._polygons:
            polygon.set_color(color)

    def set_option(self, option, value):
        for polygon in self._polygons:
            polygon.set_option(option, value)

    def transform(self, matrix, tid=None):
        if tid is None:
            tid = helper.unique_id()

        for polygon in self._polygons:
            polygon.transform(matrix, tid)

    def get_polygons(self):
        return list(self._polygons)

    def _add_polygon(self, polygon):
        polygon.wireframe = self._wireframe
        self._polygons.append(polygon)

    def _build_incidence_graph(self):
        polygons = self.get_polygons()

        surfaces = {}
        edges = []
        points = []

        point_hash = {}
        edge_hash = {}

        np = 0
        for polygon in polygons:
            poly_points = polygon.get_points()

            last_index = None
            first_index = None

            for point in poly_points:
                pp_hash = str(point)
                if pp_hash in point_hash:
                    pp_index = point_hash[pp_hash]
                else:
                    points.append(point)
                    pp_index = len(point_hash) - 1
                    point_hash[pp_hash] = pp_index

                if last_index is not None:
                    edge_points = [pp_index, last_index]
                    edge_points.sort()
                    pe_hash = " -< ".join(edge_points)

                    if pe_hash in edge_hash:
                        if np not in surfaces:
                            surfaces[np] = []
                        surfaces[np].append(edge_hash[pe_hash])
                    else:
                        edges.append(edge_points)
                        edge_hash[pe_hash] = len(edges) - 1
                        if np not in surfaces:
                            surfaces[np] = []
                        surfaces[np].append(edge_hash[pe_hash])
                else:
                    first_index = pp_index

                last_index = pp_index

            edge_points = [first_index, last_index]
            edge_points.sort()
            pe_hash = " -< ".join(edge_points)

            if pe_hash in edge_hash:
                if np not in surfaces:
                    surfaces[np] = []
                surfaces[np].append(edge_hash[pe_hash])
            else:
                edges.append(edge_points)
                edge_hash[pe_hash] = len(edges) - 1
                if np not in surfaces:
                    surfaces[np] = []
                surfaces[np].append(edge_hash[pe_hash])

            np += 1

        return {
            'surfaces': surfaces,
            'edges': edges,
            'points': points
        }

    def subdivide_surfaces(self, factor=1):
        for i in range(factor):
            data = self._build_incidence_graph()

            edge_surfaces = {}
            edge_middles = []
            point_edges = {}

            face_points = {}
            edge_points = []
            old_points = {}

            for surface, edges in data['surfaces'].iteritems():
                points = []
                for edge in edges:
                    points += data['edges'][edge]
                    if edge not in edge_surfaces:
                        edge_surfaces[edge] = []
                    edge_surfaces[edge].append(surface)
                    points = set(points)

                face_point = [0, 0, 0]
                point_count = len(points)
                for point in points:
                    face_point[0] += data['points'][point].x / point_count
                    face_point[1] += data['points'][point].y / point_count
                    face_point[2] += data['points'][point].z / point_count

                face_points[surface] = point.ImagePoint(face_point[0], face_point[1], face_point[2])

            edge = 0
            for points in data['edges']:
                if edge in edge_middles:
                    edge_middle = edge_middles[edge]
                else:
                    edge_middle = [0, 0, 0]
                    point_count = len(points)
                    for point in points:
                        if point not in point_edges:
                            point_edges[points] = []
                        point_edges[point] = edge

                        edge_middle[0] += data['points'][points].x / point_count
                        edge_middle[1] += data['points'][points].y / point_count
                        edge_middle[2] += data['points'][points].z / point_count
                    edge_middles[edge] = edge_middle

                average_face = [0, 0, 0]
                point_count = len(edge_surfaces[edge])
                for surface in edge_surfaces[edge]:
                    average_face[0] += edge_points[surface].x / point_count
                    average_face[1] += edge_points[surface].y / point_count
                    average_face[2] += edge_points[surface].z / point_count

                edge_points[edge] = point.ImagePoint(
                    (average_face[0] + edge_middle[0]) / 2,
                    (average_face[1] + edge_middle[1]) / 2,
                    (average_face[2] + edge_middle[2]) / 2
                )

                edge += 1

            npoint = 0
            for value in data['points']:
                r = [0, 0, 0]
                surfaces = []
                point_count = len(point_edges[npoint])
                for edge in point_edges[npoint]:
                    r[0] += edge_middles[edge][0] / point_count
                    r[1] += edge_middles[edge][1] / point_count
                    r[2] += edge_middles[edge][2] / point_count

                    surfaces += edge_surfaces[edge]

                surfaces = set(surfaces)

                q = [0, 0, 0]
                surface_count = len(surfaces)
                for surface in surfaces:
                    q[0] += face_points[surface][0] / surface_count
                    q[1] += face_points[surface][1] / surface_count
                    q[2] += face_points[surface][2] / surface_count

                n = len(point_edges[npoint])
                old_points[npoint] = point.ImagePoint(
                    (q[0] / n) + ((2 * r[0]) / n) + ((value.x * (n - 3)) / n),
                    (q[1] / n) + ((2 * r[1]) / n) + ((value.y * (n - 3)) / n),
                    (q[2] / n) + ((2 * r[2]) / n) + ((value.z * (n - 3)) / n)
                )

                npoint += 1

            self._polygons = []
            for surface, face_point in face_points.iteritems():
                points = []
                for edge in data['surface']:
                    points += data['edges'][edge]
                points = set(points)

                for point in points:
                    edges = list(set(point_edges[point]) & set(data['surfaces'][surface]))
                    self._add_polygon(polygon.ImagePaintablePolygon([
                        old_points[point],
                        edge_points[edges[0]],
                        face_point,
                        edge_points[edges[1]]
                    ]))

    def __repr__(self):
        repr_str = "Object: polygons {:d}\n".format(len(self._polygons))
        for polygon in self._polygons:
            repr_str += "\t" + str(polygon) + "\n"

        return repr_str
