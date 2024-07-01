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
# 2024/06/21

import bpy

from bpy.types import Operator
from bpy.props import BoolProperty, FloatProperty, IntProperty

from bsmax.curve import (
	get_curve_object_selection,
	spline_set_free,
	spline_clone,
	spline_reverse,
	spline_join,
	spline_remove,
	spline_offset,
	spline_select
)


def curve_outline(
		curve, value:float, close:bool, mirror:bool, count:int
	):

	if curve.type != 'CURVE':
		return

	if value == 0:
		return

	for spline in get_curve_object_selection(curve, 'spline'):

		spline_set_free(spline)
		clone_count = 1 if close else count

		for clone_index in range(clone_count):
			value = value * (clone_index + 1)
			newspline = spline_clone(curve, spline)
			spline_select(newspline, False)
			spline_offset(newspline, value)

			if mirror and not close:
				mirror_spline = spline_clone(curve, spline)
				spline_select(mirror_spline, False)
				spline_offset(mirror_spline, -value)

			if not spline.use_cyclic_u and close:
				spline_reverse(newspline)
				spline_join(spline, newspline)
				spline_remove(curve, newspline)
				spline.use_cyclic_u = True


class Curve_OT_Outline(Operator):
	bl_idname = 'curve.outline'
	bl_label = "Outline (Curve)"
	bl_description = "Curve Outline"
	bl_options = {'REGISTER', 'UNDO'}
	
	value: FloatProperty(
		name="Value:", unit='LENGTH'
	) # type: ignore

	close: BoolProperty(
		name="Close:", default=True
	) # type: ignore

	count: IntProperty(
		name="Count:", default=1, min=0
	) # type: ignore

	mirror: BoolProperty(
		name="Mirror:", default=False
	) # type: ignore

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return ctx.mode == 'EDIT_CURVE'
		return False

	def draw(self, _):
		layout = self.layout
		col = layout.column(align=True)
		col.prop(self, 'value')
		col.prop(self, 'close')

		if not self.close:
			col.prop(self, 'count')
			col.prop(self, 'mirror')
	
	def execute(self, ctx):
		for curve in ctx.selected_objects:
			curve_outline(
				curve, self.value, self.close, self.mirror, self.count
			)

		return{'FINISHED'}


def register_outline():
	bpy.utils.register_class(Curve_OT_Outline)


def unregister_outline():
	bpy.utils.unregister_class(Curve_OT_Outline)