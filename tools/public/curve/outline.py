import bpy, numpy
from bpy.types import Operator
from bpy.props import BoolProperty, FloatProperty
from copy import deepcopy
from mathutils import Vector
from bsmax.math import (get_distance, get_segment_length, point_on_line,
						get_spline_left_index, get_spline_rigth_index)
from bsmax.data import Shape

from math import sin, cos, atan, sqrt, degrees, pi, atan2

def get_2_points_3d_normal(p1, p2):
	a = p1.y-p2.y
	b = p2.x-p1.x
	#c = p2.z-p1.z
	d1 = atan2(b,a)
	#d2 = atan2(a,c)
	x,y,z = cos(d1),sin(d1),0
	return Vector((x,y,z))

def get_side_position_ofset(p1, p2, val):
	return get_2_points_3d_normal(p1,p2)*val

def get_corner_position_ofset(p1, p2, p3, val):
	# TODO fix this mis calculation
	offset = get_side_position_ofset(p1,p2,val)
	offset += get_side_position_ofset(p2,p3,val)
	return offset

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
					p1 = points[index].co
					p2 = points[right].co
					point.co += get_side_position_ofset(p1,p2,self.value)
				elif hasleft and hasright:
					# TODO fix this mis calculation
					p1 = points[left].co
					p2 = points[index].co
					p3 = points[right].co
					ofset = get_corner_position_ofset(p1,p2,p3,self.value)
					point.co += ofset
					nslpoint = newspline.bezier_points[left].co
					d1 = get_distance(p1,p2)
					d2 = get_distance(nslpoint,point.co)
					scale = d2/d1
					newpos = point.handle_left+ofset
					point.handle_left = point_on_line(point.co,newpos,scale)
					newpos = point.handle_right+ofset
					point.handle_right = point_on_line(point.co,newpos,scale)
				elif hasleft and not hasright:				
					p1 = points[left].co
					p2 = points[index].co
					point.co += get_side_position_ofset(p1,p2,self.value)
			if close:
				shape.splines.append(newspline)
			else:
				# note 4 point tangent most turn to corner
				for point in reversed(newspline.bezier_points):
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