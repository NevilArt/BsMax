import bpy
from bpy.props import *
from bsmax.curve import Curve
#from .operator import CurveTool
from tools.public.curve.operator import CurveTool

class BsMax_OT_BooleanCurve(CurveTool):
	bl_idname = "curve.boolean"
	bl_label = "Boolean"
	singleaction = True
	typein: BoolProperty(name="Type In:",default=False)
	advance: BoolProperty(name="advance:",default=False)
	value: FloatProperty(name="tollerance:",unit='LENGTH',default=0.001, min=0.000001, max=1)
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

		splines = curve.splines
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
			#curve.merge_gaps_by_distance(0.00001)
		curve.update()
		# temprary solution
		# bpy.ops.curve.mergebydistance('INVOKE_DEFAULT')

	def draw(self, ctx):
		layout = self.layout
		col = layout.column()
		col.prop(self,"mode")
		col.prop(self,"advance")
		if self.advance:
			col = layout.column(align=True)
			col.prop(self,"value")

def boolean_cls(register):
	classes = [BsMax_OT_BooleanCurve]
	if register: 
		[bpy.utils.register_class(c) for c in classes]
	else: 
		[bpy.utils.unregister_class(c) for c in classes]

if __name__ == '__main__':
	boolean_cls(True)

__all__ = ["boolean_cls"]