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
from bpy.props import BoolProperty,FloatProperty,EnumProperty
from bsmax.curve import Curve
from bsmax.operator import CurveTool

class Curve_OT_Boolean(CurveTool):
	bl_idname = "curve.boolean"
	bl_label = "Boolean"
	bl_options = {'REGISTER', 'UNDO'}
	
	singleaction = True
	typein: BoolProperty(name="Type In:",default=False)
	advance: BoolProperty(name="advance:",default=False)
	value: FloatProperty(name="tollerance:",unit='LENGTH',default=0.000001, min=0.0000000000001, max=1)
	mode: EnumProperty(name='Type',default='UNION',
		items=[('UNION','Union',''),
		('INTERSECTION','Intersection',''),
		('DIFFERENCE','Difference',''),
		('CUT','Cut','') ])

	def get_data(self, ctx):
		self.obj = ctx.active_object
		self.curve = Curve(self.obj)

	def apply(self):
		curve = self.curve
		curve.restore()

		# splines = curve.splines
		indexes = curve.selection('close')
		active = curve.active()
		index1, index2 = None, None
		if active != None and len(indexes) == 2:
			index1 = active
			index2 = indexes[0] if indexes[0] != active else indexes[1]
		elif len(indexes) == 2:
			index1 = indexes[0]
			index2 = indexes[1]
		if len(indexes) == 2:
			curve.boolean(index1, index2, self.mode, self.value)
		curve.update()

	def draw(self, ctx):
		layout = self.layout
		col = layout.column()
		col.prop(self,"mode")
		col.prop(self,"advance")
		if self.advance:
			col = layout.column(align=True)
			col.prop(self,"value")
	
	def self_report(self):
		self.report({'OPERATOR'},'bpy.ops.curve.boolean()')

def register_boolean():
	bpy.utils.register_class(Curve_OT_Boolean)

def unregister_boolean():
	bpy.utils.unregister_class(Curve_OT_Boolean)