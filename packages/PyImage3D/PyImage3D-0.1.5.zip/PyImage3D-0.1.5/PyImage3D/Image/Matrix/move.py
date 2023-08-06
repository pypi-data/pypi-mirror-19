from PyImage3D.Image import matrix


class ImageMatrixMove(matrix.ImageMatrix):
    def __init__(self, x=0, y=0, z=0):
        super(ImageMatrixMove, self).__init__()

        self.set_move_matrix(x, y, z)
