import bpy
from bpy.types import Operator
from bpy.props import BoolProperty, FloatProperty

def remove_doubles(ctx, distance):
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
				if dot.select_control_point and dot1.select_control_point and (i!=0 or spline.use_cyclic_u):   
					if (dot.co-dot1.co).length < distance:
						# remove points and recreate hangles
						dot1.handle_right_type = "FREE"
						dot1.handle_right = dot.handle_right
						dot1.co = (dot.co + dot1.co) / 2
						dellist.append(dot)
					else:
						# Handles that are on main point position converts to vector,
						# if next handle are also vector
						if dot.handle_left_type == 'VECTOR' and (dot1.handle_right - dot1.co).length < distance:
							dot1.handle_right_type = "VECTOR"
						if dot1.handle_right_type == 'VECTOR' and (dot.handle_left - dot.co).length < distance:
							dot.handle_left_type = "VECTOR"  
	bpy.ops.curve.select_all(action = 'DESELECT')
	for dot in dellist:
		dot.select_control_point = True
	count = len(dellist)
	bpy.ops.curve.delete(type = 'VERT')
	bpy.ops.curve.select_all(action = 'SELECT')

class BsMax_OT_CurveMergeByDistance(Operator):
	bl_idname = "curve.mergebydistance"
	bl_label = "Merge by Distance"
	bl_options = {'REGISTER','UNDO'}
	distance: FloatProperty(name="Distance",min=0,default=0.1)
	selected: BoolProperty(name="Selected",default=True)
	connected: BoolProperty(name="Connected",default=True)
	typein: BoolProperty(name="Type in",default=False)

	def execute(self, ctx):
		remove_doubles(ctx, self.distance)
		return {'FINISHED'}

def weld_cls(register):
	classes = [BsMax_OT_CurveMergeByDistance]
	if register: 
		[bpy.utils.register_class(c) for c in classes]
	else: 
		[bpy.utils.unregister_class(c) for c in classes]

if __name__ == '__main__':
	weld_cls(True)

__all__ = ["weld_cls"]