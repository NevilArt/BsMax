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

import bpy

from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from bpy.app import version


def get_npolys(mesh):
	return [
		polygon for polygon in mesh.polygons if len(polygon.edge_keys) > 4
	]


def get_npolys_border_edges(mesh, npolys):
	border_edges, inner_edges = [], []

	for npoly in npolys:
		for poly_edge_key in npoly.edge_keys:
			for i, edge_key in enumerate(mesh.edge_keys):
				if edge_key == poly_edge_key:
					edge = mesh.edges[i]
					if edge in border_edges:
						inner_edges.append(edge)
					else:
						border_edges.append(edge)
					continue

	for inner_edge in inner_edges:
		border_edges.remove(inner_edge)

	return border_edges


def set_edge_crease(mesh, edges, crease):
	if version < (4, 0, 0):
		for edge in edges:
			edge.crease = crease
		return
	
	mesh.edge_creases_ensure()
	creases_data = mesh.edge_creases.data
	for edge in edges:
		creases_data[edge.index].value = crease


def get_material(name, color):
	materials = bpy.data.materials
	if name in materials:
		return materials[name]
	
	new_material = materials.new(name)
	new_material.diffuse_color = color


def get_open_geometry_node_editor():
	for screen in bpy.data.screens:
		for area in screen.areas:
			if not area.type == 'NODE_EDITOR':
				continue

			for space in area.spaces:
				if space.type == 'NODE_EDITOR' and \
					space.tree_type == 'GeometryNodeTree':

					return area
	return None

def get_active_node(area):
	if area:
		space = area.spaces.active
		if space.node_tree:
			return space.node_tree.nodes.active
	return None


def set_material(obj):
	root_material = get_material("Mesh Hair Root" ,(0, 0.007, 0.8, 1))
	body_material = get_material("Mesh Hair Body" ,(0.45, 0.03, 0.005, 1))
	if len(obj.data.materials) == 2:
		obj.data.materials[0] = root_material
		obj.data.materials[1] = body_material
		return

	obj.data.materials.clear()
	obj.data.materials.append(root_material)
	obj.data.materials.append(body_material)


def set_material_id(mesh, npolys):
	for polygon in mesh.polygons:
		polygon.material_index = 1
	for npoly in npolys:
		npoly.material_index = 0


def set_uv_chanel(mesh):
	if not mesh.uv_layers:
		mesh.uv_layers.new(name="UVMap")
	
	if 'UVMap' in mesh.uv_layers:
		return
	
	mesh.uv_layers[0].name = 'UVMap'


def fix_root_uv(mesh, npolys):
	for polygon in mesh.polygons:
		polygon.select = False
	for polygon in npolys:
		polygon.select = True
	bpy.ops.object.mode_set(mode='EDIT', toggle=False)
	bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)
	bpy.ops.object.mode_set(mode='OBJECT', toggle=False)


def modifier_check(obj):
	for modifier in obj.modifiers:
		if modifier.type == 'MESH_SEQUENCE_CACHE':
			modifier.read_data = {'VERT'}


def mesh_setting(obj):
	# active rest position
	obj.add_rest_position_attribute = True
	# clear sharp edges
	attributes = obj.data.attributes
	if 'sharp_edge' in attributes:
		attributes.remove(attributes['sharp_edge'])
	

def mesh_to_hair_guid(obj):
	if obj.type != 'MESH':
		return
	
	mesh = obj.data
	npolys = get_npolys(mesh)
	
	if not npolys:
		return

	edges = get_npolys_border_edges(mesh, npolys)
	set_edge_crease(mesh, edges, 1)
	set_material(obj)
	set_material_id(mesh, npolys)
	set_uv_chanel(mesh)
	fix_root_uv(mesh, npolys)
	modifier_check(obj)
	mesh_setting(obj)


class Particle_OT_mesh_to_Hair(Operator):
	bl_idname = 'particle.mesh_to_hair'
	bl_label = "Mesh to hair"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			if ctx.mode == 'OBJECT':
				return ctx.selected_objects
		return False
	
	def execute(self, ctx):
		selection = ctx.selected_objects.copy() 
		bpy.ops.object.select_all(action='DESELECT')
		for obj in selection:
			obj.select_set(state=True)
			ctx.view_layer.objects.active = obj
			mesh_to_hair_guid(obj)
			obj.select_set(state=False)
		
		for obj in selection:
			obj.select_set(state=True)

		return{'FINISHED'}


class Node_OT_multi_object_picker(Operator):
	bl_idname = 'node.auto_object_picker'
	bl_label = "Auto object picker"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(self, ctx):
		active_space = ctx.area.spaces.active
		if active_space.type == 'NODE_EDITOR':
			return active_space.tree_type == 'GeometryNodeTree'
		return False
	
	def execute(self, ctx):
		objects = ctx.selected_objects
		obj_count = len(objects)
		active_space = ctx.area.spaces.active
		active_node = active_space.node_tree.nodes.active
		obj_inputs = [input 
			for input in active_node.inputs if input.type == 'OBJECT'
		]
		min_count = min(obj_count, len(obj_inputs))
		for index in range(min_count):
			obj_inputs[index].default_value = objects[index]

		return{'FINISHED'}


classes = {
	Particle_OT_mesh_to_Hair,
	Node_OT_multi_object_picker
}


def register_mesh_to_hair():
	for cls in classes:
		register_class(cls)


def unregister_mesh_to_hair():
	for cls in classes:
		unregister_class(cls)


if __name__ =="__main__":
	register_mesh_to_hair()