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
from bpy.props import FloatProperty, EnumProperty
from bsmax.curve import (
	get_curve_object_selection,
	get_splines_intersection_points,
	collect_splines_divisions,
	get_inout_segments,
	curve_delete_segments,
	curve_merge_gaps_by_distance
)


def curve_boolean(curve, spline1, spline2, mode, tollerance):

	intersections = get_splines_intersection_points(spline1, spline2, tollerance)
	divisions = collect_splines_divisions(intersections)

	for division in divisions:
		for division_segment in division.segments:
			division.spline.multi_division(
				division_segment.index,
				division_segment.times,
				cos=division_segment.cos
			)

	inner1, outer1 = get_inout_segments(spline1, spline2)
	inner2, outer2 = get_inout_segments(spline2, spline1)

	if mode == 'UNION':
		curve_delete_segments(curve, spline1, inner1)
		curve_delete_segments(curve, spline2, inner2)

	elif mode == 'INTERSECTION':
		curve_delete_segments(curve, spline1, outer1)
		curve_delete_segments(curve, spline2, outer2)

	elif mode == 'DIFFERENCE':
		curve_delete_segments(curve, spline1, inner1)
		curve_delete_segments(curve, spline2, outer2)
	
	elif mode == 'CUT':
		pass

	curve_merge_gaps_by_distance(curve, 0.0001, False)


def apply_curve_boolean(curve, mode, tollerance):
	selected_splines = get_curve_object_selection(curve, 'close')
	active_spline = curve.data.splines.active

	if len(selected_splines) < 2 or not active_spline:
		return
	
	if active_spline in selected_splines:
		selected_splines.remove(active_spline)

	for spline in selected_splines:
		curve_boolean(curve, active_spline, spline, mode, tollerance)


class Curve_OT_Boolean(Operator):
	bl_idname = 'curve.boolean'
	bl_label = "Boolean"
	bl_description = "Curve Boolean tool"
	bl_options = {'REGISTER', 'UNDO'}
	
	mode: EnumProperty(
		name="Mode",
		items=[
			(
				'UNION', "Union", "Make Union",
				'SELECT_EXTEND', 1
			),
			(
				'SUBTRACT', "Subtract", "Subtract",
				'SELECT_SUBTRACT', 2
			),
			(
				'INTERSECTION', "Intersection", "Keep Intersection",
				'SELECT_INTERSECT', 3
			),
			(
				'DIFFERENCE', "Difference", "Keep Difrence",
				'SELECT_DIFFERENCE', 4
			),
			(
				'CUT', "Cut", "Only Cut on collision point",
				'SELECT_SET', 5
			) 
		],
		default='UNION'
	) # type: ignore

	tollerance: FloatProperty(
		name="tollerance:", unit='LENGTH',
		min=0.0000000000001, max=1,
		default=0.000001
	) # type: ignore

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return ctx.mode == 'EDIT_CURVE'
		return False

	def draw(self, _):
		layout = self.layout
		col = layout.column()
		col.prop(self, 'mode', expand=True)
		layout.prop(self, 'tollerance')

	def execute(self, ctx):
		for curve in ctx.selected_objects:
			apply_curve_boolean(curve, self.mode, self.tollerance)
		return{'FINISHED'}


def register_boolean():
	bpy.utils.register_class(Curve_OT_Boolean)


def unregister_boolean():
	bpy.utils.unregister_class(Curve_OT_Boolean)

if __name__ == '__main__':
	register_boolean()