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
from tools.public.curve.operator import CurveTool

class BsMax_OT_CurveBreak(Operator):
	bl_idname = "curve.break"
	bl_label = "Break (Curve)"
	bl_options = {'REGISTER','UNDO'}

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
		return{"FINISHED"}

class BsMax_OT_MakeFirst(Operator):
	bl_idname = "curve.makefirst"
	bl_label = "Make First (Curve)"
	bl_options = {'REGISTER','UNDO'}

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
		return{"FINISHED"}

class BsMax_OT_CurveMergeByDistance(CurveTool):
	bl_idname = "curve.mergebydistance"
	bl_label = "Merge by distance"
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
		layout = self.layout
		col = layout.column()
		col.prop(self,"value")
		col.prop(self,"selectedonly")
		col.prop(self,"gapsonly")

classes = [BsMax_OT_CurveMergeByDistance, BsMax_OT_CurveBreak, BsMax_OT_MakeFirst]

def register_weld():
	[bpy.utils.register_class(c) for c in classes]

def unregister_weld():
	[bpy.utils.unregister_class(c) for c in classes]