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
# 2024/06/22

from bpy.types import Operator
from bpy.props import BoolProperty, FloatProperty
from bpy.utils import register_class, unregister_class

from bsmax.curve import (
	get_curve_object_selection,
	curve_merge_gaps_by_distance,
	spline_merge_bezier_points_by_distance,
	spline_make_first,
	curve_break_point
)


class Curve_OT_Break(Operator):
	bl_idname = 'curve.break'
	bl_label = "Break"
	bl_description = ""
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return ctx.mode == 'EDIT_CURVE'
		return False

	def execute(self, ctx):
		curve = ctx.object
		selection = get_curve_object_selection(curve, 'point')
		for spline, points in selection:
			curve_break_point(curve, spline, points)
		return{'FINISHED'}


class Curve_OT_Make_First(Operator):
	bl_idname = 'curve.make_first'
	bl_label = "Make First"
	bl_description = "Make selected point First point of curve"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return ctx.mode == 'EDIT_CURVE'
		return False

	def execute(self, ctx):
		curve = ctx.object
		selection = get_curve_object_selection(curve, 'point')
		for spline_index, points in selection:
			if len(points) != 1:
				continue
			spline = curve.data.splines[spline_index]
			spline_make_first(spline, points[0])
		return{'FINISHED'}


class Curve_OT_Merge_By_Distance(Operator):
	bl_idname = 'curve.merge_by_distance'
	bl_label = "Merge by distance"
	bl_description = ""
	bl_options = {'REGISTER', 'UNDO'}
	
	value: FloatProperty(
		name="distance:", unit='LENGTH', min=0.0, default=0.0001
	) # type: ignore

	selected_only: BoolProperty(name="Selected only", default=True) # type: ignore
	gaps_only: BoolProperty(name="Gaps only", default=True) # type: ignore

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return ctx.mode == 'EDIT_CURVE'
		return False

	def draw(self, _):
		col = self.layout.column()
		col.prop(self, 'value')
		col.prop(self, 'selected_only')
		col.prop(self, 'gaps_only')

	def execute(self, ctx):
		curve = ctx.object
		curve_merge_gaps_by_distance(
			curve, self.value, self.selected_only
		)

		if self.gaps_only:
			return{'FINISHED'}
		
		for spline in curve.data.splines:
			spline_merge_bezier_points_by_distance(
				spline, self.value, self.selected_only
			)

		return{'FINISHED'}


classes = {
	Curve_OT_Merge_By_Distance,
	Curve_OT_Break,
	Curve_OT_Make_First
}


def register_weld():
	for cls in classes:
		register_class(cls)


def unregister_weld():
	for cls in classes:
		unregister_class(cls)


if __name__ == '__main__':
	register_weld()