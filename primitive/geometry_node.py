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

class Object_OT_Geometry_Node_Primitive(Operator):
	bl_idname = "object.geometry_node_primitive"
	bl_label = "Geometry Node"
	bl_description = ""

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return ctx.mode == 'OBJECT'
		return False

	def execute(self, ctx):
		# bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
		# bpy.ops.node.new_geometry_node_group_assign()
		# bpy.ops.node.add_node(type="GeometryNodeMeshCircle", use_transform=True)
		# bpy.ops.node.translate_attach(TRANSFORM_OT_translate={"value":(4.38965, 59.2961, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False}, NODE_OT_attach={}, NODE_OT_insert_offset={})
		return {'FINISHED'}

classes = [Object_OT_Geometry_Node_Primitive]

def register_geometry_node():
	[bpy.utils.register_class(c) for c in classes]
	# bpy.types.VIEW3D_MT_view_cameras.append(camera_menu)

def unregister_geometry_node():
	# bpy.types.VIEW3D_MT_view_cameras.remove(camera_menu)	
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_geometry_node()