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
from bpy.props import BoolProperty, IntProperty, FloatProperty
from mathutils.geometry import intersect_point_line
from bpy_extras.view3d_utils import region_2d_to_location_3d, region_2d_to_vector_3d ,location_3d_to_region_2d
from bsmax.math import get_bias, get_distance
from bsmax.curve import Curve
from bsmax.operator import CurveTool

class Point:
	def __init__(self, segment, time, distance, point_on_view):
		self.segment = segment
		self.time = time
		self.distance = distance
		self.point_on_view = point_on_view



class Curve_OT_divid_plus(CurveTool):
	bl_idname = "curve.divid_plus"
	bl_label = "Divid plus"
	bl_options = {'REGISTER', 'UNDO'}
	
	typein: BoolProperty(name="Type In:",default=True)
	count: IntProperty(name="Count",min=0,default=0)
	squeeze: FloatProperty(name="Squeeze",min=0,max=1,default=0)
	bias: FloatProperty(name="Bias",min=-1,max=1,default=0)
	shift: FloatProperty(name="Shift",min=-1,max=1,default=0)

	def apply(self):
		curve = self.curve
		curve.restore()

		for selection in curve.selection('segment'):
			spline = curve.splines[selection[0]]
			selection[1].sort(reverse=True)
			count = self.count+1
			scale = 1-self.squeeze
			offset = self.squeeze/2 + self.shift
			for index in selection[1]:
				times = [offset+get_bias(self.bias,t/count)*scale for t in range(1,count)]
				spline.multi_division(index, times)

		self.canceled = (self.count == 0)
		curve.update()

	def draw(self, ctx):
		layout = self.layout
		col = layout.column(align=True)
		col.prop(self,"count")
		col.prop(self,"squeeze")
		col.prop(self,"bias")
		col.prop(self,"shift")
	
	def self_report(self):
		self.report({'OPERATOR'},'bpy.ops.curve.divid_plus()')



class Curve_OT_Refine(Operator):
	bl_idname = "curve.refine"
	bl_label = "Refine"
	obj, curve = None, None
	new_point_added = False

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			if len(ctx.scene.objects) > 0:
				if ctx.object != None:
					return ctx.mode == 'EDIT_CURVE'
		return False

	def get_nearest_point_on_line(self, line, point):
		intersect = intersect_point_line(point, line[0], line[1])
		return intersect[0]

	def get_nearest_point(self, points):
		if points:
			nearest_point = points[0]
			for point in points:
				if point.distance < nearest_point.distance:
					nearest_point = point
		return nearest_point
	
	def divide_segment(self, ctx, segment, statr_time, end_time, count, coord):
		statr_time = 0 if statr_time < 0 else statr_time
		end_time = 1 if end_time > 1 else end_time
		step = (end_time - statr_time) / count
		points = []
		for i in range(count):
			time = statr_time + i * step
			point_on_curve = self.obj.matrix_world @ segment.get_point_on(time)
			point_on_view = region_2d_to_location_3d(ctx.region, ctx.space_data.region_3d, coord, point_on_curve)
			distance = get_distance(point_on_curve, point_on_view)
			points.append(Point(segment, time, distance, point_on_view))
		return points
	
	def modal(self, ctx, event):
		ctx.area.tag_redraw()
		x,y = event.mouse_region_x, event.mouse_region_y
	
		if ctx.mode != 'EDIT_CURVE':
			return {'CANCELLED'}

		if not event.type in {'LEFTMOUSE', 'RIGHTMOUSE', 'MOUSEMOVE', 'ESC'}:
			return {'PASS_THROUGH'}
		
		elif event.type == 'MOUSEMOVE':
			# if vert created:
			# 	slide on the segment or spline
			# else:
			# 	pass
			pass

		elif event.type == 'LEFTMOUSE':
			if event.value == 'PRESS':
				self.new_point_added = False
				self.curve = Curve(self.obj)
				""" Divide each segment to 10 part and collect distance from click point """
				points = []
				for spline in self.curve.splines:
					for segment in spline.get_as_segments():
						points += self.divide_segment(ctx, segment, 0, 1, 10, (x,y))

				nearest_point = self.get_nearest_point(points)

				""" second division steps """
				for step in {0.1, 0.01, 0.001}:
					points.clear()
					start_time, end_time = nearest_point.time - step, nearest_point.time + step
					points = self.divide_segment(ctx, nearest_point.segment, start_time, end_time, 10, (x,y))
					nearest_point = self.get_nearest_point(points)

				""" get nearest point of curve on 2d screen """
				nearest_point_on_curve = self.obj.matrix_world @ nearest_point.segment.get_point_on(nearest_point.time)
				pl = location_3d_to_region_2d(ctx.region, ctx.space_data.region_3d, nearest_point_on_curve)

				""" insert if distance les than 10 pixel """
				if abs(x-pl.x) < 10 and abs(y-pl.y) < 10:
					nearest_point.segment.spline.divid(nearest_point.segment.index, nearest_point.time)
					self.new_point_added = True

			if event.value =='RELEASE' and self.new_point_added:
				""" Update and Get new genarated curve data """
				self.curve.update()
				bpy.ops.ed.undo_push()
			
			return {'RUNNING_MODAL'}

		elif event.type in {'RIGHTMOUSE','ESC'}:
			return {'CANCELLED'}

		return {'RUNNING_MODAL'}
	
	def invoke(self, ctx, event):
		self.obj = ctx.active_object
		self.curve = Curve(self.obj)
		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}


classes = [Curve_OT_divid_plus, Curve_OT_Refine]

def register_divid():
	[bpy.utils.register_class(c) for c in classes]

def unregister_divid():
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_divid()