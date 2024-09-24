from obj_handling import operations
import unittest

class TestMyObjectWriter(unittest.TestCase):

        
    def test(self):
        verts, faces = operations.get_test_cube()
        fn = "./testcube.obj"
        
        operations.write(fn,"testcube",verts,faces)
        verts_r, faces_r = operations.read(fn)
        
        assert verts_r == verts
        assert faces_r == faces

if __name__=="__main__":
    unittest.main()
