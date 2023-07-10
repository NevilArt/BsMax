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

from mathutils import Vector

from bpy.types import Operator
from bpy.props import BoolProperty, EnumProperty



# this operator works smoother then the original one in panel 
class UV_OT_Mirror_Cover(Operator):
	""" Mirror the selected UV """
	bl_idname = "uv.mirror_cover"
	bl_label = "Mirror (Cover)"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}
	
	axis: EnumProperty(
		name="Axis",  default='X', 
		items=[('X', 'X', ''), ('Y', 'Y', '')]
	)

	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'EDIT_MESH'

	def execute(self, ctx):
		if self.axis == 'X':
			bpy.ops.transform.mirror(constraint_axis=(True, False, False))

		if self.axis == 'Y':
			bpy.ops.transform.mirror(constraint_axis=(False, True, False))

		return{"FINISHED"}



class UV_OT_Turn(Operator):
	""" Rotate Selected UV by given degere """
	bl_idname = "uv.turn"
	bl_label = "Turn"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}
	
	ccw: BoolProperty(name="CCW")

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
		
		return{"FINISHED"}



class UV_OT_Snap_Toggle(Operator):
	""" Rotate Selected UV by given degere """
	bl_idname = "uv.snap_toggle"
	bl_label = "Snap Toggle"
	bl_options = {'REGISTER', 'INTERNAL'}
	
	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'EDIT_MESH'

	def execute(self, ctx):
		tool_settings = ctx.scene.tool_settings
		tool_settings.use_snap_uv = not tool_settings.use_snap_uv
		return{"FINISHED"}



class UV_OT_Split_To_Island(Operator):
	""" Split Selected to Island with seam border """
	bl_idname = "uv.split_to_island"
	bl_label = "Split to Island"
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
		bpy.ops.transform.resize(value=(0.5, 0.5, 0.5),
								orient_type='GLOBAL',
								orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
								orient_matrix_type='GLOBAL'
							)
		# conver edges to seam
		bpy.ops.uv.seams_from_islands()

		# reset scale to original size
		bpy.ops.transform.resize(value=(2, 2, 2),
						orient_type='GLOBAL',
						orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
						orient_matrix_type='GLOBAL'
					)

		# reset sync mode
		ctx.scene.tool_settings.use_uv_select_sync = use_uv_select_sync
		return{"FINISHED"}




class UV_OT_Rectangulate_Active_Face(Operator):
	""" Make active face perfect rectangle """
	bl_idname = "uv.rectangulate_active_face"
	bl_label = "Rectangulate Active Face"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(self, ctx):
		return ctx.scene.tool_settings.uv_select_mode == 'FACE'


	def execute(self, ctx):
		# uv = ctx.object.data.uv_layers.active

		# bm = bmesh.from_edit_mesh(ctx.object.data)
		# uv_layer = bm.verts.layers.uv.verify()

		# for face in bm.faces:
		# 	print(face.index)

		# 	for loop in face.loops:
		# 		uv = loop[uv_layer]
		# 		print(uv.co, uv.select, loop.vert.index)
		# 		#TODO --- 
		return{"FINISHED"}



""" Original Author 'Simon Lusenc' """
class UV_OT_Select_Flipped_UVs(Operator):
	"""Select polygons with flipped UV mapping."""

	# Algorithm stands on the thesis that order of polygon loop is defining direction of face normal
	# and that same loop order is used in uv data.
	# With this knowladge we can easily say that cross product:
	# (v2.uv-v1.uv)x(v3.uv-v2.uv) gives us uv normal direction of part of the polygon. Further
	# this normal has to be used in dot product with up vector (0,0,1) and result smaller than zero
	# means uv normal is pointed in opposite direction than it should be (partial polygon v1,v2,v3 is flipped).

	bl_idname = "uv.select_flipped"
	bl_label = "Select Flipped UVs"

	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'EDIT_MESH'

	def execute(self, ctx):
		obj = ctx.object
		
		bpy.ops.mesh.select_all(action="DESELECT")
		bpy.ops.object.mode_set(mode="OBJECT")
		
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
				
				# as soon as we find partial flipped polygon we select it and finish search
				if diffs[i].cross(diffs[i+1]) @ Vector((0,0,1)) <= 0:
					poly.select = True
					break

		bpy.ops.object.mode_set(mode="EDIT")
		
		return {'FINISHED'}



def uv_select_menu(self, ctx):
	self.layout.operator("uv.select_flipped")



classes = (
	UV_OT_Mirror_Cover,
	UV_OT_Turn,
	UV_OT_Select_Flipped_UVs,
	UV_OT_Snap_Toggle,
	UV_OT_Split_To_Island,
	UV_OT_Rectangulate_Active_Face
)


def register_edit():
	for c in classes:
		bpy.utils.register_class(c)
	
	bpy.types.IMAGE_MT_select.append(uv_select_menu)



def unregister_edit():
	bpy.types.IMAGE_MT_select.remove(uv_select_menu)

	for c in classes:
		bpy.utils.unregister_class(c)



if __name__ == '__main__':
	register_edit()