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


from bsmax.state import is_objects_selected
from bsmax.mouse import get_click_point_info
from bsmax.math import get_axis_constraint



class Object_OT_Drag_Clone(bpy.types.Operator):
	bl_idname = "object.drag_clone"
	bl_label = "Drag Clone"
	bl_options = {'REGISTER', 'UNDO'}

	point_a = None
	point_b = None

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	
	def execute(self,ctx):
		self.report({'OPERATOR'},'bpy.ops.object.drag_clone()')
		return{"FINISHED"}

	def modal(self, ctx, event):
		x, y = event.mouse_region_x, event.mouse_region_y
		cp = get_click_point_info(x, y, ctx)
		if event.type == 'LEFTMOUSE':
			if event.value == 'PRESS':
				self.point_a = cp.view
			if event.value =='RELEASE':
				return {'CANCELLED'}
		# get direction
		if event.type == 'MOUSEMOVE':
			if self.point_a != None:
				self.point_b = cp.view
				tr = get_axis_constraint(self.point_a, self.point_b)
				print(tr)
		# get active tool
		# set action
		if event.type in {'RIGHTMOUSE', 'ESC'}:
			return {'CANCELLED'}
		return {'RUNNING_MODAL'}

	def invoke(self, ctx, event):
		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}



def register_dragclone():
	bpy.utils.register_class(Object_OT_Drag_Clone)



def unregister_dragclone():
	bpy.utils.unregister_class(Object_OT_Drag_Clone)