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
from bpy.props import BoolProperty, FloatProperty
from bsmax.math import get_distance
from bsmax.curve import Curve, Spline
from bsmax.operator import CurveTool

class Curve_OT_Break(Operator):
	bl_idname = "curve.break"
	bl_label = "Break"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			if len(ctx.scene.objects) > 0:
				if ctx.object != None:
					return ctx.mode == 'EDIT_CURVE'
		return False

	def execute(self, ctx):
		curve = Curve(ctx.active_object)
		for spline, points in curve.selection("point"):
			curve.break_point(spline, points)
		curve.update()

		self.report({'OPERATOR'},'bpy.ops.curve.break()')
		return{"FINISHED"}

class Curve_OT_Make_First(Operator):
	bl_idname = "curve.make_first"
	bl_label = "Make First"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			if len(ctx.scene.objects) > 0:
				if ctx.object != None:
					return ctx.mode == 'EDIT_CURVE'
		return False

	def execute(self, ctx):
		curve = Curve(ctx.active_object)
		for splineindex, points in curve.selection("point"):
			if len(points) == 1:
				spline = curve.splines[splineindex]
				spline.make_first(points[0])
		curve.update()
		
		self.report({'OPERATOR'},'bpy.ops.curve.make_first()')
		return{"FINISHED"}

class Curve_OT_Merge_By_Distance(CurveTool):
	bl_idname = "curve.merge_by_distance"
	bl_label = "Merge by distance"
	bl_options = {'REGISTER', 'UNDO'}
	
	singleaction = True
	typein: BoolProperty(name="Type In:",default=True)
	value: FloatProperty(name="distance:",unit='LENGTH',default=0.0001,min=0.0)
	selectedonly: BoolProperty(name="Selected only:",default=True)
	gapsonly: BoolProperty(name="Gaps only:",default=True)

	def get_data(self, ctx):
		self.obj = ctx.active_object
		self.curve = Curve(self.obj)

	def apply(self):
		curve = self.curve
		curve.restore()
		curve.merge_gaps_by_distance(self.value, self.selectedonly)
		if not self.gapsonly:
			for spline in curve.splines:
				spline.merge_points_by_distance(self.value, self.selectedonly)
		curve.update()

	def draw(self, ctx):
		col = self.layout.column()
		col.prop(self,"value")
		col.prop(self,"selectedonly")
		col.prop(self,"gapsonly")
	
	def self_report(self):
		self.report({'OPERATOR'},'bpy.ops.curve.merge_by_distance()')

classes = [Curve_OT_Merge_By_Distance, Curve_OT_Break, Curve_OT_Make_First]

def register_weld():
	[bpy.utils.register_class(c) for c in classes]

def unregister_weld():
	[bpy.utils.unregister_class(c) for c in classes]