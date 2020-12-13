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
from bpy.props import BoolProperty, FloatProperty, IntProperty
from bsmax.curve import Curve
from bsmax.operator import CurveTool

class BsMax_OT_OutlineCurve(CurveTool):
	bl_idname = "curve.outline"
	bl_label = "Outline (Curve)"
	bl_options = {'REGISTER', 'UNDO'}
	
	typein: BoolProperty(name="Type In:",default=False)
	value: FloatProperty(name="Value:",unit='LENGTH')
	close: BoolProperty(name="Close:",default=True)
	count: IntProperty(name="Count:",default=1,min=0)
	mirror: BoolProperty(name="Mirror:",default=False)

	def apply(self):
		curve = self.curve
		curve.restore()

		if not self.typein:
			self.value = self.value_y
		if self.value != 0:
			for i in curve.selection('spline'):
				curve.splines[i].set_free()
				count = 1 if self.close else self.count
				for j in range(count):
					value = self.value * (j+1)
					newspline = curve.clone(i)
					newspline.select(False)
					newspline.offset(value)
					if self.mirror and not self.close:
						mirrorspline = curve.clone(i)
						mirrorspline.select(False)
						mirrorspline.offset(-value)
						curve.splines.append(mirrorspline)
					if not curve.splines[i].use_cyclic_u and self.close:
						newspline.reverse()
						curve.join(i,newspline)
						curve.splines[i].use_cyclic_u = True
					else:
						curve.splines.append(newspline)

		self.canceled = (self.value == 0)
		curve.update()

	def draw(self, ctx):
		layout = self.layout
		col = layout.column(align=True)
		col.prop(self,"value")
		col.prop(self,"close")
		if not self.close:
			col.prop(self,"count")
			col.prop(self,"mirror")
	
	def self_report(self):
		self.report({'OPERATOR'},'bpy.ops.curve.outline()')

def register_outline():
	bpy.utils.register_class(BsMax_OT_OutlineCurve)

def unregister_outline():
	bpy.utils.unregister_class(BsMax_OT_OutlineCurve)