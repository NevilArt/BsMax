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
from bpy.props import BoolProperty,IntProperty,FloatProperty
from bsmax.math import get_bias
from .operator import CurveTool

class BsMax_OT_dividplus(CurveTool):
	bl_idname = "curve.dividplus"
	bl_label = "Divid plus"
	typein: BoolProperty(name="Type In:",default=True)
	count: IntProperty(name="Count",min=0,default=0)
	squeeze: FloatProperty(name="Squeeze",min=0,max=1,default=0)
	bias: FloatProperty(name="Bias",min=-1,max=1,default=0)
	shift: FloatProperty(name="Shift",min=-1,max=1,default=0)

	def apply(self):
		curve = self.curve
		curve.restore()

		# splines = curve.splines
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

def register_divid():
	bpy.utils.register_class(BsMax_OT_dividplus)

def unregister_divid():
	bpy.utils.unregister_class(BsMax_OT_dividplus)