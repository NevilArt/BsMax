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
from bpy.props import BoolProperty, FloatProperty
# from bsmax.curve import Curve
from bsmax.operator import CurveTool

class Curve_OT_Chamfer(CurveTool):
	bl_idname = 'curve.chamfer'
	bl_label = 'Fillet/Chamfer'
	bl_options = {'REGISTER', 'UNDO'}
	
	fillet: BoolProperty(name='Fillet:', default=False)
	value: FloatProperty(name='Value:', unit='LENGTH', min=0)
	typein: BoolProperty(name='Type In:', default=False)

	def apply(self):
		curve = self.curve
		curve.restore()

		value = abs(self.value) if self.typein else abs(self.value_y)
		tention = 0.5 if self.fillet else 0

		for i, sel in curve.selection('point'):
			curve.splines[i].chamfer(sel, value, tention)
		
		self.canceled = (self.value == 0)
		curve.update()

	def draw(self, ctx):
		layout = self.layout
		icon = 'SPHERECURVE' if self.fillet else 'LINCURVE'
		text = 'Fillet' if self.fillet else 'Chamfer'
		col = layout.column(align=True)
		col.prop(self, 'fillet', text=text, icon=icon)
		col.prop(self, 'value', text='Value')

def register_chamfer():
	bpy.utils.register_class(Curve_OT_Chamfer)

def unregister_chamfer():
	bpy.utils.unregister_class(Curve_OT_Chamfer)