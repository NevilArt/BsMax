import bpy, bmesh, itertools
from functools import reduce

# Original code from https://blenderartists.org/u/maxiv94
# https://blenderartists.org/t/interactive-tools-for-blender-2-8/1164932

#Global Variables
ITERATION_LIMIT = 200

def list_intersection(a, b):
	return list(set(a) & set(b))

def list_difference(a,b):
	return list(set(a) - set(b))

def get_bmesh():
	return bmesh.from_edit_mesh(bpy.context.edit_object.data)

def get_selected(verts = False, edges = False, faces = False, get_item = False):
	bm = get_bmesh()
	if verts:
		update_indexes(verts = True)
		selected_verts = []
		for vert in bm.verts:
			if vert.select :
				if get_item:
					selected_verts.append(vert)
				else:
					selected_verts.append(vert.index)
		return selected_verts
	if edges:
		update_indexes(edges = True)
		selected_edges = []
		for edge in bm.edges:
			if edge.select:
				if get_item:
					selected_edges.append(edge)
				else:
					selected_edges.append(edge.index)
		return selected_edges
	if faces:
		update_indexes(faces=True)
		selected_faces = []
		for face in bm.faces:
			if face.select:
				if get_item:
					selected_faces.append(face)
				else:
					selected_faces.append(face.index)
		return selected_faces

def update_indexes(verts = False, edges = False, faces = False):
	bm = get_bmesh()
	if verts:
		bm.verts.index_update()
	if edges:
		bm.edges.index_update()
	if faces:
		bm.faces.index_update()
	bm.verts.ensure_lookup_table()
	bm.edges.ensure_lookup_table()
	bm.faces.ensure_lookup_table()
	bmesh.update_edit_mesh(bpy.context.edit_object.data)

def select_from_index(	indexes,
						verts = False,
						edges = False,
						faces = False,
						replace = False,
						add_to_history = False,
						deselect = False ):
	selection_value = True
	bm = get_bmesh()
	if replace:
		bpy.ops.mesh.select_all(action = 'DESELECT')
	if deselect:
		selection_value = False
	if verts:
		for index in indexes:
			bm.verts[index].select = selection_value
			if add_to_history:
				bm.select_history.add(bm.verts[index])
	if edges:
		for index in indexes:
			bm.edges[index].select = selection_value
			if add_to_history:
				bm.select_history.add(bm.edges[index])
	if faces:
		for index in indexes:
			bm.faces[index].select = selection_value
			if add_to_history:
				bm.select_history.add(bm.faces[index])

def select_from_item(	items, verts = False,
						edges = False,
						faces = False,
						replace = False,
						add_to_history = False,
						deselect = False):
	selection_value = True
	bm = get_bmesh()
	if replace:
		bpy.ops.mesh.select_all(action = 'DESELECT')
	if deselect:
		selection_value = False
	if verts:
		for item in items:
			bm.verts[item.index].select = selection_value
			if add_to_history:
				bm.select_history.add(bm.verts[item.index])
	if edges:
		for item in items:
			bm.edges[item.index].select = selection_value
			if add_to_history:
				bm.select_history.add(bm.edges[item.index])
	if faces:
		for item in items:
			bm.faces[item.index].select = selection_value
			if add_to_history:
				bm.select_history.add(bm.faces[item.index])

def verts_share_edge(verts):
	if len(verts) == 2:
		return len(list_intersection(verts[0].link_edges, verts[1].link_edges)) == 1	
	else:
		return False

def verts_share_face(verts):
	face_list = []
	for vert in verts:
		face_list.append(vert.link_faces)
	face_list = reduce(lambda x, y:list_intersection(x,y) ,face_list)
	if len(face_list) > 0:
		return True
	else:
		return False

def split_edge_select_vert(change_selection = False):
	selection = get_selected(verts = True)
	bpy.ops.mesh.subdivide()
	if change_selection:
		new_selection = get_selected(verts = True)
		new_selection = list_difference(new_selection, selection)
		select_from_index(new_selection, verts = True,replace = True)
		bpy.context.scene.tool_settings.mesh_select_mode = [True,False,False]
	return new_selection

def quad_fill():
	selection = get_selected(edges = True)
	bpy.ops.mesh.delete(type = 'FACE')
	select_from_index(selection, edges = True, replace = True)
	bpy.ops.mesh.fill_grid()

def is_border_vert(vert):
	borderEdges = [edge for edge in vert.link_edges if len(edge.link_faces) == 1]
	return len(borderEdges) > 1

def are_border_verts(verts):
	return all(is_border_vert(vert) for vert in verts) 

def is_border_edge(edge):
	return all(is_border_vert(vert) for vert in edge.verts)

def is_border(selection):
	#every edge must be adjacent with two other edges, if its a closed border the number of adjacent edges should be at least 2 X number edges
	number_adjacent_edges = len([neightbour for edge in selection for verts in edge.verts for neightbour in verts.link_edges if neightbour in selection and neightbour is not edge])
	return all(is_border_edge(edge) for edge in selection) and number_adjacent_edges >= len(selection) * 2 

def is_ring(selection):
	neightbour_Numbers = [edge for edge in selection if len([face for face in edge.link_faces if any(edge2 for edge2 in face.edges if edge2 in selection and edge2 != edge)]) > 0]
	return len(neightbour_Numbers) == len(selection)

def is_adjacent(selection):
	vert_list = [edge.verts for edge in selection]
	common_vert = reduce(lambda x, y: list_intersection(x, y), vert_list)
	return len(common_vert) == 1

__all__ = [	"ITERATION_LIMIT",
			"list_intersection",
			"list_difference",
			"get_bmesh",
			"get_selected",
			"update_indexes",
			"select_from_index",
			"select_from_item",
			"verts_share_edge",
			"verts_share_face",
			"split_edge_select_vert",
			"quad_fill",
			"is_border_vert",
			"are_border_verts",
			"is_border_edge",
			"is_border",
			"is_ring",
			"is_adjacent" ]