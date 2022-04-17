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
from bpy.props import BoolProperty



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
		bpy.ops.transform.rotate(value=value,
								orient_axis='Z',
								orient_type='VIEW',
								orient_matrix=((1, 0, 0), ( 0, 1, 0), ( 0, 0, 1)),
								orient_matrix_type='VIEW'
				)
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
		uv = ctx.object.data.uv_layers.active
		#TODO --- 
		return{"FINISHED"}




classes = [UV_OT_Turn, UV_OT_Split_To_Island]

def register_edit():
	for c in classes:
		bpy.utils.register_class(c)

def unregister_edit():
	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == '__main__':
	register_edit()