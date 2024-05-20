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
# 2024/05/16

import bpy
import bmesh

from bpy.types import Operator
from bpy.utils import register_class, unregister_class

#############################################################

def get_mode(ctx):
	mode = ctx.mode
	if mode == 'EDIT_MESH':
		selection_mode = (tuple(ctx.scene.tool_settings.mesh_select_mode))
		if selection_mode[0]:
			return 'VERT'
		elif selection_mode[1]:
			return 'EDGE'
		elif selection_mode[2]:
			return 'FACE'

	if mode == 'EDIT_GPENCIL':
		return ctx.scene.tool_settings.gpencil_selectmode_edit

	return mode


def get_bmesh(ctx):
	if get_mode(ctx) in ['VERT', 'EDGE', 'FACE']:
		return bmesh.from_edit_mesh(ctx.edit_object.data)
	else:
		print("Must be in obj mode to get bmesh")


def set_mode(ctx, mode, grow=False):
	actual_mode = get_mode(ctx)
	if mode == 'OBJECT' and actual_mode != 'OBJECT':
		bpy.ops.object.mode_set(mode='OBJECT')

	elif mode in ['VERT', 'EDGE', 'FACE']:
		if actual_mode == 'OBJECT':
			bpy.ops.object.mode_set(mode='EDIT')
		bpy.ops.mesh.select_mode(type=mode, use_expand=grow)


# Make selection based on indexes for selected mesh elements or names for objects
def select(
		ctx, target, mode='', item=True, replace=False, deselect=False,
		add_to_history=False, safe_mode=False
	):
	if not mode:
		mode = get_mode(ctx)

	if safe_mode:
		existing_items = get_selected(mode=mode, item=item, all=True)

	selection_value = True

	if deselect:
		selection_value = False

	if type(target) is not list:
		target = [target]

	if mode == 'OBJECT':
		if replace:
			bpy.ops.object.select_all(action='DESELECT')

		if item:
			for obj in target:
				target.select_set(selection_value)

		else:
			for obj in target:
				bpy.data.objects[obj].select_set(selection_value)

	elif mode in ['VERT', 'EDGE', 'FACE']:
		bm = get_bmesh(ctx)

		if replace:
			bpy.ops.mesh.select_all(action='DESELECT')

		if item:
			target = [item.index for item in target]

		if safe_mode:
			if mode == 'VERT':
				for vert in target:
					if vert in existing_items:
						bm.verts[vert].select = selection_value
						if add_to_history:
							bm.select_history.add(bm.verts[vert])

			elif mode == 'EDGE':
				for edge in target:
					if edge in existing_items:
						bm.edges[edge].select = selection_value
						if add_to_history:
							bm.select_history.add(bm.edges[edge])

			elif mode == 'FACE':
				for face in target:
					if face in existing_items:
						bm.faces[face].select = selection_value
						if add_to_history:
							bm.select_history.add(bm.faces[face])

		else:
			if mode == 'VERT':
				for vert in target:
					bm.verts[vert].select = selection_value
					if add_to_history:
						bm.select_history.add(bm.verts[vert])

			elif mode == 'EDGE':
				for edge in target:
					bm.edges[edge].select = selection_value
					if add_to_history:
						bm.select_history.add(bm.edges[edge])

			elif mode == 'FACE':
				for face in target:
					bm.faces[face].select = selection_value
					if add_to_history:
						bm.select_history.add(bm.faces[face])

	elif mode == 'EDIT_CURVE':
		curves = ctx.active_object.data.splines
		for curve in curves:
			if safe_mode:
				if curve.type == 'BEZIER':
					for point in curve.bezier_points:
						if point in existing_items:
							point.select_control_point = True
				else:
					for point in curve.points:
						if point in existing_items:
							point.select = True
			else:
				if curve.type == 'BEZIER':
					for point in curve.bezier_points:
						point.select_control_point = True
				else:
					for point in curve.points:
						point.select = True


# Return item or index for selected mesh elements or names for objects
# Add selection order by using print([a.index for a in bm.select_history])
def get_selected(ctx, mode='', item=True, ordered=False, all=False):
	selection = []
	if not mode:
		mode = get_mode(ctx)

	if mode == 'OBJECT':
		if item:
			return [obj for obj in ctx.selected_objects]

		else:
			return [obj.name for obj in ctx.selected_objects]

	elif mode in ['VERT', 'EDGE', 'FACE']:
		bm = get_bmesh(ctx)

		if ordered:
			if mode == 'VERT':
				selection = [
					vert for vert in bm.select_history
						if isinstance(vert, bmesh.types.BMVert)
				]
			elif mode == 'EDGE':
				selection = [
					edge for edge in bm.select_history
						if isinstance(edge, bmesh.types.BMEdge)
				]
			elif mode == 'FACE':
				selection = [
					face for face in bm.select_history
						if isinstance(face, bmesh.types.BMFace)
				]

		if all:
			if mode == 'VERT':
				selection = [vert for vert in bm.verts]
			elif mode == 'EDGE':
				selection = [edge for edge in bm.edges]
			elif mode == 'FACE':
				selection = [face for face in bm.faces]

		else:
			if mode == 'VERT':
				selection = [vert for vert in bm.verts if vert.select]
			elif mode == 'EDGE':
				selection = [edge for edge in bm.edges if edge.select]
			elif mode == 'FACE':
				selection = [face for face in bm.faces if face.select]

		if item:
			return selection
		else:
			return [element.index for element in selection]

	elif mode == 'EDIT_CURVE':
		curves = ctx.active_object.data.splines
		points = []

		if all:
			for curve in curves:
				if curve.type == 'BEZIER':
					points.append([point for point in curve.bezier_points])

				else:
					points.append([point for point in curve.points])

		else:
			for curve in curves:
				if curve.type == 'BEZIER':
					points.append([point for point in curve.bezier_points
								   if point.select_control_point])

				else:
					points.append([point for point in curve.points
								   if point.select])

		points = [item for sublist in points for item in sublist]
		return points

	else:
		return []


def select_face_loops(ctx, ring=False):
	if ring:
		bpy.ops.mesh.loop_multi_select(ring=True)

	else:
		bpy.ops.mesh.loop_multi_select(ring=False)

	set_mode(ctx, 'EDGE')
	bpy.ops.mesh.select_more()
	set_mode(ctx, 'FACE')
	bpy.ops.mesh.select_less()


# Review this function later
def select_vert_loops(ctx, ring=False):
	bm = get_bmesh(ctx)
	vert = get_selected(ctx, 'VERT', item=False)
	edges = [edge.index for edge in bm.verts[vert[0]].link_edges]
	select(ctx, edges, 'EDGE', item=False)

	if ring:
		bpy.ops.mesh.loop_multi_select(ring=True)

	else:
		bpy.ops.mesh.loop_multi_select(ring=False)


def distance_between_elements(ctx, elements, mode, ring=False):
	select(ctx, elements, mode, item=False, replace=True)
	bpy.ops.mesh.shortest_path_select()
	selection = get_selected(ctx, mode, item=False)

	if ring:
		distance = len(selection)-3
	else:
		distance = len(selection)-2

	if distance > 0:
		return distance
	return 0


def list_intersection(a, b):
	temp = set(b)
	result = [item for item in a if item in temp]
	return result


def list_difference(a, b):
	temp = set(b)
	result = [item for item in a if item not in temp]
	return result


def organize_elements_by_loop(ctx, elements, mode, ring=False):
	selected_elements = []
	elements_to_check = elements

	while len(elements_to_check) > 0:
		select(ctx, [elements_to_check[0]], mode, item=False, replace=True)

		if mode == 'VERT':
			select_vert_loops(ctx, ring=ring)
		elif mode == 'EDGE':
			bpy.ops.mesh.loop_multi_select(ring=ring)
		elif mode == 'FACE':
			select_face_loops(ctx, ring=ring)

		element_loop = get_selected(ctx, mode, item=False)
		selected_elements.append(list_intersection(element_loop, elements_to_check))
		elements_to_check = list_difference(elements_to_check, element_loop)

	return selected_elements


def is_step_selection(ctx, selection, mode, ring=False):
	if len(selection) > 2:
		results = []
		# OPTIMIZATION: ONLY CHECK FIRST 3
		if len(selection) > 3:
			selection = selection[:3]

		for a in selection:
			min = []
			other_elements = list_difference(selection, [a])

			for b in other_elements:
				distance = distance_between_elements(ctx, [a, b], mode, ring)

				if len(min) == 0 or min[1] > distance:
					min = [[a, b], distance]

			results.append(min)

		distances = list(set([x[1] for x in results]))
		select(ctx, selection, item=False, replace=True, add_to_history=True)

		if len(distances) == 1:
			return [True, distances[0]]

		else:
			return [False, 0]

	else:
		return [False, 0]


# Think of new way to complete step selection for future updates to fix bugs with
# step selections in loops and rings that are not cyclical
def complete_step_selection(ctx, mode):
	iteration = 0
	last_selection = []
	selected_elements = get_selected(ctx, mode, item=False)

	while not selected_elements == last_selection and iteration < 400:
		bpy.ops.mesh.select_next_item()
		last_selection = selected_elements
		selected_elements = get_selected(ctx, mode, item=False)
		iteration += 1


def smart_loop(ctx, ring=False):
	final_selection = []
	mode = get_mode(ctx)
	selection = get_selected(ctx, mode, item=False)
	organized_loops = organize_elements_by_loop(ctx, selection, mode, ring)

	for loop in organized_loops:
		step_selection_result = is_step_selection(ctx, loop, mode, ring)

		if step_selection_result[0]:
			complete_step_selection(ctx, mode)

		elif len(loop) == 2:
			distance = distance_between_elements(
				ctx, [loop[0], loop[1]], mode, ring
			)

			if distance > 0:
				select(
					ctx, loop, mode, item=False,
					replace=True, add_to_history=True
				)

				if ring:
					bpy.ops.mesh.shortest_path_select(use_face_step=True)

				else:
					bpy.ops.mesh.shortest_path_select()

			elif distance == 0:
				select(
					ctx, loop, mode, item=False,
					replace=True, add_to_history=True
				)
				bpy.ops.mesh.loop_multi_select(ring=ring)

		else:
			if mode == 'EDGE':
				select(
					ctx, loop, mode, item=False,
					replace=True, add_to_history=True
				)
				bpy.ops.mesh.loop_multi_select(ring=ring)

		final_selection += get_selected(mode, item=False)

	select(
		ctx, final_selection, mode, item=False,
		replace=True, add_to_history=True
	)


class SmartSelectLoop(Operator):
	"""
	BUGS:
	 *Step Face Loop only goes in one direction for faces
	 *Sometimes top and bottom is ignored on loops of spheres, investigate
	 *Complete step selection only works in one direction
	"""
	bl_idname = "mesh.smart_select_loop"
	bl_label = "Smart Select Loop"
	bl_description = "Context sensitive smart loop selection"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, ctx):
		smart_loop(ctx)
		return{'FINISHED'}


class SmartSelectRing(Operator):
	"""
	BUGS:
	 *Step Face Loop only goes in one direction for faces
	"""
	bl_idname = "mesh.smart_select_ring"
	bl_label = "Smart Select Ring"
	bl_description = "Context sensitive smart ring selection"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, ctx):
		smart_loop(ctx, ring=True)
		return{'FINISHED'}

classes = {
	SmartSelectLoop,
	SmartSelectRing
}


def register_loop():
	for c in classes:
		register_class(c)


def unregister_loop():
	for c in classes:
		unregister_class(c)


if __name__ == '__main__':
	register_loop()