import unittest

from obj_handling import operations
from vector import vector


class MyCutTest(unittest.TestCase):
    def test_cube(self):
        verts, faces = operations.get_test_cube()
        point = vector.Vector(0.5, 0.5, 0.5)
        n = vector.Vector(1, 0, 0)
        verts1, faces1, verts2, faces2 = operations.cut(verts, faces, point, n)

        assert len(verts1) == 8
        assert len(verts2) == 8

        assert len(faces1) == 6
        assert len(faces2) == 6

    def test_works_with_polygons(self):
        # verts, faces = operations.get_test_cube()
        verts = [[1, 0, 0],
                 [1, 1, 0],
                 [0, 1, 0],
                 [0, 0, 0],]
        faces = [[0, 1, 2, 3]]
        point = vector.Vector(0.5, 0.5, 0.5)
        n = vector.Vector(1, 0, 0)

        verts1, faces1, verts2, faces2 = operations.cut(verts, faces, point, n)

        assert len(verts1) == 4
        assert len(verts2) == 4

        assert len(faces1) == 1
        assert len(faces2) == 1

    def test_clean_1(self):
        verts = [[1, 0, 0],
                 [1, 1, 0],
                 [0, 1, 0],
                 [0, 0, 0],]
        faces = [[0, 1, 2, 3]]
        point = vector.Vector(1.5, 0.5, 0.5)
        n = vector.Vector(1, 0, 0)

        verts1, faces1, verts2, faces2 = operations.cut(verts, faces, point, n)

        assert len(verts1) == 0
        assert len(verts2) == 4

        assert len(faces1) == 0
        assert len(faces2) == 1

    def test_clean_2(self):
        verts = [[1, 0, 0],
                 [1, 1, 0],
                 [0, 1, 0],
                 [0, 0, 0],]
        faces = [[0, 1, 2, 3]]
        point = vector.Vector(-0.5, 0.5, 0.5)
        n = vector.Vector(1, 0, 0)

        verts1, faces1, verts2, faces2 = operations.cut(verts, faces, point, n)

        assert len(verts1) == 4
        assert len(verts2) == 0

        assert len(faces1) == 1
        assert len(faces2) == 0


if __name__ == "__main__":
    unittest.main()
