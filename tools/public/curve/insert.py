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

"""
the idea is
	devide each segment to 100 part
	collect distance of click point with each points
	get two shortest distance point
between two point repatet the
	devide each section to 100 part
	collect distance of click point with each points
	get two shortest distance point
to get beeter resoult repeat the
	devide each section to 100 part
	collect distance of click point with each points
	get shortest distance point time
	if distance was lower than specific value return the index and time
"""

class Point:
	def __init__(self, spline_index, curve_index, co, time):
		self.spline_index = spline_index
		self.curve_index = curve_index
		self.co = co
		self.time = time

class Curve_OT_Insert(Operator):
	bl_idname = "curve.dividplus"
	bl_label = "Insert"

	def apply(self):
		curve = self.curve
		curve.restore()
		curve.update()

	def modal(self, ctx, event):
		ctx.area.tag_redraw()
		x,y = event.mouse_region_x, event.mouse_region_y
		
		if not event.type in {'LEFTMOUSE', 'MOUSEMOVE', 'ESC'}:
			return {'PASS_THROUGH'}
		
		elif event.type == 'MOUSEMOVE':
			pass
			# recalculate and update
			# update with new position

		elif event.type == 'LEFTMOUSE':
			if event.value == 'PRESS':
				pass
				# get nearest point between curve and click point
				# get time and segment index of the point
				# insert 

			if event.value =='RELEASE':
				pass
				# commit
				
			return {'RUNNING_MODAL'}

		elif event.type in {'RIGHTMOUSE','ESC'}:
			return {'CANCELLED'}

		return {'RUNNING_MODAL'}
	
	def cancel(self, ctx):
		pass

	def invoke(self, ctx, event):
		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}

def register_insert():
	bpy.utils.register_class(Curve_OT_Insert)

def unregister_insert():
	bpy.utils.unregister_class(Curve_OT_Insert)