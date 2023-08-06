from PyImage3D.Image import matrix


class ImageMatrixRotate(matrix.ImageMatrix):
    def __init__(self, x=0, y=0, z=0):
        super(ImageMatrixRotate, self).__init__()

        self.set_rotation_matrix(x, y, z)
