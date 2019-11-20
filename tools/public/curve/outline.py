import bpy, numpy
from bpy.types import Operator
from bpy.props import BoolProperty, FloatProperty
from copy import deepcopy
from mathutils import Vector
from bsmax.math import (get_distance, get_segment_length, point_on_line,
						get_spline_left_index, get_spline_rigth_index)
from bsmax.data import Shape

from math import sin, cos, atan, sqrt, degrees, pi, atan2

def get_2_points_2d_normal(p1, p2):
	a,b = p1.y-p2.y, p2.x-p1.x
	d = atan2(b,a)
	x,y = cos(d),sin(d)
	return Vector((x,y,0))

def get_side_offset(p1, p2, val):
	return get_2_points_2d_normal(p1,p2)*val

def get_intersection_of_2_lines(p1,p2,p3,p4):
	d = ((p1.x-p2.x)*(p3.y-p4.y)-(p1.y-p2.y)*(p3.x-p4.x))
	d = 0.000000000000001 if d == 0 else d
	x=((p1.x*p2.y-p1.y*p2.x)*(p3.x-p4.x)-(p1.x-p2.x)*(p3.x*p4.y-p3.y*p4.x))/d
	y=((p1.x*p2.y-p1.y*p2.x)*(p3.y-p4.y)-(p1.y-p2.y)*(p3.x*p4.y-p3.y*p4.x))/d
	return x,y

def get_corner_offset(p1, p2, p3, val):
	o1 = get_side_offset(p1,p2,val)
	o2 = get_side_offset(p2,p3,val)
	lp1 = Vector((p1.x+o1.x, p1.y+o1.y, 0))
	lp2 = Vector((p2.x+o1.x, p2.y+o1.y, 0))
	lp3 = Vector((p2.x+o2.x, p2.y+o2.y, 0))
	lp4 = Vector((p3.x+o2.x, p3.y+o2.y, 0))
	x,y = get_intersection_of_2_lines(lp1,lp2,lp3,lp4)
	x -= p2.x
	y -= p2.y
	return Vector((x,y,0))

def get_corner_position(p1, p2, p3, val):
	o1 = get_side_offset(p1,p2,val)
	o2 = get_side_offset(p2,p3,val)
	lp1 = Vector((p1.x+o1.x, p1.y+o1.y, 0))
	lp2 = Vector((p2.x+o1.x, p2.y+o1.y, 0))
	lp3 = Vector((p2.x+o2.x, p2.y+o2.y, 0))
	lp4 = Vector((p3.x+o2.x, p3.y+o2.y, 0))
	x,y = get_intersection_of_2_lines(lp1,lp2,lp3,lp4)
	return Vector((x,y,0))

class BsMax_OT_OutlineCurve(Operator):
	bl_idname = "curve.outlinecurve"
	bl_label = "Outline (Curve)"

	typein: BoolProperty(name="Type In:",default = False)
	value: FloatProperty(name="Value:",unit='LENGTH')
	shape,obj = None,None
	start,finish = False,False
	start_y = 0

	def get_data(self, ctx):
		self.obj = ctx.active_object
		self.shape = Shape(self.obj, self.obj.data.splines)

	def outline(self):
		shape = self.shape.deepcopy()
		selection = []
		for i in range(len(shape.splines)):
			for j in range(len(shape.splines[i].bezier_points)):
				point = shape.splines[i].bezier_points[j]
				if point.select_control_point:
					selection.append(i)
					break
		for i in selection:
			spline = shape.splines[i]
			close = spline.use_cyclic_u
			points = spline.bezier_points
			newspline = deepcopy(shape.splines[i])			
			for index in range(len(points)):
				# check for start and end of spline
				hasleft = True if close else (index > 0)
				hasright = True if close else (index < len(points) - 1)

				# get nex and previews besier point index
				left = get_spline_left_index(newspline, index)
				right = get_spline_rigth_index(newspline, index)

				point = newspline.bezier_points[index]
				# dis select the new created segment
				point.select_left_handle = False
				point.select_right_handle = False
				point.select_control_point = False

				if not hasleft and hasright:
					point.handle_left_type = 'VECTOR'
					points[index].handle_left_type = 'VECTOR'
					point.handle_right_type = 'FREE'
					points[index].handle_right_type = 'FREE'

					p1 = points[index].co
					p2 = points[index].handle_right
					p3 = points[right].handle_left

					point.co += get_side_offset(p1,p2,self.value)
					point.handle_right = get_corner_position(p1,p2,p3,self.value)
					
				elif hasleft and hasright:
					point.handle_left_type = 'FREE'
					point.handle_right_type = 'FREE'

					p0 = points[left].handle_right
					p1 = points[index].handle_left
					p2 = points[index].co
					p3 = points[index].handle_right
					p4 = points[right].handle_left

					point.handle_left = get_corner_position(p0,p1,p2,self.value)
					point.co = get_corner_position(p1,p2,p3,self.value)
					point.handle_right = get_corner_position(p2,p3,p4,self.value)

				elif hasleft and not hasright:
					points[index].handle_left_type = 'FREE'
					point.handle_left_type = 'FREE'
					point.handle_right_type = 'VECTOR'
					points[index].handle_right_type = 'VECTOR'

					p0 = points[left].handle_right
					p1 = points[index].handle_left
					p2 = points[index].co
					
					point.handle_left = get_corner_position(p0,p1,p2,self.value)
					point.co += get_side_offset(p1,p2,self.value)

			if close:
				shape.splines.append(newspline)
			else:
				for point in reversed(newspline.bezier_points):
					left = point.handle_right
					right = point.handle_left
					ltype = point.handle_right_type
					rtype = point.handle_left_type
					point.handle_left = left
					point.handle_right = right
					point.handle_left_type = ltype
					point.handle_right_type = rtype
					shape.splines[i].bezier_points.append(point)
				spline.use_cyclic_u = True
		shape.create_shape()

	def abort(self):
		if self.shape != None:
			self.shape.create_shape()

	def execute(self, ctx):
		if self.value == 0:
			self.abort()
		else:
			self.outline()
		return{"FINISHED"}

	def check(self, ctx):
		if not self.start:
			self.start = True
			self.get_data(ctx)
		self.outline()

	def draw(self, ctx):
		layout = self.layout
		col = layout.column(align=True)
		col.prop(self,"value",text="Value")

	def modal(self, ctx, event):
		if event.type == 'LEFTMOUSE':
			if not self.start:
				self.start = True
				self.start_y = event.mouse_y
				self.get_data(ctx)
		if event.type == 'MOUSEMOVE':
			if self.start:
				scale = (event.mouse_y - self.start_y)
				self.value = scale / 200
				self.outline()
			if self.start and event.value =='RELEASE':
				self.finish = True
		if self.finish:
			if self.value == 0:
				self.abort()
			return {'CANCELLED'}
		if event.type in {'RIGHTMOUSE', 'ESC'}:
			self.abort()
			return {'CANCELLED'}
		return {'RUNNING_MODAL'}

	def invoke(self, ctx, event):
		if self.typein:
			wm = ctx.window_manager
			return wm.invoke_props_dialog(self, width=120)
		else:
			ctx.window_manager.modal_handler_add(self)
			return {'RUNNING_MODAL'}

def outline_cls(register):
	c = BsMax_OT_OutlineCurve
	if register:
		bpy.utils.register_class(c)
	else:
		bpy.utils.unregister_class(c)

if __name__ == '__main__':
	outline_cls(True)

__all__ = ["outline_cls"]