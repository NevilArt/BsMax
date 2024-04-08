############################################################################
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation,either version 3 of the License,or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not,see <https://www.gnu.org/licenses/>.
############################################################################
# 2024/040/04

import bpy
from bpy.types import Operator
from bsmax.actions import set_as_active_object


def mesh_to_cloth(obj):
	cloth = obj.modifiers["Cloth"]
	cloth.settings.use_pressure = True
	cloth.settings.uniform_pressure_force = 3
	cloth.collision_settings.use_self_collision = True
	cloth.settings.effector_weights.gravity = 0


def face_to_mesh(obj):
	obj.modifiers.new(name='Solidify', type='SOLIDIFY')
	obj.modifiers.new(name='Remesh', type='REMESH')
	obj.modifiers.new(name='Cloth', type='CLOTH')
	mesh_to_cloth(obj)


def curve_to_mesh(ctx, obj):
	obj.modifiers.new(name='Fill', type='NODES')
	node_group = obj.modifiers['Fill'].node_group
	nodes = node_group.nodes
	nodes.new('GeometryNodeFillCurve')
	input = nodes['Group Input']
	fill = nodes['Fill Curve']
	output = nodes['Group Output']

	node_group.links.new(input.outputs['Geometry'], fill.inputs['Curve'])
	node_group.links.new(fill.outputs['Mesh'], output.inputs['Geometry'])

	set_as_active_object(ctx, obj)
	bpy.ops.object.convert(target='MESH')
	
	face_to_mesh(obj)


def font_to_mesh(ctx, obj):
	set_as_active_object(ctx, obj)


class Mesh_OT_Make_Pillow(Operator):
	bl_idname = "mesh.make_pillow"
	bl_label = "Make Pillow"
	bl_description = "Convert Selected Flat Mesh or Curve to pillow"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		# TODO
		return True
	
	def execute(self, ctx):
		# Filter by height
		objs = [obj for obj in ctx.selected_objects if obj.dimensions.z == 0]
		# Setup Pillow
		for obj in objs:
			if obj.type == 'MESH':
				face_to_mesh(obj)

			elif obj.type == 'CURVE':
				curve_to_mesh(ctx, obj)

			# elif obj.type == 'FONT':
			# 	font_to_mesh(ctx, obj)

		return{"FINISHED"}


def register_preset():
	bpy.utils.register_class(Mesh_OT_Make_Pillow)


def unregister_preset():
	bpy.utils.unregister_class(Mesh_OT_Make_Pillow)


if __name__ == '__main__':
	register_preset()
