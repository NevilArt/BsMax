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
# 2024/08/30

import bpy

from mathutils import Vector

from bpy.types import Operator
from bpy.props import BoolProperty, EnumProperty
from bpy.utils import register_class, unregister_class


# this operator works smoother then the original one in panel 
class UV_OT_Mirror_Cover(Operator):
	bl_idname = 'uv.mirror_cover'
	bl_label = "Mirror (Cover)"
	bl_description = "Mirror the selected UV"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}
	
	axis: EnumProperty(
		name="Axis",
		items=[
			('X', "X", "X Axis"),
			('Y', "Y", "Y Axis")
		],
		default='X'
	) # type: ignore

	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'EDIT_MESH'

	def execute(self, ctx):
		if self.axis == 'X':
			bpy.ops.transform.mirror(constraint_axis=(True, False, False))

		if self.axis == 'Y':
			bpy.ops.transform.mirror(constraint_axis=(False, True, False))

		return{'FINISHED'}


class UV_OT_Turn(Operator):
	bl_idname = 'uv.turn'
	bl_label = "Turn"
	bl_description = "Rotate Selected UV by given degere"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}
	
	ccw: BoolProperty(name="CCW") # type: ignore

	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'EDIT_MESH'

	def execute(self, ctx):
		value = 1.5708 if self.ccw else -1.5708

		bpy.ops.transform.rotate(
			value=value,
			orient_axis='Z',
			orient_type='VIEW',
			orient_matrix=((1, 0, 0), ( 0, 1, 0), ( 0, 0, 1)),
			orient_matrix_type='VIEW'
		)
		
		return{'FINISHED'}


class UV_OT_Snap_Toggle(Operator):
	bl_idname = 'uv.snap_toggle'
	bl_label = "Snap Toggle"
	bl_description = "Rotate Selected UV by Given Degere"
	bl_options = {'REGISTER', 'INTERNAL'}
	
	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'EDIT_MESH'

	def execute(self, ctx):
		tool_settings = ctx.scene.tool_settings
		tool_settings.use_snap_uv = not tool_settings.use_snap_uv
		return{'FINISHED'}


class UV_OT_Split_To_Island(Operator):
	bl_idname = 'uv.split_to_island'
	bl_label = "Split to Island"
	bl_description = "Split Selected to Island with seam border"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}
	
	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'EDIT_MESH'

	def execute(self, ctx):
		# store sync mode
		use_uv_select_sync = ctx.scene.tool_settings.use_uv_select_sync
		if use_uv_select_sync:
			# disable sync mode and reselect 
			ctx.scene.tool_settings.use_uv_select_sync = False
			bpy.ops.uv.select_all(action='SELECT')

		bpy.ops.uv.select_split()

		# scale down to seprate from rest to let next operator works
		bpy.ops.transform.resize(
			value=(0.5, 0.5, 0.5),
			orient_type='GLOBAL',
			orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
			orient_matrix_type='GLOBAL'
		)
		# conver edges to seam
		bpy.ops.uv.seams_from_islands()

		# reset scale to original size
		bpy.ops.transform.resize(
			value=(2, 2, 2),
			orient_type='GLOBAL',
			orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
			orient_matrix_type='GLOBAL'
		)

		# reset sync mode
		ctx.scene.tool_settings.use_uv_select_sync = use_uv_select_sync
		return{'FINISHED'}


########################################################################

# def get_active_uv_face(mesh):
# 	uv_layer = mesh.uv_layers.active
# 	if not uv_layer:
# 		return None

# 	uv_data = uv_layer.data
# 	selected_faces = []

# 	# Find the selected UV face in the UV Editor
# 	for poly in mesh.polygons:
# 		face_uv = [uv_data[loop_index].uv for loop_index in poly.loop_indices]
# 		if all(uv_data[loop_index].select for loop_index in poly.loop_indices):
# 			selected_faces.append(face_uv)

# 	if len(selected_faces) == 0:
# 		return None

# 	if len(selected_faces) > 1:
# 		return None

# 	return selected_faces[0]



class UV_OT_Rectangulate_Active_Face(Operator):
	bl_idname = 'uv.rectangulate_active_face'
	bl_label = "Rectangulate Active Face"
	bl_description = "Make active face perfect rectangle"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(self, ctx):
		return ctx.scene.tool_settings.uv_select_mode == 'FACE'

	def execute(self, ctx):
		# face = get_active_uv_face(ctx.object.data)
		# print(">>>", face)
		return{'FINISHED'}

########################################################################


# Original Author 'Simon Lusenc'
# Algorithm stands on the thesis that order of polygon loop is defining direction of face normal
# and that same loop order is used in uv data.
# With this knowladge we can easily say that cross product:
# (v2.uv-v1.uv)x(v3.uv-v2.uv) gives us uv normal direction of part of the polygon. Further
# this normal has to be used in dot product with up vector (0,0,1) and result smaller than zero
# means uv normal is pointed in opposite direction than it should be (partial polygon v1,v2,v3 is flipped).

class UV_OT_Select_Flipped_UVs(Operator):
	bl_idname = 'uv.select_flipped'
	bl_label = "Select Flipped UVs"
	bl_description = "Select polygons with flipped UV Mapping"

	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'EDIT_MESH'

	def execute(self, ctx):
		obj = ctx.object
		
		bpy.ops.mesh.select_all(action='DESELECT')
		bpy.ops.object.mode_set(mode='OBJECT')
		
		for poly in obj.data.polygons:
			# calculate uv differences between current and next face vertex for
			# whole polygon	  
			diffs = []
			for l_i in poly.loop_indices:
				
				next_l = l_i+1 if l_i < poly.loop_start + poly.loop_total - 1 \
															else poly.loop_start
				
				next_v_uv = obj.data.uv_layers.active.data[next_l].uv
				v_uv = obj.data.uv_layers.active.data[l_i].uv
				
				diffs.append((next_v_uv - v_uv).to_3d())	

			# go trough all uv differences and calculate cross product between
			# currentand next cross product gives us normal of the triangle.
			# That normal then is used in dot product with up vector (0,0,1).
			# If result is negative we have found flipped part of polygon.
			for i, _ in enumerate(diffs):
				
				if i == len(diffs)-1:
					break
				
				# as soon as we find partial flipped polygon we
				# select it and finish search
				if diffs[i].cross(diffs[i+1]) @ Vector((0,0,1)) <= 0:
					poly.select = True
					break

		bpy.ops.object.mode_set(mode="EDIT")
		
		return {'FINISHED'}


def uv_select_menu(self, ctx):
	self.layout.operator("uv.select_flipped")


classes = {
	UV_OT_Mirror_Cover,
	UV_OT_Turn,
	UV_OT_Select_Flipped_UVs,
	UV_OT_Snap_Toggle,
	UV_OT_Split_To_Island,
	UV_OT_Rectangulate_Active_Face
}


def register_edit():
	for cls in classes:
		register_class(cls)
	
	bpy.types.IMAGE_MT_select.append(uv_select_menu)


def unregister_edit():
	bpy.types.IMAGE_MT_select.remove(uv_select_menu)

	for cls in classes:
		unregister_class(cls)


if __name__ == '__main__':
	# register_edit()
	register_class(UV_OT_Rectangulate_Active_Face)