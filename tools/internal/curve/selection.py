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
from bpy.props import EnumProperty, FloatProperty, IntProperty
from bpy.utils import register_class, unregister_class


def set_spline_select(spline, state):
	for bezier_points in spline.bezier_points:
		bezier_points.select_left_handle = state
		bezier_points.select_control_point = state
		bezier_points.select_right_handle = state


def deselect_all_splines(curve):
	for spline in curve.data.splines:
			set_spline_select(spline, False)


def select_curve_by_length(cls, curve):
	if curve.type != 'CURVE':
		return
	
	if cls.mode == 'SET':
		deselect_all_splines(curve)

	state = cls.mode != 'SUB' #{'SET', 'EXTEND'}

	for spline in curve.data.splines:
		length = spline.calc_length()

		if cls.by == 'GREATER':
			if length > cls.length:
				set_spline_select(spline, state)

		elif cls.by == 'LESS':
			if length < cls.length:
				set_spline_select(spline, state)

		elif cls.by == 'EQUAL':
			min_length = cls.length - cls.length_tolerans
			max_length = cls.length + cls.length_tolerans
			if min_length < length <= max_length:
				set_spline_select(spline, state)


def select_splines_by_points_count(cls, curve):
	if curve.type != 'CURVE':
		return
	
	if cls.mode == 'SET':
		deselect_all_splines(curve)

	state = cls.mode != 'SUB' #{'SET', 'EXTEND'}

	for spline in curve.data.splines:
		count = len(spline.bezier_points)
		state = False
		if cls.by == 'GREATER':
			if count > cls.count:
				set_spline_select(spline, state)
		
		elif cls.by == 'LESS':
			if count < cls.count:
				set_spline_select(spline, state)
		
		elif cls.by == 'EQUAL':
			min_count = cls.count - cls.count_tolerans
			max_count = cls.count + cls.count_tolerans
			if min_count < count < max_count:
				set_spline_select(spline, state)


def select_splines_by_close(cls, curve):
	if curve.type != 'CURVE':
		return
	
	if cls.mode == 'SET':
		for spline in curve.data.splines:
			set_spline_select(spline, False)

	state = cls.mode != 'SUB' #{'SET', 'EXTEND'}
	
	for spline in curve.data.splines:
		if cls.collect == 'OPEN':
			if not spline.use_cyclic_u:
				set_spline_select(spline, state)
		
		elif cls.collect == 'CLOSE':
			if spline.use_cyclic_u:
				set_spline_select(spline, state)


def draw_curve_select_by_ui(cls):
	layout = cls.layout

	if cls.method == 'LENGTH':
		row = layout.row()
		row.prop(cls, 'by', expand=True)

		row = layout.row()
		row.prop(cls, 'length')

		if cls.by == 'EQUAL':
			row.prop(cls, 'length_tolerans')

	elif cls.method == 'COUNT':
		row = layout.row()
		row.prop(cls, 'by', expand=True)
		
		row = layout.row()
		row.prop(cls, 'count')

		if cls.by == 'EQUAL':
			row.prop(cls, 'count_tolerans')

	if cls.method == 'CLOSE':
		row = layout.row()
		row.prop(cls, 'collect', expand=True)
		
	row = layout.row()
	row.prop(cls, 'mode', expand=True)


class Curve_OT_Select_By(Operator):
	bl_idname = 'curve.select_by'
	bl_label = "Select By"
	bl_description = "Select splines by Length, Count or Close"
	bl_options = {'REGISTER', 'UNDO'}

	method: EnumProperty(
		name = 'Method',
		items=[
			('LENGTH', "Length", "By Spline Length"),
			('COUNT', "Count", "By Segment Count"),
			('CLOSE', "Colse", "Close or Open")
		],
		default='LENGTH'
	) # type: ignore

	mode: EnumProperty(
		name = 'Mode',
		items=[
			('SET', "Set", "Set selection", 'SELECT_SET', 1),
			('EXTEND', "Extend", "Extend to selection", 'SELECT_EXTEND', 2),
			('SUB', "Subtract", "Subtract From Selection", 'SELECT_SUBTRACT', 3)
		],
		default='SET'
	) # type: ignore

	by: EnumProperty(
		name = 'By',
		items=[
			('GREATER', "Greater then", "Greater then", 'ALIGN_RIGHT', 1),
			('EQUAL', "Equal to", "Equal to", 'ALIGN_JUSTIFY', 2),
			('LESS', "Less than", "Less than", 'ALIGN_CENTER', 3)
		],
		default='GREATER'
	) # type: ignore


	count: IntProperty(name="Count", min= 2, default=3) # type: ignore
	count_tolerans: IntProperty(default=1, min=1) # type: ignore

	length: FloatProperty(unit='LENGTH', default=1.0, min=0) # type: ignore
	length_tolerans: FloatProperty(
		unit='LENGTH', default=0.01, min=0
	) # type: ignore

	collect: EnumProperty(
		name = 'Collect',
		items=[
			('OPEN', "Open", "Collect Open Splines", 'OUTLINER_DATA_CURVE', 1),
			('CLOSE', "Close", "Collect Close Splines", 'OUTLINER_DATA_MESH', 2)
		],
		default='CLOSE'
	) # type: ignore

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return ctx.mode == 'EDIT_CURVE'
		return False
	
	def draw(self, _):
		draw_curve_select_by_ui(self)

	def execute(self, ctx):
		if self.method == 'LENGTH':
			for curve in ctx.selected_objects:
				select_curve_by_length(self, curve)

		elif self.method == 'COUNT':
			for curve in ctx.selected_objects:
				select_splines_by_points_count(self, curve)

		elif self.method == 'CLOSE':
			for curve in ctx.selected_objects:
				select_splines_by_close(self, curve)

		return{'FINISHED'}


def selection_menu(self, _):
	layout = self.layout
	layout.separator()
	layout.operator(
		'curve.select_by', text="Select By Length"
	).method='LENGTH'
	
	layout.operator(
		'curve.select_by', text="Select By Segment Count"
	).method='COUNT'

	layout.operator(
		'curve.select_by', text="Selecy Close"
	).method='CLOSE'


def register_selection():
	register_class(Curve_OT_Select_By)
	bpy.types.VIEW3D_MT_select_edit_curve.append(selection_menu)


def unregister_selection():
	bpy.types.VIEW3D_MT_select_edit_curve.remove(selection_menu)
	unregister_class(Curve_OT_Select_By)


if __name__ == '__main__':
	register_selection()