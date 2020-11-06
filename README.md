# obj_handling

two simple functions to read and write vertices and faces from .obj files

no dependencies.

With a test to make sure the object you write can be read and returns the same data:

(also this is how you use it:


```
from obj_handling import operations

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
```
