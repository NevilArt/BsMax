import bpy
from bpy.props import *
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

		splines = curve.splines
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

def divid_cls(register):
	c = BsMax_OT_dividplus
	if register: 
		bpy.utils.register_class(c)
	else:
		bpy.utils.unregister_class(c)

if __name__ == '__main__':
	divid_cls(True)

__all__ = ["divid_cls"]