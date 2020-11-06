def read(fn):
    verts=[]
    faces=[]
    with open(fn,"r") as f:
        t=f.readlines()
    
    for line in t:
        line=line.replace("\n","")
        line=line.split(" ")
        while "" in line:
            line.remove("")
        print([line])
        if line[0]=="v":
            vert=[]
            for x in line[1:]:
                vert.append(float(x))
            verts.append(vert)
        if line[0]=="f":
            face=[]
            for x in line[1:]:
                face.append(int(x))
            faces.append(face)
    return verts, faces
    
if __name__=="__main__":
    r=main("testcube.obj")
    print(r)
