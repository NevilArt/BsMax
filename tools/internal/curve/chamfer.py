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
# 2024/06/23

import bpy

from mathutils import Vector
from math import pi
from bpy.types import Operator
from bpy.props import FloatProperty, EnumProperty

from bsmax.curve import (
	Spline, BezierPoint,
	get_next_index_on_spline,
	get_spline_segment_length,
	split_segment,
	get_3_points_angle_3d,
	point_on_line,
	curve_append
)


def spline_chamfer(spline, indexs:list, value:float, tention:float):
	# TODO need to optimize and add tention functinality
	new_spline = Spline(spline)

	for index in reversed(indexs):
		point_selected = new_spline.bezier_points[index]
		left = get_next_index_on_spline(spline, index, riverce=True)
		right = get_next_index_on_spline(spline, index)

		# igonor points on head and taile of sline
		if left == index or right == index:
			continue

		point_start = spline.bezier_points[left]
		point_center = spline.bezier_points[index]
		point_end = spline.bezier_points[right]

		segment1 = [point_start, point_center]
		a1 = segment1[0].co
		b1 = segment1[0].handle_right
		c1 = segment1[1].handle_left
		d1 = segment1[1].co
		length1 = get_spline_segment_length(spline, left)

		val = value if value <= length1 else length1
		#TODO if left bezierpoint selected devide val/2
		t1 = 1 - (val / length1) if length1 != 0 else 0

		segment2 = [point_center, point_end]
		a2 = segment2[0].co
		b2 = segment2[0].handle_right
		c2 = segment2[1].handle_left
		d2 = segment2[1].co
		length2 = get_spline_segment_length(spline, index)

		val = value if value <= length2 else length2
		#TODO if right bezierpoint selected devide val/2
		t2 = val / length2 if length2 != 0 else 1

		left_segment = split_segment(a1, b1, c1, d1, t1)
		right_segment = split_segment(a2, b2, c2, d2, t2)

		start_point = right_segment[2] #center_in
		center_point = Vector(point_center.co)
		end_point = left_segment[4] #center_uot
		angle = get_3_points_angle_3d(start_point, center_point, end_point)

		# not a perfect solution
		time = 0.551786 * (angle / (pi / 2))

		fillet_in = point_on_line(start_point, center_point, time)
		fillet_out = point_on_line(end_point, center_point, time)

		# point_0_co = left_segment[0]
		point_0_out = left_segment[1]

		point_1_in = right_segment[4]
		point_1_co = right_segment[3]
		point_1_out = fillet_in # Flet arc

		point_2_in = fillet_out # Flet arc
		point_2_co = left_segment[3]
		point_2_out = left_segment[2]

		point_3_in = right_segment[5]
		# point_3_co = right_segment[6]#

		handle_type = 'FREE' if tention > 0 else 'VECTOR'
		
		# left point co not changed but handel changed
		# point_start.co = point_0_co #unchanged
		point_start.handle_right_type = 'FREE'
		point_start.handle_right = point_0_out

		# selected point moves to new posiotion
		point_selected.handle_right_type = 'FREE'
		point_selected.handle_right = point_1_in
		point_selected.co = point_1_co
		point_selected.handle_left = point_1_out # make filet arc
		point_selected.handle_left_type = handle_type

		# selected point clone added after selected one
		# new clone move to next posiotion
		point_new = BezierPoint(point_selected)
		point_new.handle_right = point_2_in # make filet arc
		point_new.handle_right_type = handle_type
		point_new.co = point_2_co
		point_new.handle_left = point_2_out
		point_new.handle_left_type = 'FREE'

		# right point co not changed but handele  changed
		point_end.handle_left_type = "FREE"
		point_end.handle_left = point_3_in
		# point_end.co = point_3_co #unchanged

		new_spline.bezier_points.insert(index, point_new)
	
	return new_spline


class Curve_OT_Chamfer(Operator):
	bl_idname = 'curve.chamfer'
	bl_label = "Fillet/Chamfer"
	bl_description = ""
	bl_options = {'REGISTER', 'UNDO'}
	
	mode: EnumProperty(
		name="Mode",
		items=[
			('FILLET', "Fillet", "Fillet Curve", 'LINCURVE', 1),
			('CHAMFER', "Chamfer", "Chamfer Curve", 'SPHERECURVE', 2),
		]
	) # type: ignore
	
	value: FloatProperty(
		name="Value:", unit='LENGTH', min=0
	) # type: ignore
	
	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return ctx.mode == 'EDIT_CURVE'
		return False

	def draw(self, _):
		layout = self.layout
		col = layout.column(align=True)
		row = col.row()
		row.prop(self, 'mode', expand=True)
		col.prop(self, 'value', text='Value')

	def execute(self, ctx):
		curve = ctx.object
		value = abs(self.value)
		tention = 0.5 if self.mode=='CHAMFER' else 0

		new_splines = []
		for spline in curve.data.splines:
			indexes = []
			for index, bezier_point in enumerate(spline.bezier_points):
				if bezier_point.select_control_point:
					indexes.append(index)

			new_spline = spline_chamfer(spline, indexes, value, tention)
			new_splines.append(new_spline)

		curve.data.splines.clear()
		for spline in new_splines:
			curve_append(curve, spline)

		return{'FINISHED'}


def register_chamfer():
	bpy.utils.register_class(Curve_OT_Chamfer)


def unregister_chamfer():
	bpy.utils.unregister_class(Curve_OT_Chamfer)


if __name__ == '__main__':
	register_chamfer()