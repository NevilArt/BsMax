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
from bpy.props import EnumProperty, BoolProperty


def mesh_select(mesh, axis, direction):
	bpy.ops.object.mode_set(mode='EDIT')
	bpy.ops.mesh.select_all(action='DESELECT')
	bpy.ops.object.mode_set(mode='OBJECT')

	axis_index = {'X': 0, 'Y': 1, 'Z': 2}.get(axis.upper())

	if direction.upper() == 'POSITIVE':
		comparison = lambda coord: coord >= 0
	elif direction.upper() == 'NEGATIVE':
		comparison = lambda coord: coord < 0

	for vert in mesh.vertices:
		if comparison(vert.co[axis_index]):
			vert.select = True
		
		vert.select = comparison(vert.co[axis_index])

	bpy.ops.object.mode_set(mode='EDIT')

def set_shape_key_active(obj, shape_key_name):
	shape_key = obj.data.shape_keys.key_blocks.get(shape_key_name)
	if shape_key:
		obj.active_shape_key_index = obj.data.shape_keys.key_blocks.keys().index(shape_key_name)


class Mesh_OT_Topo_Symmetry(Operator):
	bl_idname = 'mesh.topo_symmetrize'
	bl_label = "Topo Symmetrize"
	bl_options = {'REGISTER', 'UNDO'}

	axis: EnumProperty(
		name="Axis", 
		items=[
			('X', "X", "", 'EVENT_X', 1),
			('Y', "Y", "", 'EVENT_Y', 2),
			('Z', "Z", "", 'EVENT_Z', 3)
		],
		default='X',
		description=""
	) # type: ignore

	direction:BoolProperty(default=False) # type: ignore

	@classmethod
	def poll(self, ctx):
		return ctx.mode == "EDIT_MESH"

	def draw(self,ctx):
		row = self.layout.row()
		row.prop(self, 'axis', text="", expand=True)
		text = self.axis + ' - < +' if self.direction else self.axis +' - > +'
		row.prop(self, 'direction', text=text, icon='BLANK1')

	def execute(self, ctx):
		shape_key_name = 'SYMETRYCORRECTIONKEY'
		obj = ctx.object
		bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

		if not ctx.object.data.shape_keys:
			obj.shape_key_add(name="Basis", from_mix=False)

		obj.shape_key_add(name=shape_key_name, from_mix=False)
		
		set_shape_key_active(obj, shape_key_name)
		bpy.ops.object.shape_key_mirror(use_topology=True)
		set_shape_key_active(obj, "Basis")

		side = 'NEGATIVE' if self.direction else 'POSITIVE'
		mesh_select(obj.data, self.axis, side)
		
		bpy.ops.mesh.blend_from_shape(shape=shape_key_name, add=False)
		bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
		
		set_shape_key_active(obj, shape_key_name)
		bpy.ops.object.shape_key_remove(all=False)
		bpy.ops.object.mode_set(mode='EDIT')
		return{'FINISHED'}

	def invoke(self, ctx, event):
		return ctx.window_manager.invoke_props_dialog(self)


def topo_symmetrize_menu(self, context):
	layout = self.layout
	layout.separator()
	layout.operator('mesh.topo_symmetrize')


def register_topo():
	bpy.utils.register_class(Mesh_OT_Topo_Symmetry)
	bpy.types.VIEW3D_MT_edit_mesh.append(topo_symmetrize_menu)


def unregister_topo():
	bpy.utils.unregister_class(Mesh_OT_Topo_Symmetry)
	bpy.types.VIEW3D_MT_edit_mesh.remove(topo_symmetrize_menu)


if __name__ == '__main__':
	register_topo()