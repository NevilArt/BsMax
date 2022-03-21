############################################################################
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################################################

import bpy, bmesh, itertools, mesh_f2, math
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, EnumProperty
from functools import reduce
from bpy_extras.view3d_utils import region_2d_to_location_3d, region_2d_to_vector_3d
from mathutils import Vector
 
#Global Variables
ITERATION_LIMIT = 200

#Utility Functions
 
def list_intersection(a, b):
	return list(set(a) & set(b))
 
def list_difference(a,b):
	return list(set(a) - set(b))
 
def get_bmesh(ctx):
	return bmesh.from_edit_mesh(ctx.edit_object.data)

def get_bmesh_from_obj(ctx):
	return bmesh.from_object(ctx.active_object.data)

def update_indexes(ctx, verts=False, edges=False, faces=False):
	bm = get_bmesh(ctx)
	if verts:
		bm.verts.index_update()
	if edges:
		bm.edges.index_update()
	if faces:
		bm.faces.index_update()
	bm.verts.ensure_lookup_table()
	bm.edges.ensure_lookup_table()
	bm.faces.ensure_lookup_table()
	bmesh.update_edit_mesh(ctx.edit_object.data)
 
def get_selected(ctx, verts=False, edges = False, faces = False, get_item = False):
	bm = get_bmesh(ctx)
	if verts:
		update_indexes(ctx, verts=True)
		selected_verts = []
		for vert in bm.verts:
			if vert.select :
				if get_item:
					selected_verts.append(vert)
				else:
					selected_verts.append(vert.index)
		return selected_verts
	if edges:
		update_indexes(ctx, edges=True)
		selected_edges = []
		for edge in bm.edges:
			if edge.select:
				if get_item:
					selected_edges.append(edge)
				else:
					selected_edges.append(edge.index)
		return selected_edges
	if faces:
		update_indexes(ctx, faces=True)
		selected_faces = []
		for face in bm.faces:
			if face.select:
				if get_item:
					selected_faces.append(face)
				else:
					selected_faces.append(face.index)
		return selected_faces

def select_from_index(ctx, indexes, verts=False, edges=False, faces=False, replace=False, add_to_history=False, deselect=False):
	selection_value = True
	bm = get_bmesh(ctx)
	if replace:
		bpy.ops.mesh.select_all(action='DESELECT')
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

def select_from_item(ctx, items, verts = False,edges = False, faces = False, replace = False, add_to_history = False, deselect = False):
	selection_value = True
	bm = get_bmesh(ctx)
	if replace:
		bpy.ops.mesh.select_all(action='DESELECT')
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
	face_list = reduce(lambda x,y:list_intersection(x,y) ,face_list)
	if len(face_list) > 0:
		return True
	else:
		return False

#aproximation, might not work all the times
def is_corner_vert(vert):
	cornerVerts = [face for face in vert.link_faces]
	return len(cornerVerts) > 2  
	
def is_border_vert(vert):
	borderEdges = [edge for edge in vert.link_edges if len(edge.link_faces) == 1]
	return len(borderEdges) > 1

def are_border_verts(verts):
	return all(is_border_vert(vert) for vert in verts) 

def is_border_edge(edge):
	return all(is_border_vert(vert) for vert in edge.verts)

#selection needs to be edges
def is_border(selection):
	#every edge must be adjacent with two other edges, if its a closed border the number of adjacent edges should be at least 2 X number edges
	number_adjacent_edges = len([neightbour for edge in selection for verts in edge.verts for neightbour in verts.link_edges if neightbour in selection and neightbour is not edge])
	return all(is_border_edge(edge) for edge in selection) and number_adjacent_edges >= len(selection) * 2 
  
def is_adjacent(selection):
	vert_list = [edge.verts for edge in selection]
	common_vert = reduce(lambda x,y: list_intersection(x, y) , vert_list)
	return len(common_vert) == 1

def is_ring(selection):
	"""
	#Aproximation that should work 98% for now
	#Gets false positives when corners are selected like this: I_ or _I
	"""
	neightbour_Numbers = [edge for edge in selection if len([face for face in edge.link_faces if any(edge2 for edge2 in face.edges if edge2 in selection and edge2 != edge)]) > 0]
	return len(neightbour_Numbers) == len(selection)	

def split_edge_select_vert(ctx, change_selection = False):
	selection = get_selected(ctx, verts = True)
	bpy.ops.mesh.subdivide()
	if change_selection:
		new_selection = get_selected(ctx, verts = True)
		new_selection = list_difference(new_selection, selection)
		select_from_index(ctx, new_selection, verts = True,replace = True)
		ctx.scene.tool_settings.mesh_select_mode = [True,False,False]
	return new_selection
	 
def quad_fill(ctx):
	selection = get_selected(ctx, edges = True)
	bpy.ops.mesh.delete(type='FACE')
	select_from_index(ctx, selection, edges = True,replace = True)
	bpy.ops.mesh.fill_grid()

#make it smarter
def find_f2_verts(vert):
	vert_list = [edge.other_vert(vert[0]) for edge in vert[0].link_edges if is_border_vert(edge.other_vert(vert[0]))] + vert
	vert_list = list(filter(lambda x: is_border_vert(x) and is_corner_vert(x), vert_list))
	"""
	if vert_list == []:
		border_edges = list(filter(lambda x:is_border_edge(x),[edge for edge in vert_list[0].link_edges]))
		
		bpy.ops.mesh.loop_multi_select(ring=False)
		
		Assuming the verts it gets are border verts
		#1)get all verts in the loop
		#2)get all border and corner verts
		#3)for each filtered vert check if its a neightbour of any other vert that was filtered
		#4)select those instead
		
		return []
	else:
	"""
	return vert_list

def select_loop_directional(ctx, edge, directional = True, direction = 0):
	"""
		*Bugs: Improve selection of edges that dont have two faces
		Selects more than intended
	FEATURES:
		*Select border if the selection is in a border    
	"""
	counter = 0
	iterations = 0
	selection = [edge]
	# selected = selection
	new_selection = selection
	iterate = True
	directionality_loop = True
	mesh = get_bmesh(ctx)
	update_indexes(ctx, mesh, edges = True)
	while directionality_loop and counter < 2:
		while iterations < ITERATION_LIMIT and iterate:
			print("")
			print("----------------------------")
			print(iterations)
			print("Current Edge")
			print(selection)
			if direction == 0:
				new_selection = [selection[0].link_loops[0].link_loop_next.link_loop_radial_next.link_loop_next.edge]
			else:
				new_selection = [selection[0].link_loops[0].link_loop_prev.link_loop_radial_next.link_loop_prev.edge]
			if new_selection[0].select:
				print("CHANGE DIRECTION")
				if direction == 0:
					new_selection = [selection[0].link_loops[0].link_loop_prev.link_loop_radial_next.link_loop_prev.edge]
				else:
					new_selection = [selection[0].link_loops[0].link_loop_next.link_loop_radial_next.link_loop_next.edge]
				#Check if new selection is still selected after correcting direction
				if new_selection[0].select:
					print("COMPLETE LAP")
					iterate = False
			if len(list_intersection(list(new_selection[0].verts),list(selection[0].verts)))< 1:
				#Correct selection for cases where theres holes close by
				print("HOLES CLOSEBY, CORRECTING")
				new_selection = [selection[0].link_loops[0].link_loop_radial_next.link_loop_prev.link_loop_radial_next.link_loop_prev.edge]
			if len([face for face in new_selection[0].link_faces if (selection[0] in face.edges)]) > 0:  
				#Make sure you cant accidentally select a loop on top or below of it 
				print("LOOP WILL JUMP ROW")
				new_selection = selection
				iterate = False
			if len([face for face in new_selection[0].link_faces if len(list(face.verts)) != 4]) != 0:
				#End selection on ngons or triangles
				print("END LOOP")
				iterate = False
			selection = new_selection
			new_selection[0].select = True
			iterations += 1
		#If not directional reset and start the other way    
		if not directional:
			iterate = True
			iterations = 0
			direction = 1
			selection = [edge]
			new_selection = selection
		else:
			directionality_loop = False
		counter += 1

#Main Functions
"""
def smart_extrude():
	"Bevel edges before extruding"
	return True
"""

class MESH_OT_QuickSelectionVert(Operator):
	bl_idname = "mesh.quick_selection_vert"
	bl_label = "Quick Selection Vert"
	bl_description = "Set selection modes quickly"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, ctx):
		if ctx.mode == 'OBJECT':
			bpy.ops.object.editmode_toggle()
			if ctx.mode == 'EDIT_MESH':
				bpy.ops.mesh.select_mode('EXEC_DEFAULT', type='VERT')
		elif ctx.mode == 'EDIT_MESH':
			selectionMode = (tuple(ctx.scene.tool_settings.mesh_select_mode))
			if selectionMode[0]:
				bpy.ops.object.editmode_toggle()
			else:
				bpy.ops.mesh.select_mode('EXEC_DEFAULT', type='VERT')
		elif ctx.mode == 'EDIT_CURVE':
			bpy.ops.object.editmode_toggle() 
		return {'FINISHED'}

class MESH_OT_QuickSelectionEdge(Operator):
	bl_idname = "mesh.quick_selection_edge"
	bl_label = "Quick Selection Edge"
	bl_description = "Set selection modes quickly"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, ctx):
		if ctx.mode == 'OBJECT':
			bpy.ops.object.editmode_toggle()
			if ctx.mode == 'EDIT_MESH':
				bpy.ops.mesh.select_mode('EXEC_DEFAULT', type='EDGE') 
		elif ctx.mode == 'EDIT_MESH':
			selectionMode = (tuple(ctx.scene.tool_settings.mesh_select_mode))
			if selectionMode[1]:
				bpy.ops.object.editmode_toggle()
			else:
				bpy.ops.mesh.select_mode('EXEC_DEFAULT', type='EDGE') 
		elif ctx.mode == 'EDIT_CURVE':
			bpy.ops.object.editmode_toggle()
		return {'FINISHED'}

class MESH_OT_QuickSelectionFace(Operator):
	bl_idname = "mesh.quick_selection_face"
	bl_label = "Quick Selection Face"
	bl_description = "Set selection modes quickly"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self,ctx):
		if ctx.mode == 'OBJECT':
			bpy.ops.object.editmode_toggle()
			if ctx.mode == 'EDIT_MESH':
				bpy.ops.mesh.select_mode('EXEC_DEFAULT', type='FACE') 
		elif ctx.mode == 'EDIT_MESH':
			selectionMode = (tuple(ctx.scene.tool_settings.mesh_select_mode))
			if selectionMode[2]:
				bpy.ops.object.editmode_toggle()
			else:
				bpy.ops.mesh.select_mode('EXEC_DEFAULT', type='FACE')
		elif ctx.mode == 'EDIT_CURVE':
			bpy.ops.object.editmode_toggle() 
		return {'FINISHED'}

class MESH_OT_QuickSG(Operator):
	bl_idname = "mesh.quick_sg"
	bl_label = "Quick Smoothing Groups"
	bl_description = "Set edge sharpness quickly"
	bl_options = {'REGISTER', 'UNDO'}

	def quick_sg(self, ctx):
		if ctx.mode == 'OBJECT':
			bpy.ops.object.shade_smooth()
			ctx.object.data.use_auto_smooth = True
			ctx.object.data.auto_smooth_angle = 1.0472
		elif ctx.mode == 'EDIT_MESH':
			bm = get_bmesh(ctx)
			selectionMode = (tuple(ctx.scene.tool_settings.mesh_select_mode))
			#if Edge is selected
			if selectionMode[1]:
				selection = get_selected(ctx, edges = True, get_item = True)
				if all(edge.smooth is False for edge in selection):
					bpy.ops.mesh.region_to_loop()
					bpy.ops.mesh.mark_sharp(clear=True)
				else:
					bpy.ops.mesh.mark_sharp()
			#if Face is selected		   
			elif selectionMode[2]:
				selection = get_selected(ctx, faces = True, get_item = True)
				bpy.ops.mesh.mark_sharp(clear=True)
				bpy.ops.mesh.region_to_loop()
				bpy.ops.mesh.mark_sharp()
				select_from_item(ctx, selection, faces = True, replace = True)
				bpy.ops.mesh.select_mode('EXEC_DEFAULT', type='FACE') 
	
	def execute(self, ctx):
		self.quick_sg(ctx)
		return {'FINISHED'}

class MESH_OT_SetCylindricalObjSides(Operator):
	bl_idname = "mesh.set_cylindrical_sides"
	bl_label = "Set Cylindrical Object Sides"
	bl_description = "Select the ammount of sides for cylindrical object"
	bl_options = {'REGISTER', 'UNDO'}

	def set_cylindrical_obj_sides(self, ctx):
		selection = ctx.active_object
		print(selection)
		if ctx.object.modifiers.find("Cylindrical Sides") > -1:
			bpy.ops.wm.context_modal_mouse('INVOKE_DEFAULT',data_path_iter='selected_editable_objects', data_path_item='modifiers["Cylindrical Sides"].steps', input_scale=0.10000000149011612, header_text='Number of Sides %.f')
		elif ctx.mode == 'EDIT_MESH':
			bpy.ops.mesh.separate(type='SELECTED')
			new_selection = ctx.selected_objects
			mesh_to_select = list(filter(lambda x:x.name != selection.name, new_selection))
			bpy.ops.object.editmode_toggle()
			bpy.ops.object.select_all(action='DESELECT')
			bpy.data.objects[mesh_to_select[0].name].select_set(state=True)
			ctx.view_layer.objects.active = mesh_to_select[0]
			bpy.ops.object.modifier_add(type='SCREW')
			ctx.object.modifiers["Screw"].name = "Cylindrical Sides"
			ctx.object.modifiers["Cylindrical Sides"].use_merge_vertices = True
			ctx.object.modifiers["Cylindrical Sides"].use_normal_calculate = True
			bpy.ops.wm.context_modal_mouse('INVOKE_DEFAULT',data_path_iter='selected_editable_objects', data_path_item='modifiers["Cylindrical Sides"].steps', input_scale=0.10000000149011612, header_text='Number of Sides %.f')

	def execute(self, ctx):
		self.set_cylindrical_obj_sides(ctx)
		return {'FINISHED'}

class MESH_OT_SmartDelete(Operator):
	bl_idname = "mesh.smart_delete"
	bl_label = "Smart Delete"
	bl_description = "Context Sensitive Deletion"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def smart_delete(cls, ctx):
		if ctx.mode == 'OBJECT':
			bpy.ops.object.delete()
		elif ctx.mode == 'EDIT_MESH':
			bm = get_bmesh(ctx)
			selectionMode = (tuple(ctx.scene.tool_settings.mesh_select_mode))
			if selectionMode[0]:
				bpy.ops.mesh.delete(type='VERT')
			#if Edge is selected
			elif selectionMode[1]:
				selection = get_selected(ctx, edges = True, get_item = True)
				if is_border(selection):
					for edge in selection:
						for face in edge.link_faces:
							face.select = 1
					bpy.ops.mesh.delete(type='FACE')
				else:
					bpy.ops.mesh.dissolve_edges()
			elif selectionMode[2]:
			#if Face is selected
				bpy.ops.mesh.delete(type='FACE')
		elif ctx.mode == 'EDIT_CURVE':
			bpy.ops.curve.delete(type='VERT')

		return{'FINISHED'}

	def draw(self, ctx):
		pass

	def execute(self, ctx):
		self.smart_delete(ctx)
		return {'FINISHED'}

class MESH_OT_SmartFlow(Operator):
	bl_idname = "mesh.smart_flow"
	bl_label = "Smart Flow"
	bl_description = "Smart Edge Flow"
	bl_options = {'REGISTER', 'UNDO'}

	def smart_hard_ops(self, ctx):
		selectionMode = (tuple(ctx.scene.tool_settings.mesh_select_mode))
		#if Vertex is selected
		if selectionMode[0]:
			print("if a loop is selected then distance fix, else Relax")
		#if Edge is selected
		elif selectionMode[1]:
			print("If border is selected then draw crcle, If Loop is selected then do loop set flow. If ring is selected then do if")
		elif selectionMode[2]:
		#if Face is selected then flatten		   
			bpy.ops.mesh.inset('INVOKE_DEFAULT')

	def execute(self, ctx):
		self.smart_hard_ops(ctx)
		return{'FINISHED'}

class MESH_OT_CSBevel(Operator):
	bl_idname = "mesh.cs_bevel"
	bl_label = "CS Bevel"
	bl_description = "Context Sensitive Bevels and Inset"
	bl_options = {'REGISTER', 'UNDO'}

	def smart_hard_ops(self, ctx):
		selectionMode = (tuple(ctx.scene.tool_settings.mesh_select_mode))
		#if Vertex is selected
		if selectionMode[0]:
			bpy.ops.mesh.bevel('INVOKE_DEFAULT', vertex_only=True) 
		#if Edge is selected
		elif selectionMode[1]:
			bpy.ops.mesh.bevel('INVOKE_DEFAULT', vertex_only=False)  		  
		elif selectionMode[2]:
		#if Face is selected		   
			bpy.ops.mesh.inset('INVOKE_DEFAULT')

	def execute(self, ctx):
		self.smart_hard_ops(ctx)
		return{'FINISHED'}

class MESH_OT_SuperSmartCreate(Operator):
	bl_idname = "mesh.super_smart_create"
	bl_label = "Super Smart Create"
	bl_description = "Context sensitive creation"
	bl_options = {'REGISTER', 'UNDO'}

	def connect_verts_to_last(self, ctx, selection):
		bm = get_bmesh(ctx)
		ordered_selection = []
		for vert in selection:
			if vert not in bm.select_history:
				ordered_selection.append(vert)
		for item in bm.select_history:
			ordered_selection.append(item)
			print(item)
		for vert in ordered_selection:
			select_from_item(ctx, [vert,ordered_selection[-1]], verts = True, replace= True)
			bpy.ops.mesh.vert_connect()
		select_from_item(ctx, selection, verts = True, replace= True)

	def select_rings_inner_loop(self, ctx):
		new_selection = get_selected(ctx, edges = True, get_item = True)
		vert_list = [vert for edge in new_selection for vert in edge.verts]
		vert_list = list(filter(lambda x: len(list_intersection(x.link_edges,new_selection)) == 2, vert_list))
		new_selection = [edge for vert in vert_list for edge in vert.link_edges if edge not in new_selection]
		select_from_item(ctx, new_selection, edges = True, replace = True)

	def super_smart_create(self, ctx):
		bm = get_bmesh(ctx)
		selectionMode = (tuple(ctx.scene.tool_settings.mesh_select_mode))
		#if Vertex is selected
		if selectionMode[0]:
			selection = get_selected(ctx, verts = True, get_item = True)
			if len(selection) == 1 or (verts_share_edge(selection) and are_border_verts(selection)):
				mesh_f2.bpy.ops.mesh.f2('INVOKE_DEFAULT')
			elif verts_share_face(selection):
				self.connect_verts_to_last(ctx, selection)
			else:
				bpy.ops.mesh.vert_connect()
		#if Edge is selected
		elif selectionMode[1]:
			selection = get_selected(ctx, edges = True, get_item = True)
			if len(selection) == 1:
				split_edge_select_vert(ctx, change_selection = True) 					
			elif is_border(selection):
				bpy.ops.mesh.edge_face_add()
				ctx.scene.tool_settings.mesh_select_mode = [False,False,True]
			elif is_ring(selection):
				bpy.ops.mesh.subdivide_edgering(number_cuts=1,interpolation='LINEAR', profile_shape='LINEAR',smoothness = 0)
				self.select_rings_inner_loop(ctx)
			elif is_adjacent(selection):
				bpy.ops.mesh.edge_face_add()
				ctx.scene.tool_settings.mesh_select_mode = [False,True,False]
			else:
				bpy.ops.mesh.bridge_edge_loops()
				ctx.scene.tool_settings.mesh_select_mode = [False,True, False]
		#if Face is selected		   
		elif selectionMode[2]:
			selection = get_selected(ctx, faces = True, get_item = True)
			if len(selection) == 1:
				quad_fill(ctx)
			if len(selection) > 1:
				bpy.ops.mesh.bridge_edge_loops()

	def execute(self, ctx):
		self.super_smart_create(ctx)
		return{'FINISHED'}

class MESH_OT_SmartSelectLoop(Operator):
	"""
	BUGS:
	 *Step Face Loop only goes in one direction for faces
	"""
	bl_idname = "mesh.smart_select_loop"
	bl_label = "Smart Select Loop"
	bl_description = "Context sensitive smart loop selection"
	bl_options = {'REGISTER', 'UNDO'}

	def select_face_loops(self, ctx):
		bpy.ops.mesh.loop_multi_select(ring=False)
		ctx.tool_settings.mesh_select_mode = [False,True,False]
		bpy.ops.mesh.select_more()
		ctx.tool_settings.mesh_select_mode = [False,False,True]
		bpy.ops.mesh.select_less()

	def select_vert_loops(self, ctx):
		"Not sure it works correctly"
		bm = get_bmesh(ctx)
		vert = get_selected(ctx, verts = True)
		print(vert)
		edges=[]
		for edge in bm.verts[vert[0]].link_edges:
			print(edge.index)
			edges.append(edge.index)
		select_from_index(ctx, edges, edges=True)
		bpy.ops.mesh.loop_multi_select(ring=False)

	def distance_between_elements(self, ctx, element_a,element_b,verts = False, edges = False, faces = False, ring = False):
		if verts:
			sel_set = [True, False, False]
		elif edges:
			sel_set = [False, True, False]
		elif faces:
			sel_set = [False, False, True]
		select_from_index(ctx, [element_a,element_b], verts = sel_set[0], edges = sel_set[1], faces = sel_set[2], replace = True)
		bpy.ops.mesh.shortest_path_select()
		selection = get_selected(ctx, verts = sel_set[0], edges = sel_set[1], faces = sel_set[2])
		if ring:
			distance = len(selection)-3
		else:
			distance = len(selection)-2
		if distance > 0:
			return distance
		else:
			return 0 

	def organize_elements_by_loop(self, ctx, element_selection,verts = False, edges = False, faces = False):
		selected_elements = []
		elements_to_check = element_selection
		if verts:
			sel_set = [True, False, False]
		elif edges:
			sel_set = [False, True, False]
		elif faces:
			sel_set = [False, False, True]
		while len(elements_to_check) > 0:
			select_from_index(ctx, indexes = [elements_to_check[0]], verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2], replace = True)
			if verts:
				self.select_vert_loops(ctx)
			elif edges:
				bpy.ops.mesh.loop_multi_select(ring=False)
			elif faces:
				self.select_face_loops(ctx)
			element_loop = get_selected(ctx, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
			selected_elements.append(list_intersection(element_loop, elements_to_check))
			elements_to_check = list_difference(elements_to_check,element_loop)
		select_from_index(ctx, indexes =element_selection, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2], replace = True)
		return selected_elements

	def is_step_selection(self, ctx, elements_selection, verts = False, edges = False, faces = False):
		if verts:
			sel_set = [True, False, False]
		elif edges:
			sel_set = [False, True, False]
		elif faces:
			sel_set = [False, False, True]
		if len(elements_selection)>2:
			# selection_results = []
			results = []
			for element_a in elements_selection:
				min = []
				other_elements = list_difference(elements_selection,[element_a])
				for element_b in other_elements:
					distance = self.distance_between_elements(ctx, element_a,element_b, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
					if len(min) == 0 or min[1] > distance: 
						min = [list(set([element_a,element_b])),distance]
				results.append(min)
			results = list(results for results,_ in itertools.groupby(results))
			if len(list(set(list(map(lambda x: x[1], results))))) == 1:
				#print(results[0][0])
				return [True,results[0][0]]
			else:
				return [False,[]]
		else:
			return [False,[]]

	def complete_step_selection(self, ctx, verts = False, edges = False, faces = False):
		iteration = 0
		last_selection = []
		if verts:
			sel_set = [True, False, False]
		elif edges:
				sel_set = [False, True, False]
		elif faces:
			sel_set = [False, False, True]
		selected_elements = get_selected(ctx, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
		while not selected_elements == last_selection and iteration < ITERATION_LIMIT:
			bpy.ops.mesh.select_next_item()
			last_selection = selected_elements
			selected_elements = get_selected(ctx, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
			iteration += 1

	def smart_loop(self, ctx):
		#print("")
		selectionMode = (tuple(ctx.scene.tool_settings.mesh_select_mode))
		if selectionMode[0]:
			sel_set = [True, False, False]
		elif selectionMode[1]:
				sel_set = [False, True, False]
		elif selectionMode[2]:
			sel_set = [False, False, True]
		final_selection = []
		selection = get_selected(ctx, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
		#print(organize_elements_by_loop(ctx, selection,verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2]))
		for loop in self.organize_elements_by_loop(ctx, selection,verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2]):
			step_selection_result = self.is_step_selection(ctx, loop, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
			#print(step_selection_result)
			if step_selection_result[0]: 
				select_from_index(ctx, step_selection_result[1], verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2], replace = True, add_to_history = True)         
				self.complete_step_selection(ctx, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
			elif len(loop) == 2:
				if self.distance_between_elements(ctx, loop[0],loop[1], verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2]) > 0:
					select_from_index(ctx, loop, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2], replace = True, add_to_history = True)
					bpy.ops.mesh.shortest_path_select()
				elif self.distance_between_elements(ctx, loop[0],loop[1], verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2]) == 0:
					select_from_index(ctx, loop, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2], replace = True, add_to_history = True)
					self.complete_step_selection(ctx, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
			else:
				if selectionMode[1] == True: 
					select_from_index(ctx, loop, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2], replace = True, add_to_history = True)
					bpy.ops.mesh.loop_multi_select(ring=False)
			final_selection += get_selected(ctx, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
			#print(final_selection)
		select_from_index(ctx, final_selection, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2], replace = True, add_to_history = True)

	def execute(self, ctx):
		self.smart_loop(ctx)
		return{'FINISHED'}

class MESH_OT_SmartSelectRing(Operator):
	"""
	BUGS:
	 *Step Face Loop only goes in one direction for faces
	"""
	bl_idname = "mesh.smart_select_ring"
	bl_label = "Smart Select Ring"
	bl_description = "Context sensitive smart ring selection"
	bl_options = {'REGISTER', 'UNDO'}

	def select_face_rings(self, ctx):
		bpy.ops.mesh.loop_multi_select(ring=True)
		ctx.tool_settings.mesh_select_mode = [False,True,False]
		bpy.ops.mesh.select_more()
		ctx.tool_settings.mesh_select_mode = [False,False,True]
		bpy.ops.mesh.select_less()

	def select_vert_rings(self, ctx):
		"Not sure it works correctly"
		bm = get_bmesh(ctx)
		vert = get_selected(ctx, verts = True)
		print(vert)
		edges=[]
		for edge in bm.verts[vert[0]].link_edges:
			print(edge.index)
			edges.append(edge.index)
		select_from_index(ctx, edges, edges=True)
		bpy.ops.mesh.loop_multi_select(ring=True)

	def distance_between_elements(self, ctx, element_a,element_b,verts = False, edges = False, faces = False, ring = False):
		if verts:
			sel_set = [True, False, False]
		elif edges:
			sel_set = [False, True, False]
		elif faces:
			sel_set = [False, False, True]
		select_from_index(ctx, [element_a,element_b], verts = sel_set[0], edges = sel_set[1], faces = sel_set[2], replace = True)
		bpy.ops.mesh.shortest_path_select()
		selection = get_selected(ctx, verts = sel_set[0], edges = sel_set[1], faces = sel_set[2])
		if ring:
			distance = len(selection)-3
		else:
			distance = len(selection)-2
		if distance > 0:
			return distance
		else:
			return 0 

	def organize_elements_by_ring(self, ctx, element_selection,verts = False, edges = False, faces = False):
		selected_elements = []
		elements_to_check = element_selection
		if verts:
			sel_set = [True, False, False]
		elif edges:
			sel_set = [False, True, False]
		elif faces:
			sel_set = [False, False, True]
		while len(elements_to_check) > 0:
			select_from_index(ctx, indexes = [elements_to_check[0]], verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2], replace = True)
			if verts:
				self.select_vert_rings(ctx)
			elif edges:
				bpy.ops.mesh.loop_multi_select(ring=True)
			elif faces:
				self.select_face_rings(ctx)
			element_loop = get_selected(ctx, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
			selected_elements.append(list_intersection(element_loop, elements_to_check))
			elements_to_check = list_difference(elements_to_check,element_loop)
		select_from_index(ctx, indexes =element_selection, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2], replace = True)
		return selected_elements

	def is_step_selection(self, ctx, elements_selection, verts = False, edges = False, faces = False):
		if verts:
			sel_set = [True, False, False]
		elif edges:
			sel_set = [False, True, False]
		elif faces:
			sel_set = [False, False, True]
		if len(elements_selection)>2:
			# selection_results = []
			results = []
			for element_a in elements_selection:
				min = []
				other_elements = list_difference(elements_selection,[element_a])
				for element_b in other_elements:
					distance = self.distance_between_elements(ctx, element_a,element_b, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2], ring = True)
					if len(min) == 0 or min[1] > distance: 
						min = [list(set([element_a,element_b])),distance]
				results.append(min)
			results = list(results for results,_ in itertools.groupby(results))
			if len(list(set(list(map(lambda x: x[1], results))))) == 1:
				return [True,results[0][0]]
			else:
				return [False,[]]
		else:
			return [False,[]]

	def complete_step_selection(self, ctx, verts = False, edges = False, faces = False):
		iteration = 0
		last_selection = []
		if verts:
			sel_set = [True, False, False]
		elif edges:
				sel_set = [False, True, False]
		elif faces:
			sel_set = [False, False, True]
		selected_elements = get_selected(ctx, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
		while not selected_elements == last_selection and iteration < ITERATION_LIMIT:
			bpy.ops.mesh.select_next_item()
			last_selection = selected_elements
			selected_elements = get_selected(ctx, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
			iteration += 1

	def smart_ring(self, ctx):
		#print("")
		selectionMode = (tuple(ctx.scene.tool_settings.mesh_select_mode))
		if selectionMode[0]:
			sel_set = [True, False, False]
		elif selectionMode[1]:
				sel_set = [False, True, False]
		elif selectionMode[2]:
			sel_set = [False, False, True]
		final_selection = []
		selection =  get_selected(ctx, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
		#print(organize_elements_by_loop(ctx, selection,verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2]))
		for loop in self.organize_elements_by_ring(ctx, selection,verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2]):
			step_selection_result = self.is_step_selection(ctx, loop, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
			print(step_selection_result)
			if step_selection_result[0]: 
				select_from_index(ctx, step_selection_result[1], verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2], replace = True, add_to_history = True)         
				self.complete_step_selection(ctx, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
			elif len(loop) == 2:
				if self.distance_between_elements(ctx, loop[0],loop[1], verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2]) > 0:
					select_from_index(ctx, loop, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2], replace = True, add_to_history = True)
					bpy.ops.mesh.shortest_path_select(use_face_step=True)
				elif self.distance_between_elements(ctx, loop[0],loop[1], verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2]) == 0:
					select_from_index(ctx, loop, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2], replace = True, add_to_history = True)
					self.complete_step_selection(ctx, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
			else:
				if selectionMode[1] == True: 
					select_from_index(ctx, loop, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2], replace = True, add_to_history = True)
					bpy.ops.mesh.loop_multi_select(ring=True)
			final_selection += get_selected(ctx, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
			#print(final_selection)
		select_from_index(ctx, final_selection, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2], replace = True, add_to_history = True)

	def execute(self, ctx):
		self.smart_ring(ctx)
		return{'FINISHED'}

class MESH_OT_QuickPivot(Operator):
	bl_idname = "mesh.quick_pivot"
	bl_label = "Quick Pivot Setup"
	bl_description = "Quick Pivot Setup based on selection"
	bl_options = {'REGISTER', 'UNDO'}
	
	def quick_pivot(self, ctx):
		if ctx.mode == 'OBJECT':
			bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
		elif ctx.mode == 'EDIT_MESH':
			cl = ctx.scene.cursor.location
			pos2 = (cl[0],cl[1],cl[2])
			bpy.ops.view3d.snap_cursor_to_selected()
			bpy.ops.object.editmode_toggle()
			bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
			bpy.ops.object.editmode_toggle()
			ctx.scene.cursor.location = (pos2[0],pos2[1],pos2[2])
	
	def execute(self, ctx):
		self.quick_pivot(ctx)
		return{'FINISHED'}

class MESH_OT_SimpleEditPivot(Operator):
	bl_idname = "mesh.simple_edit_pivot"
	bl_label = "Simple Edit Pivot"
	bl_description = "Edit pivot position and scale"
	bl_options = {'REGISTER', 'UNDO'}

	def create_pivot(self, ctx, obj):
		bpy.ops.object.empty_add(type='ARROWS', location= obj.location)
		pivot = ctx.active_object
		pivot.name = obj.name + ".PivotHelper"
		pivot.location = obj.location
		print("Pivot")

	def get_pivot(self, ctx, obj):
		pivot = obj.name + ".PivotHelper"
		if bpy.data.objects.get(pivot) is None:
			return False
		else:
			bpy.data.objects[obj.name].select_set(False)
			bpy.data.objects[pivot].select_set(True)
			ctx.view_layer.objects.active = bpy.data.objects[pivot]
			return True

	def apply_pivot(self, ctx, pivot):
		obj = bpy.data.objects[pivot.name[:-12]]
		piv_loc = pivot.location
		#I need to create piv as it seem like the pivot location is passed by reference? Still no idea why this happens
		cl = ctx.scene.cursor.location
		piv = (cl[0],cl[1],cl[2])
		ctx.scene.cursor.location = piv_loc
		ctx.view_layer.objects.active = obj
		bpy.data.objects[obj.name].select_set(True)
		bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
		ctx.scene.cursor.location = (piv[0],piv[1],piv[2])
		#Select pivot, delete it and select obj again
		bpy.data.objects[obj.name].select_set(False)
		bpy.data.objects[pivot.name].select_set(True)
		bpy.ops.object.delete()
		bpy.data.objects[obj.name].select_set(True)
		ctx.view_layer.objects.active = obj

	def execute(self, ctx):
		obj = ctx.active_object
		if  obj.name.endswith(".PivotHelper"):
			self.apply_pivot(ctx, obj)
		elif self.get_pivot(ctx, obj):
			piv = ctx.active_object
		else:
			self.create_pivot(ctx,obj)
		return{'FINISHED'}

class MESH_OT_QuickModifierToggle(Operator):
	bl_idname = "mesh.modifier_toggle"
	bl_label = "Modifier Toggle"
	bl_description = "Toggles the modifiers on and off for selected objects"
	bl_options = {'REGISTER', 'UNDO'}

	def modifier_toggle(self, ctx):
		for obj in ctx.selected_objects:
			if all(modifier.show_in_editmode and modifier.show_viewport for modifier in obj.modifiers):
				for modifier in obj.modifiers:
					modifier.show_in_editmode = False
					modifier.show_viewport = False
			else:
				for modifier in obj.modifiers:
					modifier.show_in_editmode = True
					modifier.show_viewport = True
	
	def execute(self,ctx):
		self.modifier_toggle(ctx)
		return {'FINISHED'}

class MESH_OT_QuickWireToggle(Operator):
	bl_idname = "mesh.wire_toggle"
	bl_label = "Quick Wire Toggle"
	bl_description = "Toggles wire mode on and off on all objects"
	bl_options = {'REGISTER', 'UNDO'}

	def wire_toggle(self, ctx):
		if ctx.space_data.overlay.show_wireframes:
			ctx.space_data.overlay.show_wireframes = False
		else:
			ctx.space_data.overlay.show_wireframes = True

	def execute(self, ctx):
		self.wire_toggle(ctx)
		return{'FINISHED'}

class MESH_OT_WireShadedToggle(Operator):
	bl_idname = "mesh.wire_shaded_toggle"
	bl_label = "Wireframe / Shaded Toggle"
	bl_description = "Toggles between wireframe and shaded mode"
	bl_options = {'REGISTER', 'UNDO'}

	def wire_shaded_toggle(self, ctx):
		areas = ctx.workspace.screens[0].areas
		for area in areas:
			for space in area.spaces:
				if space.type == 'VIEW_3D':
					if space.shading.type == 'WIREFRAME':
						space.shading.type = 'SOLID'
					else:
						space.shading.type = 'WIREFRAME'

	def execute(self, ctx):
		self.wire_shaded_toggle(ctx)
		return{'FINISHED'}

class MESH_OT_TargetWeldToggle(Operator):
	bl_idname = "mesh.target_weld_toggle"
	bl_label = "Target Weld Toggle"
	bl_description = "Toggles snap to vertex and automerge editing on and off"
	bl_options = {'REGISTER', 'UNDO'}

	def toggle_target_weld(self, ctx):
		if ctx.scene.tool_settings.use_mesh_automerge and ctx.scene.tool_settings.use_snap:
			ctx.scene.tool_settings.use_mesh_automerge = False
			ctx.scene.tool_settings.use_snap = False
		else:
			ctx.scene.tool_settings.snap_elements |=  {'VERTEX'}
			ctx.scene.tool_settings.use_mesh_automerge = True
			ctx.scene.tool_settings.use_snap = True

	def execute(self, ctx):
		self.toggle_target_weld(ctx)
		return{'FINISHED'}

class MESH_OT_ContextSensitiveSlide(Operator):
	bl_idname = "mesh.context_sensitive_slide"
	bl_label = "Context Sensitive Slide"
	bl_description = "Slide vert or edge based on selection"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, ctx):
		bm = get_bmesh(ctx)
		selectionMode = (tuple(ctx.scene.tool_settings.mesh_select_mode))
		if selectionMode[0]:
			bpy.ops.transform.vert_slide('INVOKE_DEFAULT')
		elif selectionMode[1]:
			bpy.ops.transform.edge_slide('INVOKE_DEFAULT')
		return{'FINISHED'}

class MESH_OT_QuickRadialSymmetry(Operator):
	bl_idname = "mesh.radial_symmetry"
	bl_label = "Quick Radial Symmetry"
	bl_description = "Setup a Quick Radial Symmetry"
	bl_options = {'REGISTER', 'UNDO'}

	mouseX = 0.0
	initial_pos_x = 0.0
	sym_count = 0.0
	sym_axis = 0
	initial_sym_axis = 0
	initial_sym_count = 0
	offset_obj = "Empty"
	selection = "Empty"
	senitivity = 0.01
	modkey = 0

	def setup_symmetry(self, ctx, selection):
		if selection is not []:
			sel_pivot = selection.location
			bpy.ops.object.empty_add(type='ARROWS', location=sel_pivot)
			symmetry_center = ctx.active_object
			#symmetry_center.hide_viewport = True
			symmetry_center.rotation_euler = (0, 0, math.radians(120))
			symmetry_center.name = selection.name + ".SymmetryPivot"
			print(symmetry_center.name)
			ctx.view_layer.objects.active = selection
			bpy.ops.object.modifier_add(type='ARRAY')
			selection.modifiers["Array"].name = "Radial Symmetry"
			selection.modifiers["Radial Symmetry"].relative_offset_displace[0] = 0
			selection.modifiers["Radial Symmetry"].count = 3
			selection.modifiers["Radial Symmetry"].offset_object = bpy.data.objects[symmetry_center.name]
			selection.modifiers["Radial Symmetry"].use_object_offset = True
		else:
			print("Select 1 object to create radial symmetry")

	def calculate_iterations(self, ctx, event, selection):
		self.mouse_x = event.mouse_x
		self.sym_count = self.initial_sym_count + int(((self.mouse_x - self.initial_pos_x) * self.senitivity))
		if self.sym_count < 1:
			self.sym_count = 1
			self.initial_pos_x = self.mouse_x
		self.selection.modifiers["Radial Symmetry"].count = self.sym_count
	
	def calculate_axis(self, ctx, event, selection):
		self.mouse_x = event.mouse_x
		self.sym_axis = int((self.initial_sym_axis  + (self.mouse_x - self.initial_pos_x) * self.senitivity ) % 3)
	
	def calculate_rotation(self, axis, selection):
		if axis == 0:
			self.offset_obj.rotation_euler = (math.radians(360/ self.sym_count), 0, 0)	
		elif axis == 1:
			self.offset_obj.rotation_euler = (0 , math.radians(360/ self.sym_count), 0)
		elif axis == 2:
			self.offset_obj.rotation_euler = (0,0,math.radians(360/ self.sym_count))

	def recover_settings(self, ctx, selection):
		self.initial_sym_count = selection.modifiers["Radial Symmetry"].count 
		self.offset_obj = selection.modifiers["Radial Symmetry"].offset_object
		rotation = selection.modifiers["Radial Symmetry"].offset_object.rotation_euler
		if rotation[0] > 0:
			self.initial_sym_axis = 0
		elif rotation[1] > 0:
			self.initial_sym_axis = 1
		elif rotation[2] > 0:
			self.initial_sym_axis = 2
		self.sym_axis = self.initial_sym_axis
		self.sym_count = self.initial_sym_count

	def __init__(self):
		print("Start")

	def __del__(self):
		print("End")

	def execute(self, ctx):
		return{'FINISHED'}

	def modal(self, ctx, event):
		if event.type == 'MOUSEMOVE':  # Apply
			if event.ctrl:
				if self.modkey != 1:
					self.modkey = 1
					self.initial_pos_x = event.mouse_x
					self.initial_sym_count = self.sym_count 
				self.calculate_axis(ctx, event, self.selection)
			else:
				if self.modkey != 0:
					self.modkey = 0
					self.initial_pos_x = event.mouse_x
					self.initial_sym_axis = self.sym_axis
				self.calculate_iterations(ctx, event, self.selection)
			self.calculate_rotation(self.sym_axis, self.selection)


		elif event.type == 'LEFTMOUSE':  # Confirm
			if event.value == 'RELEASE':
 				return {'FINISHED'}
		elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Confirm
			return {'CANCELLED'}
		return {'RUNNING_MODAL'}
	
	def invoke(self, ctx, event):
		self.initial_pos_x = event.mouse_x
		self.selection = ctx.active_object
		if self.selection.modifiers.find("Radial Symmetry") < 0:
			self.setup_symmetry(ctx, self.selection)
		self.recover_settings(ctx, self.selection)
		self.execute(ctx)
		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}

class MESH_OT_SmartExtrude(Operator):
	bl_idname = "mesh.smart_extrude_modal"
	bl_label = "Smart Extrude Modal"
	bl_description = "Context Sensitive Extrude operation"
	bl_options = {'REGISTER', 'UNDO'}

	initial_mouse_pos = Vector((0,0,0))
	translation_accumulator = Vector((0,0,0))
	initial_pos = Vector((0,0,0))
	sensitivity = 1

	def mouse_2d_to_3d(self, ctx, event):
		x, y = event.mouse_region_x, event.mouse_region_y
		location = region_2d_to_location_3d(ctx.region, ctx.space_data.region_3d, (x,y), (0,0,0))
		return Vector(location)

	#Not Needed, delete later
	def get_verts_center(self, ctx):
		# bm = get_bmesh(ctx)
		obj = ctx.active_object
		selectionMode = (tuple(ctx.scene.tool_settings.mesh_select_mode))
		if selectionMode[0]:
			verts = get_selected(ctx, verts=True, get_item = True)
		elif selectionMode[1]:
			edges = get_selected(ctx, edges=True, get_item = True)
			verts = [edge.verts for edge in edges]
			verts = [vert for vert_pair in verts for vert in vert_pair]
			verts = list(set(verts))
		elif selectionMode[2]:
			faces = get_selected(ctx, faces=True, get_item = True)
			verts = [face.verts for face in faces]
			verts = [vert for vert_pair in verts for vert in vert_pair]
			verts = list(set(verts))
		verts_center = reduce(lambda x, y: x + y, [obj.matrix_world @ vert.co for vert in verts]) 
		#verts_center = reduce(lambda x, y: x + y, [vert.co for vert in verts]) 
		verts_center /= len(verts)
		return verts_center

	def calculate_translation(self, ctx, event):
		translation = Vector((0,0,0))
		for area in ctx.screen.areas:
			if area.type == "VIEW_3D":
				new_mouse_pos = self.mouse_2d_to_3d(ctx, event)
			else:
				new_mouse_pos = self.initial_mouse_pos
		increment = (new_mouse_pos - self.initial_mouse_pos) * self.sensitivity
		increment_abs = [abs(value) for value in increment]
		axis = list(increment_abs).index(max(increment_abs))
		if axis == 0:
			translation[0] = increment[0] - self.translation_accumulator[0]
			translation[1] = -self.translation_accumulator[1] 
			translation[2] = -self.translation_accumulator[2] 
		elif axis == 1:
			translation[0] = -self.translation_accumulator[0]  
			translation[1] = increment[1] - self.translation_accumulator[1]
			translation[2] = -self.translation_accumulator[2] 
		elif axis == 2:
			translation[0] = -self.translation_accumulator[0] 
			translation[1] = -self.translation_accumulator[1] 
			translation[2] = increment[2] - self.translation_accumulator[2]

		#Debug
		"""
		print("INITIAL VERT POS : %s" % (self.initial_pos))
		print("INITIAL MOUSE POS : %s " % (self.initial_mouse_pos))
		print("NEW MOUSE POS : %s " % (new_mouse_pos))
		print("INCREMENT : %s " % (increment))
		print("ACCUMULATOR : %s " % (self.translation_accumulator))
		print("TRANSLATION: %s " % (translation))
		"""
		self.translation_accumulator += translation 
		bpy.ops.transform.translate(value = translation, orient_type = 'GLOBAL')
		return True

	def calculate_rotation(self, ctx, event):
		translation = Vector((0,0,0))
		for area in ctx.screen.areas:
			if area.type == "VIEW_3D":
				new_mouse_pos = self.mouse_2d_to_3d(ctx, event)
			else:
				new_mouse_pos = self.initial_mouse_pos
		increment = (new_mouse_pos - self.initial_mouse_pos) * self.sensitivity * 0.1
		increment_abs = [abs(value) for value in increment]
		axis = list(increment_abs).index(max(increment_abs))
		if axis == 0:
			translation[0] = increment[0] - self.translation_accumulator[0]
			translation[1] = -self.translation_accumulator[1] 
			translation[2] = -self.translation_accumulator[2] 
			rot_axis = 'X'
			translation_axis = increment[0] - self.translation_accumulator[0]
		elif axis == 1:
			translation[0] = -self.translation_accumulator[0]  
			translation[1] = increment[1] - self.translation_accumulator[1]
			translation[2] = -self.translation_accumulator[2] 
			rot_axis = 'Y'
			translation_axis = increment[1] - self.translation_accumulator[1]
		elif axis == 2:
			translation[0] = -self.translation_accumulator[0] 
			translation[1] = -self.translation_accumulator[1] 
			translation[2] = increment[2] - self.translation_accumulator[2]
			rot_axis = 'Z'
			translation_axis = increment[2] - self.translation_accumulator[2]
		self.translation_accumulator += translation 
		bpy.ops.transform.rotate(value = translation_axis, axis =  rot_axis,orient_type = 'GLOBAL')
		return True

	def context_sensitive_extend(self, ctx):
		if ctx.mode == 'OBJECT':
			if len(ctx.selected_objects) > 0:
				initial_pos = ctx.selected_objects[0].location
				bpy.ops.object.duplicate()
			else:
				return {'FINISHED'}
		
		elif ctx.mode == 'EDIT_MESH':
			bm = get_bmesh(ctx)
			selectionMode = (tuple(ctx.scene.tool_settings.mesh_select_mode))
			if selectionMode[1]:
				selection = get_selected(ctx, edges = True, get_item = True)
				if all(is_border_edge(edge) for edge in selection):
					bpy.ops.mesh.extrude_edges_move(MESH_OT_extrude_edges_indiv=None, TRANSFORM_OT_translate=None)
				else:
					return {'FINISHED'}
			else:
				bpy.ops.mesh.duplicate(mode=1)
		elif ctx.mode == 'EDIT_CURVE':
			bpy.ops.curve.extrude_move(CURVE_OT_extrude={"mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
			print("Curve")
			#self.initial_pos = self.get_verts_center(ctx)

	def __init__(self):
		self.initial_mouse_pos = Vector((0,0,0))
		self.translation_accumulator = Vector((0,0,0))
		self.initial_pos = Vector((0,0,0))
		print("Start")

	def __del__(self):
		print("End")

	def execute(self, ctx):
		return {'FINISHED'}

	def modal(self, ctx, event):
		if event.type == 'MOUSEMOVE':  # Apply
			self.calculate_translation(ctx, event)
			self.execute(ctx)
		elif event.type == 'LEFTMOUSE':  # Confirm
			if event.value == 'RELEASE':
 				return {'FINISHED'}
		elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Confirm
			bpy.ops.transform.translate(value = (Vector((0,0,0)) - self.translation_accumulator), orient_type = 'GLOBAL')
			SmartDelete.smart_delete(ctx)
			return {'CANCELLED'}
		return {'RUNNING_MODAL'}
			
	def invoke(self, ctx, event):
		self.initial_mouse_pos = self.mouse_2d_to_3d(ctx, event)
		self.context_sensitive_extend(ctx)
		self.execute(ctx)
		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}

class MESH_OT_SmartTranslate(Operator):
	bl_idname = "mesh.smart_translate_modal"
	bl_label = "Smart Translate"
	bl_description = "Smart Translate Tool"
	bl_options = {'REGISTER', 'UNDO'}

	initial_mouse_pos = Vector((0,0,0))
	translation_accumulator = Vector((0,0,0))
	initial_pos = Vector((0,0,0))
	sensitivity = 1

	def mouse_2d_to_3d(self,ctx, event):
		x, y = event.mouse_region_x, event.mouse_region_y
		location = region_2d_to_location_3d(ctx.region, ctx.space_data.region_3d, (x, y), (0, 0, 0))
		return Vector(location)

	def calculate_translation(self, ctx, event):
		translation = Vector((0,0,0))
		for area in ctx.screen.areas:
			if area.type == "VIEW_3D":
				new_mouse_pos = self.mouse_2d_to_3d(ctx, event)
			else:
				new_mouse_pos = self.initial_mouse_pos
		increment = (new_mouse_pos - self.initial_mouse_pos) * self.sensitivity
		increment_abs = [abs(value) for value in increment]
		axis = list(increment_abs).index(max(increment_abs))
		if axis == 0:
			translation[0] = increment[0] - self.translation_accumulator[0]
			translation[1] = -self.translation_accumulator[1] 
			translation[2] = -self.translation_accumulator[2] 
		elif axis == 1:
			translation[0] = -self.translation_accumulator[0]  
			translation[1] = increment[1] - self.translation_accumulator[1]
			translation[2] = -self.translation_accumulator[2] 
		elif axis == 2:
			translation[0] = -self.translation_accumulator[0] 
			translation[1] = -self.translation_accumulator[1] 
			translation[2] = increment[2] - self.translation_accumulator[2]
		self.translation_accumulator += translation 
		bpy.ops.transform.translate(value = translation, orient_type = 'GLOBAL')
		return True

	def calculate_rotation(self, ctx, event):
		translation = Vector((0,0,0))
		for area in ctx.screen.areas:
			if area.type == "VIEW_3D":
				new_mouse_pos = self.mouse_2d_to_3d(ctx, event)
			else:
				new_mouse_pos = self.initial_mouse_pos
		increment = (new_mouse_pos - self.initial_mouse_pos) * self.sensitivity * 0.1
		increment_abs = [abs(value) for value in increment]
		axis = list(increment_abs).index(max(increment_abs))
		if axis == 0:
			translation[0] = increment[0] - self.translation_accumulator[0]
			translation[1] = -self.translation_accumulator[1] 
			translation[2] = -self.translation_accumulator[2] 
			rot_axis = 'Y'
			translation_axis = increment[0] - self.translation_accumulator[0]
		elif axis == 1:
			translation[0] = -self.translation_accumulator[0]  
			translation[1] = increment[1] - self.translation_accumulator[1]
			translation[2] = -self.translation_accumulator[2] 
			rot_axis = 'Z'
			translation_axis = increment[1] - self.translation_accumulator[1]
		elif axis == 2:
			translation[0] = -self.translation_accumulator[0] 
			translation[1] = -self.translation_accumulator[1] 
			translation[2] = increment[2] - self.translation_accumulator[2]
			rot_axis = 'X'
			translation_axis = increment[2] - self.translation_accumulator[2]
		self.translation_accumulator += translation
		bpy.ops.transform.rotate(value = translation[0], orient_axis =  'X',orient_type = 'GLOBAL')
		bpy.ops.transform.rotate(value = translation[1], orient_axis =  'Z',orient_type = 'GLOBAL') 
		bpy.ops.transform.rotate(value = translation[2], orient_axis =  'Y',orient_type = 'GLOBAL')
		return True

	def __init__(self):
		self.initial_mouse_pos = Vector((0,0,0))
		self.translation_accumulator = Vector((0,0,0))
		self.initial_pos = Vector((0,0,0))
		print("Start")

	def __del__(self):
		print("End")

	def execute(self, ctx):
		return {'FINISHED'}

	def modal(self, ctx, event):
		if event.type == 'MOUSEMOVE':  # Apply
			self.calculate_translation(ctx, event)
			self.execute(ctx)
		elif event.type == 'MIDDLEMOUSE':  # Confirm
			if event.value == 'RELEASE':
 				return {'FINISHED'}
		elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Confirm
			bpy.ops.transform.translate(value = - self.translation_accumulator, orient_type = 'GLOBAL')
			return {'CANCELLED'}
		return {'RUNNING_MODAL'}
			
	def invoke(self, ctx, event):
		self.initial_mouse_pos = self.mouse_2d_to_3d(ctx, event)
		self.execute(ctx)
		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}

class MESH_OT_QuickFFD(Operator):
	bl_idname = "mesh.quick_ffd"
	bl_label = "Quick FFD"
	bl_description = "Setup a Quick FFD"
	bl_options = {'REGISTER', 'UNDO'}

	mouseX = 0.0
	initial_pos_x = 0.0
	sym_count = 0.0
	sym_axis = 0
	initial_sym_axis = 0
	initial_sym_count = 0
	offset_obj = "Empty"
	selection = "Empty"
	senitivity = 0.01
	modkey = 0

	def setup_ffd(self, ctx, selection):
		if selection is not []:
			if ctx.mode == 'OBJECT':
				verts = selection.data.vertices
				vert_positions = [vert.co @ selection.matrix_world for vert in verts] 
				rotation = bpy.data.objects[selection.name].rotation_euler
			elif ctx.mode == 'EDIT_MESH':
				bmesh = get_bmesh(ctx)
				minimum = Vector()
				maximum = Vector()
				selectionMode = (tuple(ctx.scene.tool_settings.mesh_select_mode))
				if selectionMode[0]:
					verts = get_selected(ctx, verts=True, get_item = True)
				elif selectionMode[1]:
					edges = get_selected(ctx, edges=True, get_item = True)
					verts = [edge.verts for edge in edges]
					verts = [vert for vert_pair in verts for vert in vert_pair]
					verts = list(set(verts))
				elif selectionMode[2]:
					faces = get_selected(ctx, faces=True, get_item = True)
					verts = [face.verts for face in faces]
					verts = [vert for vert_pair in verts for vert in vert_pair]
					verts = list(set(verts))
				vert_positions = [(selection.matrix_world @ vert.co) for vert in verts]
				#Make vertex group
				selection.vertex_groups.new(name = "ffd_group")
				bpy.ops.object.vertex_group_assign()
				rotation = Vector()
				bpy.ops.object.editmode_toggle()
			#calculate positions
			minimum = Vector()
			maximum = Vector()
			for axis in range(3):
				poslist = [pos[axis] for pos in vert_positions]
				maximum[axis] = max(poslist)
				minimum[axis] = min(poslist)
			location = (maximum + minimum) / 2 
			dimensions = maximum - minimum
			#add lattice			
			bpy.ops.object.add(type='LATTICE', enter_editmode=False, location=(0, 0, 0))
			ffd = ctx.active_object
			ffd.data.use_outside = True
			ffd.name = selection.name + ".Lattice"
			ffd.data.interpolation_type_u = 'KEY_LINEAR'
			ffd.data.interpolation_type_v = 'KEY_LINEAR'
			ffd.data.interpolation_type_w = 'KEY_LINEAR'
			ffd.location = location
			ffd.scale = dimensions
			ffd.rotation_euler = rotation
			ctx.view_layer.objects.active = selection
			bpy.ops.object.modifier_add(type='LATTICE')
			selection.modifiers["Lattice"].object = ffd
			selection.modifiers["Lattice"].vertex_group = "ffd_group"
			ctx.view_layer.objects.active = ffd
			#Deselect obj, select FFD and make it active, switch to edit mode
			bpy.data.objects[selection.name].select_set(False)
			bpy.data.objects[ffd.name].select_set(True)
			bpy.ops.object.editmode_toggle()

	def apply_ffd(self, ctx, ffd):
		if ctx.mode == 'EDIT_MESH':
			bpy.ops.object.editmode_toggle()
		obj = bpy.data.objects[ffd.name[:-8]]
		bpy.data.objects[ffd.name].select_set(False)
		bpy.data.objects[obj.name].select_set(True)
		ctx.view_layer.objects.active = obj
		bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Lattice")
		#Delete vertex group
		vg = obj.vertex_groups.get("ffd_group")
		if vg is not None:
			obj.vertex_groups.remove(vg)
		#Delete lattice
		bpy.data.objects[obj.name].select_set(False)
		bpy.data.objects[ffd.name].select_set(True)
		bpy.ops.object.delete()
		bpy.data.objects[obj.name].select_set(True)
		bpy.ops.object.editmode_toggle()

	def get_ffd(self, ctx, obj):
		ffd = obj.name + ".Lattice"
		if bpy.data.objects.get(ffd) is None:
			return False
		else:
			bpy.data.objects[obj.name].select_set(False)
			bpy.data.objects[ffd].select_set(True)
			ctx.view_layer.objects.active = bpy.data.objects[ffd]
			bpy.ops.object.editmode_toggle()
			return True

	def execute(self, ctx):
		selection = ctx.active_object
		if selection.name.endswith(".Lattice"):
			self.apply_ffd(ctx, selection)
		elif self.get_ffd(ctx, selection):
			ffd = ctx.active_object
		else:
			self.setup_ffd(ctx, selection)
		return{'FINISHED'}
	
####### UV SCRIPTS #########

def selected_uv_verts_pos(ctx):
	bm = get_bmesh(ctx)
	uv_layer = bm.loops.layers.uv.verify()
	verts_loc = [loop[uv_layer].uv for face in bm.faces for loop in face.loops if loop[uv_layer].select]
	return verts_loc

class UV_OT_QuickRotateUv90Pos(Operator):
	bl_idname = "uv.rotate_90_pos"
	bl_label = "Rotate UV 90 Pos"
	bl_description = "Rotate Uvs +90 degrees"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, ctx):
		original_pos = selected_uv_verts_pos(ctx)
		print(original_pos)
		#original_pos = reduce((lambda x, y: x + y), original_pos)
		bpy.ops.transform.rotate(value= math.radians(90), orient_axis='Z')
		new_pos = selected_uv_verts_pos(ctx)
		return{'FINISHED'}

class UV_OT_QuickRotateUv90Neg(Operator):
	bl_idname = "uv.rotate_90_neg"
	bl_label = "Rotate Uvs -90 degrees"
	bl_description = "Edit pivot position and scale"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, ctx):
		bpy.ops.transform.rotate(value=math.radians(-90), orient_axis='Z')
		return{'FINISHED'}