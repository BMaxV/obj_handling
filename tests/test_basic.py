from obj_handling import operations

          
def test():
    verts=[
    [1, 0, 0] ,
    [1, 1, 0] ,
    [0, 1, 0] ,
    [0, 0, 0] ,
    [1, 0, 1] ,
    [1, 1, 1] ,
    [0, 1, 1] ,
    [0, 0, 1] ,
    ]    
    faces=[[1,2,3,4],[1,2,6,5],[2,3,7,6],[3,4,8,7],[4,1,5,8],[5,6,7,8]]
    fn="testcube.obj"
    
    operations.write(fn,"testcube",verts,faces)
    verts_r, faces_r = operations.read(fn)
    
    assert verts_r == verts
    assert faces_r == faces
