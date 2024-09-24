from vector import vector


def get_test_cube():

    verts = [
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 0],
        [0, 0, 0],
        [1, 0, 1],
        [1, 1, 1],
        [0, 1, 1],
        [0, 0, 1],
    ]

    faces = [[0, 1, 2, 3],
             [0, 1, 5, 4],
             [1, 2, 6, 5],
             [2, 3, 7, 6],
             [3, 0, 4, 7],
             [4, 5, 6, 7]
             ]

    return verts, faces


def analyze_mesh(verts, faces, plane_point, plane_normal):
    crosssection_polygons = []
    on_side_a_total = []
    on_side_b_total = []
    in_plane_points = []
    new_edges = []
    new_vert_indices_in_new_verts = []

    fully_side_a = []
    fully_side_b = []

    for face in faces:

        # the face has verts on side a of the plane
        # s.a. since we're only interested in cases
        # of "true" for both, we start with two falses

        on_side_a = []
        on_side_b = []
        in_plane = []
        side_a = True
        side_b = True
        for index in face:
            vert = vector.Vector(*verts[index])
            lp = vert - plane_point
            product = plane_normal.dot(lp)
            product = round(product, 4)
            if product > 0:
                on_side_a.append(index)
                side_b = False
            if product < 0:
                on_side_b.append(index)
                side_a = False
            if product == 0:
                in_plane.append(index)
                in_plane_points.append(index)

        # these are needed for selection purposes

        if side_a:
            fully_side_a.append(face)
        if side_b:
            fully_side_b.append(face)

        on_side_a_total += on_side_a
        on_side_b_total += on_side_b
        if (on_side_a and on_side_b) or (on_side_a and in_plane) or (on_side_b and in_plane):
            crosssection_polygons.append(
                [face, on_side_a, on_side_b, in_plane])
    return on_side_a_total, on_side_b_total, crosssection_polygons, in_plane_points, fully_side_a, fully_side_b


def get_cut_edges(crosssection_polygons):
    cut_edges = []

    for plist in crosssection_polygons:
        if plist[4][1] != []:
            new_edge1 = set(plist[4][1]).difference(set(plist[2]))
            cut_edges.append(new_edge1)
        if plist[4][0] != []:
            new_edge2 = set(plist[4][0]).difference(set(plist[1]))
            cut_edges.append(new_edge2)
    return cut_edges


def create_new_faces(crosssection_polygons):
    # this creates the new faces to replace those that get cut
    for plist in crosssection_polygons:

        mymax = 2
        counter = 0
        while counter < mymax:
            side_face = plist[4][counter]
            actual_face = []
            for edge in side_face:
                if actual_face == []:
                    actual_face.append(set(edge))
                else:
                    actual_face[0] = actual_face[0].union(set(edge))
            if actual_face == []:
                counter += 1
                continue
            actual_face = tuple(actual_face[0])
            plist[4][counter] = actual_face
            counter += 1


def cut_plane_add(d, vert_index, edge, cross_section_object, side_a_face, side_b_face):
    # this is an extra in case a point is actually in the cutting plane

    side_a_org = cross_section_object[1]
    side_b_org = cross_section_object[2]

    ep1 = edge[0]
    ep2 = edge[1]

    # why are these different?
    # oh, because one is new.
    if (d == 0 and ep1 in side_a_org) or (d == 1 and ep2 in side_a_org):
        side_a_face.append((ep1, ep2))
        return

    if (d == 0 and ep1 in side_b_org) or (d == 1 and ep2 in side_b_org):
        side_b_face.append((ep1, ep2))
        return

    # regular case.
    if d not in [0, 1]:
        if ep1 in side_a_org:
            side_a_face.append((ep1, vert_index))
            side_b_face.append((vert_index, ep2))

        else:
            # if ep1 in side_b_org:
            side_b_face.append((ep1, vert_index))
            side_a_face.append((vert_index, ep2))


def create_and_file_new_point(verts, edge, d, point_vec, new_verts):
    new_vert = vector.Vector(*verts[edge[1]]) + vector.Vector(*(d * point_vec))

    # calculates new vert in the plane

    d = round(d, 5)

    if new_vert not in new_verts:
        new_verts.append(new_vert)
        vert_index = len(verts) + len(new_verts)-1
    else:
        vert_index = new_verts.index(new_vert) + len(verts)
    return new_vert, vert_index


def file_into_groups(d, edge, vert_index, cut_plane_point_pairs, in_plane_points):

    if d == 0 or d == 1:
        if d == 0:
            cut_plane_point_pairs.append((edge[0], vert_index))
        if d == 1:
            cut_plane_point_pairs.append((edge[1], vert_index))
        in_plane_points.append(vert_index)


def index_correction(crosssection_polygons, verts, in_plane_points, new_verts):
    # this corrects the index in the b side face

    # I hate this so much.
    counter = 0
    max = len(crosssection_polygons)
    while counter < max:
        thing = crosssection_polygons[counter]
        counter2 = 0
        max2 = len(thing[4][1])
        thing[4][1] = list(thing[4][1])
        while counter2 < max2:
            thing2 = thing[4][1][counter2]
            if thing2 > len(verts)-1 and thing2 not in in_plane_points:
                thing[4][1][counter2] = thing[4][1][counter2]+len(new_verts)
            counter2 += 1
        counter += 1


def include_in_plane_points(cut_edges, in_plane_points):
    in_plane_points = set(in_plane_points)

    counter = 0
    mymax = len(cut_edges)-1
    for meh_point in list(in_plane_points):
        for edge in edge_list:
            if meh_point == edge[0]:
                if edge[1] in list(in_plane_points) and set(edge) not in cut_edges:
                    cut_edges.append(set(edge))
            if meh_point == edge[1]:
                if edge[0] in list(in_plane_points) and set(edge) not in cut_edges:
                    cut_edges.append(set(edge))


def get_normal_direction_polys(verts, faces, in_plane_points):
    """...what"""
    normal_direction_polys = []

    for poly in faces:
        append = True
        for vert in poly:
            if vert not in in_plane_points:
                append = False
                break
        if append == True:
            normal_direction_polys.append(poly)
    return normal_direction_polys


def get_useless_edges(normal_direction_polys):
    useless_edges = []
    for poly in normal_direction_polys:
        for poly2 in normal_direction_polys:
            if poly != poly2:
                # this won't work :/
                u_edge = set(poly.edge_keys).intersection(set(poly2.edge_keys))
                if u_edge:
                    u_edge = set(list(u_edge)[0])
                if u_edge != set():
                    if u_edge not in useless_edges:
                        useless_edges.append(u_edge)
    return useless_edges

    # polygon , on side a , on side b , in plane


def duplicate_crosssection_faces(crosssection_polygons, verts, faces, plane_point, plane_normal, in_plane_points):

    vert_amount = len(verts)
    cut_plane_point_pairs = []
    new_verts = []
    faces1 = []
    faces2 = []
    for cross_section_object in crosssection_polygons:
        # these are the new side faces.
        side_a_face = []
        side_b_face = []

        # this is where the new point will go

        cross_section_object.append([side_a_face, side_b_face])
        edge_tuples = []

        real_face = cross_section_object[0]
        c = -1
        m = len(real_face)-1
        while c < m:
            edge_tuples.append((real_face[c], real_face[c+1]))
            c += 1

        for edge in edge_tuples:

            # if the edge is entirely on one side of the plane

            found_side_a = cross_section_object[1]
            found_side_b = cross_section_object[2]

            if edge[0] in found_side_a and edge[1] in found_side_a:
                side_a_face.append(edge)
                continue

            if edge[0] in found_side_b and edge[1] in found_side_b:
                side_b_face.append(edge)
                continue

            # what's left are edges that have verts on both sides of the plane
            # or faces with points or even an edge in the plane

            edgepoint1 = vector.Vector(*verts[edge[0]])
            edgepoint2 = vector.Vector(*verts[edge[1]])

            point_vec = edgepoint1 - edgepoint2

            # point_vec=Vector((verts[edge[0]].co[0]-verts[edge[1]].co[0],
            # verts[edge[0]].co[1]-verts[edge[1]].co[1],
            # verts[edge[0]].co[2]-verts[edge[1]].co[2]))
            d = 0
            if point_vec.dot(plane_normal) != 0:
                vec = plane_point - edgepoint2
                dp1 = vec.dot(plane_normal)
                dp2 = point_vec.dot(plane_normal)
                d = dp1 / dp2

                # d = (Vector((plane_point[0]-verts[edge[1]].co[0],point[1]-verts[edge[1]].co[1],point[2]-verts[edge[1]].co[2])).dot(direction))/(point_vec.dot(direction))

            # d is the distance of the vert edge[0] to the plane
            # in direction of the vector from edge[0] to edge[1]

            new_vert, vert_index = create_and_file_new_point(
                verts, edge, d, point_vec, new_verts)

            # normal cases are done here, from here it's special cases
            file_into_groups(d, edge, vert_index,
                             cut_plane_point_pairs, in_plane_points)
            cut_plane_add(d, vert_index, edge,
                          cross_section_object, side_a_face, side_b_face)

        if side_a_face != []:
            faces1.append(side_a_face)
        if side_b_face != []:
            faces2.append(side_b_face)

    return new_verts, cut_plane_point_pairs, faces1, faces2


def cut(verts, faces, plane_point, plane_normal):
    """I honestly don't really get what I'm doing here.

    I'm manipulating one object in place and the other one...
    was originally newly created. Hm.
    """

    r = analyze_mesh(verts, faces, plane_point, plane_normal)
    on_side_a_total, on_side_b_total, crosssection_polygons, in_plane_points, fully_side_a, fully_side_b = r

    new_verts, cut_plane_point_pairs, faces1, faces2 = duplicate_crosssection_faces(
        crosssection_polygons, verts, faces, plane_point, plane_normal, in_plane_points)

    # indexing
    create_new_faces(crosssection_polygons)
    index_correction(crosssection_polygons, verts, in_plane_points, new_verts)

    # from here on it's about the creation of the new faces
    cut_edges = get_cut_edges(crosssection_polygons)

    # these are catches for points, edges and whole areas in the plane
    include_in_plane_points(cut_edges, in_plane_points)

    normal_direction_polys = get_normal_direction_polys(
        verts, faces, in_plane_points)
    useless_edges = get_useless_edges(normal_direction_polys)

    for element in useless_edges:
        cut_edges.remove(element)

    incomplete_cut_areas = []
    complete_cut_areas = []
    if cut_edges != []:
        if incomplete_cut_areas == []:
            incomplete_cut_areas.append(cut_edges.pop(0))

    if False:

        # this code is doing the normal cases where no points or edges
        # are in the cutting plane the rest has already been dealt with

        while cut_edges != []:
            current_edge = cut_edges.pop(0)
            counter = 0
            max = len(incomplete_cut_areas)
            appended = False
            while counter < max:
                area = incomplete_cut_areas[counter]
                if list(current_edge.intersection(area)) != []:
                    if len(list(current_edge.intersection(area))) == 2:
                        complete_cut_areas.append(area.union(current_edge))
                        incomplete_cut_areas.remove(area)
                        if cut_edges != []:
                            incomplete_cut_areas.append(cut_edges.pop(0))

                    else:
                        incomplete_cut_areas[counter] = area.union(
                            current_edge)
                    appended = True
                counter += 1
            if appended == False:
                cut_edges.append(current_edge)

    full_verts = verts + new_verts
    # on_side_a_total, on_side_b_total

    cut_face = []
    for vert in new_verts:
        index = full_verts.index(vert)
        cut_face.append(index)

    # fully_side_a, fully_side_b
    verts1, faces1 = separate_verts(faces1, full_verts, fully_side_a, cut_face)
    verts2, faces2 = separate_verts(faces2, full_verts, fully_side_b, cut_face)

    # from here on, all the calculations are done. this part of the code adds all new
    # parts and deletes the old ones

    # the rest didn't make sense to me anymore.

    return verts1, faces1, verts2, faces2


def separate_verts(faces, full_verts, fully_one_side, cut_face):
    filtered_verts = []
    new_faces = []

    for face in faces:

        good_face = []
        c = -1
        m = len(face)-1
        while c < m:
            i1, i2 = face[c]
            i3, i4 = face[c+1]
            for i in [i1, i2, i3, i4]:
                if i not in good_face:
                    good_face.append(i)
            c += 1

        new_face = []
        for index in good_face:
            vert = vector.Vector(*full_verts[index])
            if vert not in filtered_verts:
                filtered_verts.append(vert)
            new_face.append(filtered_verts.index(vert))
        new_faces.append(new_face)

    # doesn't really matter at this point.
    if len(cut_face) > 2:
        # if it's just an edge, I don't actually need it.
        fully_one_side.append(cut_face)

    for face in fully_one_side:
        new_face = []
        for index in face:
            vert = vector.Vector(*full_verts[index])
            if vert not in filtered_verts:
                filtered_verts.append(vert)
            new_face.append(filtered_verts.index(vert))
        new_faces.append(new_face)

    return filtered_verts, new_faces


def write(filename, objectname, vertices, faces):
    with open(filename, "w") as f:
        if objectname == None:
            f.write("o "+objectname+"\n")

        for vert in vertices:
            f.write("v ")
            for i in vert:
                f.write(str(i)+" ")
            f.write("\n")

        for face in faces:
            f.write("f ")
            for i in face:
                f.write(str(i)+" ")
            f.write("\n")


def read(fn):
    verts = []
    faces = []
    with open(fn, "r") as f:
        t = f.readlines()

    for line in t:
        line = line.replace("\n", "")
        line = line.split(" ")
        while "" in line:
            line.remove("")

        if line[0] == "v":
            vert = []
            for x in line[1:]:
                vert.append(float(x))
            verts.append(vert)
        if line[0] == "f":
            face = []
            for x in line[1:]:
                face.append(int(x))
            faces.append(face)
    return verts, faces


if __name__ == "__main__":
    test()
