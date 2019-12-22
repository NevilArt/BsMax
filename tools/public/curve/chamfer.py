import bpy
from bpy.props import BoolProperty, FloatProperty
from bsmax.curve import Curve
from .operator import CurveTool

class BsMax_OT_CurveChamfer(CurveTool):
	bl_idname = "curve.chamfer"
	bl_label = "Fillet/Chamfer (Curve)"
	fillet: BoolProperty(name="Fillet:",default=False)
	value: FloatProperty(name="Value:",unit='LENGTH',min=0)
	typein: BoolProperty(name="Type In:",default=False)

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
		text = "Fillet" if self.fillet else "Chamfer"
		col = layout.column(align=True)
		col.prop(self,"fillet",text=text, icon=icon)
		col.prop(self,"value",text="Value")


def chamfer_cls(register):
	c = BsMax_OT_CurveChamfer
	if register: 
		bpy.utils.register_class(c)
	else:
		bpy.utils.unregister_class(c)

if __name__ == '__main__':
	chamfer_cls(True)

__all__ = ["chamfer_cls"]