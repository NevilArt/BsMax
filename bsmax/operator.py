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
from bsmax.curve import Curve

class CurveTool(Operator):
	bl_options = {'REGISTER','UNDO'}
	curve,obj = None,None
	start,finish = False,False
	start_x,start_y = 0,0
	value_x,value_y,value_w = 0,0,0

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			if len(ctx.scene.objects) > 0:
				if ctx.object != None:
					return ctx.mode == 'EDIT_CURVE'
		return False

	def get_data(self, ctx):
		self.obj = ctx.active_object
		self.curve = Curve(self.obj)

	def apply(self):
		pass

	def draw(self, ctx):
		pass

	def abort(self):
		self.curve.reset()

	def execute(self, ctx):
		if self.value_x + self.value_y == 0:
			self.abort()
		else:
			self.apply()
		return{"FINISHED"}

	def check(self, ctx):
		if not self.start:
			self.start = True
		self.apply()

	def modal(self, ctx, event):
		if event.type == 'LEFTMOUSE':
			if not self.start:
				self.start = True
				self.start_x = event.mouse_x
				self.start_y = event.mouse_y
				self.get_data(ctx)
		if event.type == 'MOUSEMOVE':
			if self.start:
				self.value_x = (event.mouse_x-self.start_x)/200
				self.value_y = (event.mouse_y-self.start_y)/200
				self.apply()
			if self.start and event.value =='RELEASE':
				self.finish = True
		#TODO mouse weel changes self.value_w
		if self.finish:
			if self.value_x + self.value_y == 0:
				self.abort()
			return {'CANCELLED'}
		if event.type in {'RIGHTMOUSE', 'ESC'}:
			self.abort()
			return {'CANCELLED'}
		return {'RUNNING_MODAL'}

	def invoke(self, ctx, event):
		self.get_data(ctx)
		if self.typein:
			wm = ctx.window_manager
			return wm.invoke_props_dialog(self)#,width=120)
		else:
			ctx.window_manager.modal_handler_add(self)
			return {'RUNNING_MODAL'}

__all__ = ["CurveTool"]