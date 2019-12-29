import bpy
from bpy.types import Operator
from bpy.props import BoolProperty, FloatProperty
from bsmax.math import get_distance
from bsmax.curve import Curve, Spline
from itertools import product
from tools.public.curve.operator import CurveTool

##############################################################################
def merge_points_by_distance(ctx, distance):
	dellist = []
	for spline in ctx.active_object.data.splines: 
		if len(spline.bezier_points) > 1:
			for i in range(0, len(spline.bezier_points)): 
				if i == 0:
					ii = len(spline.bezier_points) - 1
				else:        
					ii = i - 1
				dot = spline.bezier_points[i];
				dot1 = spline.bezier_points[ii];   
				while dot1 in dellist and i != ii:
					ii -= 1
					if ii < 0: 
						ii = len(spline.bezier_points)-1
					dot1 = spline.bezier_points[ii]
				if dot.select_control_point and\
				   dot1.select_control_point and\
				   (i!=0 or spline.use_cyclic_u):   
					if (dot.co-dot1.co).length < distance:
						# remove points and recreate hangles
						dot1.handle_right_type = "FREE"
						dot1.handle_right = dot.handle_right
						dot1.co = (dot.co + dot1.co) / 2
						dellist.append(dot)
					else:
						# Handles that are on main point position converts to vector,
						# if next handle are also vector
						if dot.handle_left_type == 'VECTOR' and\
						   (dot1.handle_right - dot1.co).length < distance:
							dot1.handle_right_type = "VECTOR"
						if dot1.handle_right_type == 'VECTOR' and\
						   (dot.handle_left - dot.co).length < distance:
							dot.handle_left_type = "VECTOR"  
	bpy.ops.curve.select_all(action = 'DESELECT')
	for dot in dellist:
		dot.select_control_point = True
	count = len(dellist)
	bpy.ops.curve.delete(type = 'VERT')
	bpy.ops.curve.select_all(action = 'SELECT')
##############################################################################

class BsMax_OT_CurveBreak(Operator):
	bl_idname = "curve.break"
	bl_label = "Break (Curve)"
	bl_options = {'REGISTER','UNDO'}

	def execute(self, ctx):
		curve = Curve(ctx.active_object)
		for spline, points in curve.selection("point"):
			curve.break_point(spline, points)
		curve.update()
		return{"FINISHED"}

class BsMax_OT_CurveMergeByDistance(CurveTool):
	bl_idname = "curve.mergebydistance"
	bl_label = "Merge by distance"
	singleaction = True
	typein: BoolProperty(name="Type In:",default=True)
	value: FloatProperty(name="distance:",unit='LENGTH',default=0.0001, min=0.0)
	selectedonly: BoolProperty(name="Selected only:",default=True)
	gapsonly: BoolProperty(name="Gaps only:",default=True)

	def get_data(self, ctx):
		self.obj = ctx.active_object
		self.curve = Curve(self.obj)

	def apply(self):
		curve = self.curve
		curve.restore()
		curve.merge_gaps_by_distance(self.value, self.selectedonly)
		curve.update()

	def draw(self, ctx):
		layout = self.layout
		col = layout.column()
		col.prop(self,"value")
		col.prop(self,"selectedonly")
		#col.prop(self,"gapsonly")

def weld_cls(register):
	classes = [BsMax_OT_CurveMergeByDistance, BsMax_OT_CurveBreak]
	if register: 
		[bpy.utils.register_class(c) for c in classes]
	else: 
		[bpy.utils.unregister_class(c) for c in classes]

if __name__ == '__main__':
	weld_cls(True)

__all__ = ["weld_cls"]