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
# 2024/06/20

import bpy

from bpy.types import Operator
from bpy.props import BoolProperty, IntProperty, FloatProperty
from bpy.utils import register_class, unregister_class

from mathutils.geometry import intersect_point_line
from bpy_extras.view3d_utils import region_2d_to_location_3d, location_3d_to_region_2d

from bsmax.math import get_bias, get_distance
from bsmax.curve import (
    get_curve_object_selection,
	get_spline_as_segments,
	spline_multi_division,
	spline_divid
)


def get_nearest_point_on_line(line, point):
	intersect = intersect_point_line(point, line[0], line[1])
	return intersect[0]


def get_nearest_point(points):
	if not points:
		return

	nearest_point = points[0]
	for point in points:
		if point.distance < nearest_point.distance:
			nearest_point = point

	return nearest_point


def divide_segment(curve, ctx, segment, statr_time, end_time, count, coord):
	statr_time = 0 if statr_time < 0 else statr_time
	end_time = 1 if end_time > 1 else end_time
	step = (end_time - statr_time) / count

	points = []
	for i in range(count):
		time = statr_time + i * step
		point_on_curve = curve.matrix_world @ segment.get_point_on(time)
		point_on_view = region_2d_to_location_3d(
			ctx.region, ctx.space_data.region_3d, coord, point_on_curve
		)

		distance = get_distance(point_on_curve, point_on_view)
		points.append(Point(segment, time, distance, point_on_view))

	return points


def curve_refinde_modal(cls, ctx, event):
	ctx.area.tag_redraw()
	x, y = event.mouse_region_x, event.mouse_region_y
	curve = cls.curve

	if ctx.mode != 'EDIT_CURVE':
		return {'CANCELLED'}

	if not event.type in {'LEFTMOUSE', 'RIGHTMOUSE', 'MOUSEMOVE', 'ESC'}:
		return {'PASS_THROUGH'}
	
	if event.type == 'MOUSEMOVE':
		# if vert created:
		# 	slide on the segment or spline
		# else:
		# 	pass
		pass

	if event.type in {'RIGHTMOUSE', 'ESC'}:
		return {'CANCELLED'}

	if event.type != 'LEFTMOUSE':
		return {'RUNNING_MODAL'}

	if event.value == 'PRESS':
		cls.new_point_added = False

		# Divide each segment to 10 part and collect distance from click point
		points = []
		for spline in curve.data.splines:
			for segment in get_spline_as_segments(spline):
				points += divide_segment(curve, ctx, segment, 0, 1, 10, (x,y))

		nearest_point = get_nearest_point(points)

		# Second division steps
		for step in {0.1, 0.01, 0.001}:
			points.clear()
			start_time = nearest_point.time - step
			end_time = nearest_point.time + step
			points = divide_segment(
				curve, ctx, nearest_point.segment, start_time, end_time, 10, (x,y)
			)
			nearest_point = get_nearest_point(points)

		# Get nearest point of curve on 2d screen
		point_on_segment = nearest_point.segment.get_point_on(nearest_point.time)
		nearest_point_on_curve = curve.matrix_world @ point_on_segment
		point_location = location_3d_to_region_2d(
			ctx.region, ctx.space_data.region_3d, nearest_point_on_curve
		)

		# Insert if distance les than 10 pixel
		if abs(x - point_location.x) < 10 and abs(y - point_location.y) < 10:
			spline_divid(
				nearest_point.segment.spline,
				nearest_point.segment.index,
				nearest_point.time
			)
			# nearest_point.segment.spline.divid(
			# 	nearest_point.segment.index, nearest_point.time
			# )
			cls.new_point_added = True

	# Update and Get new genarated curve data
	if event.value =='RELEASE' and cls.new_point_added:
		bpy.ops.ed.undo_push()
	
	return {'RUNNING_MODAL'}


class Point:
	def __init__(self, segment, time, distance, point_on_view):
		self.segment = segment
		self.time = time
		self.distance = distance
		self.point_on_view = point_on_view


class Curve_OT_divid_plus(Operator):
	bl_idname = 'curve.divid_plus'
	bl_label = "Divid plus"
	bl_description = ""
	bl_options = {'REGISTER', 'UNDO'}
	
	typein: BoolProperty(name="Type In:", default=True) # type: ignore
	count: IntProperty(name="Count", min=0, default=0) # type: ignore
	squeeze: FloatProperty(
		name="Squeeze", min=0, max=1, default=0
	) # type: ignore
	
	bias: FloatProperty(name="Bias", min=-1, max=1, default=0) # type: ignore
	shift: FloatProperty(name="Shift", min=-1, max=1, default=0) # type: ignore

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return ctx.mode == 'EDIT_CURVE'
		return False
	
	def draw(self, _):
		layout = self.layout
		col = layout.column(align=True)
		col.prop(self, 'count')
		col.prop(self, 'squeeze')
		col.prop(self, 'bias')
		col.prop(self, 'shift')

	def execute(self, ctx):
		curve = ctx.object
		count = self.count + 1
		selected_segments = get_curve_object_selection(curve, 'segment')

		for selection in selected_segments:
			spline = curve.data.splines[selection[0]]
			selection[1].sort(reverse=True)
			# count = self.count + 1
			scale = 1 - self.squeeze
			offset = self.squeeze/2 + self.shift
			for index in selection[1]:
				times = [
					offset + get_bias(self.bias, t/count) \
						* scale for t in range(1, count)
				]
				spline_multi_division(spline, index, times)

		return{'FINISHED'}


class Curve_OT_Refine(Operator):
	bl_idname = "curve.refine"
	bl_label = "Refine"
	bl_description = ""
	bl_options = {'REGISTER', 'UNDO'}

	curve = None
	new_point_added = False

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return ctx.mode == 'EDIT_CURVE'
		return False
	
	def modal(self, ctx, event):
		return curve_refinde_modal(self, ctx, event)
	
	def invoke(self, ctx, _):
		self.curve = ctx.object
		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}


classes = {
	Curve_OT_divid_plus,
	Curve_OT_Refine
}


def register_divid():
	for cls in classes:
		register_class(cls)


def unregister_divid():
	for cls in classes:
		unregister_class(cls)


if __name__ == '__main__':
	register_divid()