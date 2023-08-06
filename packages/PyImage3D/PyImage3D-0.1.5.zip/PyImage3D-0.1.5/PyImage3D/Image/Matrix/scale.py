from PyImage3D.Image import matrix


class ImageMatrixScale(matrix.ImageMatrix):
    def __init__(self, x=0, y=0, z=0):
        super(ImageMatrixScale, self).__init__()

        self.set_scale_matrix(x, y, z)
