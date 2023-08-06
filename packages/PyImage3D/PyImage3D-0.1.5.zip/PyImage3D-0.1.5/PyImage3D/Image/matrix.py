import copy, math


class ImageMatrix(object):
    def __init__(self):
        self._matrix = None

        self.set_unit_matrix()

    def set_value(self, x, y, value):
        if len(self._matrix) > x:
            if len(self._matrix[x]) > y:
                self._matrix[x][y] = float(value)

    def get_value(self, x, y):
        if len(self._matrix) > x:
            if len(self._matrix[x]) > y:
                return self._matrix[x][y]

    def set_unit_matrix(self):
        self._matrix = [
            [1., 0., 0., 0.],
            [0., 1., 0., 0.],
            [0., 0., 1., 0.],
            [0., 0., 0., 1.],
        ]

    def differential(self, matrix):
        result = ImageMatrix()
        for i in range(4):
            for j in range(4):
                result.set_value(i, j, matrix.get_value(i, j) - self.get_value(i, j))

    def scalar(self, scalar):
        for i in range(4):
            for j in range(4):
                self.set_value(i, j, self.get_value(i, j) * scalar)

    def multiply(self, matrix):
        copied = ImageMatrix()
        copied._matrix = self._matrix

        for i in range(4):
            for j in range(4):
                sum = 0
                for k in range(4):
                    sum += copied.get_value(i, k) * matrix.get_value(k, j)
                self.set_value(i, j, sum)

    def set_rotation_matrix(self, rotx=None, roty=None, rotz=None):
        if rotx is not None:
            rotx = math.radians(rotx)

            matrix = ImageMatrix()
            matrix.set_value(1, 1, math.cos(rotx))
            matrix.set_value(1, 2, math.sin(rotx))
            matrix.set_value(2, 1, -math.sin(rotx))
            matrix.set_value(2, 2, math.cos(rotx))

            self.multiply(matrix)

        if roty is not None:
            roty = math.radians(roty)

            matrix = ImageMatrix()
            matrix.set_value(0, 0, math.cos(roty))
            matrix.set_value(0, 2, -math.sin(roty))
            matrix.set_value(2, 0, math.sin(roty))
            matrix.set_value(2, 2, math.cos(roty))

            self.multiply(matrix)

        if rotz is not None:
            rotz = math.radians(rotz)

            matrix = ImageMatrix()
            matrix.set_value(0, 0, math.cos(rotz))
            matrix.set_value(0, 1, math.sin(rotz))
            matrix.set_value(1, 0, -math.sin(rotz))
            matrix.set_value(1, 1, math.cos(rotz))

            self.multiply(matrix)

    def set_move_matrix(self, movex=0, movey=0, movez=0):
        matrix = ImageMatrix()
        matrix.set_value(3, 0, movex)
        matrix.set_value(3, 1, movey)
        matrix.set_value(3, 2, movez)

        self.multiply(matrix)

    def set_scale_matrix(self, scalex=0, scaley=0, acalez=0):
        matrix = ImageMatrix()
        matrix.set_value(0, 0, scalex)
        matrix.set_value(1, 1, scaley)
        matrix.set_value(2, 2, acalez)

        self.multiply(matrix)