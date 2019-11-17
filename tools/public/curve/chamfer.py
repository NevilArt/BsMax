import bpy#, numpy, copy, math
from bpy.types import Operator
from mathutils import Vector
from bpy.props import BoolProperty, FloatProperty
from bsmax.data import Point,Spline,Shape
from bsmax.math import (get_segment_length, split_segment, get_3_points_angle, point_on_line,
						get_spline_left_index, get_spline_rigth_index)

class BsMax_OT_CurveChamfer(Operator):
	bl_idname = "curve.chamfer"
	bl_label = "Fillet/Chamfer (Curve)"
	fillet: BoolProperty(name="Fillet:",default = False)
	value: FloatProperty(name="Value:",unit='LENGTH')
	typein: BoolProperty(name="Type In:",default = False)
	start,finish = False,False
	shape,obj = None,None
	start_y = 0

	def get_data(self, ctx):
		self.obj = ctx.active_object
		self.shape = Shape(self.obj, self.obj.data.splines)

	def chamfer(self):
		shape = self.shape.deepcopy()
		selection = []
		for i in range(len(shape.splines)):
			for j in range(len(shape.splines[i].bezier_points)):
				point = shape.splines[i].bezier_points[j]
				if point.select_control_point:
					selection.append([i, j, point])

		for i, j, point in reversed(selection):
			left = get_spline_left_index(shape.splines[i], j)
			right = get_spline_rigth_index(shape.splines[i], j)

			point_start = shape.splines[i].bezier_points[left]
			point_center = shape.splines[i].bezier_points[j] 
			point_end = shape.splines[i].bezier_points[right]

			value = abs(self.value)

			segment1 = [point_start]
			segment1.append(point_center)
			a1 = segment1[0].co
			b1 = segment1[0].handle_right
			c1 = segment1[1].handle_left
			d1 = segment1[1].co
			length1 = get_segment_length(a1, b1, c1, d1, 100)
			val = value if value <= length1 else length1
			t1 = 1 - (val / length1)

			segment2 = [point_center]
			segment2.append(point_end)
			a2 = segment2[0].co
			b2 = segment2[0].handle_right
			c2 = segment2[1].handle_left
			d2 = segment2[1].co
			length2 = get_segment_length(a2, b2, c2, d2, 100)
			val = value if value <= length2 else length2
			t2 = val / length2

			l = split_segment(a1, b1, c1, d1, t1)
			r = split_segment(a2, b2, c2, d2, t2)

			a = r[2]
			c = Vector(point_center.co)
			b = l[4]
			angle = get_3_points_angle(a, c, b)

			# not a perfect solution
			t = 0.551786 * (angle / 1.5708) # 1.5708 = rad(90)

			f1 = point_on_line(a, c, t)
			f2 = point_on_line(b, c, t)

			point_0 = l[0]#
			out_0 = l[1]#
			in_1 = r[4]
			point_1 = r[3]#
			out_1 = f1 # Flet arc
			in_2 = f2 # Flet arc
			point_2 = l[3]#
			out_2 = l[2]#
			in_3 = r[5]#
			point_3 = r[6]#

			handle_type = 'FREE' if self.fillet else 'VECTOR'

			NewPoint = Point(point)
			point_start.handle_right_type = 'FREE'
			point_start.handle_right = out_0

			point.handle_right_type = 'FREE'
			point.handle_right = in_1
			point.co = point_1
			point.handle_left = out_1 # make filet arc
			point.handle_left_type = handle_type

			NewPoint.handle_right = in_2 # make filet arc
			NewPoint.handle_right_type = handle_type
			NewPoint.co = point_2
			NewPoint.handle_left = out_2
			NewPoint.handle_left_type = 'FREE'

			point_end.handle_left_type = "FREE"
			point_end.handle_left = in_3

			shape.splines[i].bezier_points.insert(j, NewPoint)

		shape.create_shape()

	def abort(self):
		if self.shape != None:
			self.shape.create_shape()

	def execute(self, ctx):
		if self.value == 0:
			self.abort()
		else:
			self.chamfer()
		return {'FINISHED'}

	def check(self, ctx):
		if not self.start:
			self.start = True
			self.get_data(ctx)
		self.chamfer()

	def draw(self, ctx):
		layout = self.layout
		icon = 'SPHERECURVE' if self.fillet else 'LINCURVE'
		text = "Fillet" if self.fillet else "Chamfer"
		col = layout.column(align=True)
		col.prop(self,"fillet",text=text, icon=icon)
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
				self.chamfer()
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

def chamfer_cls(register):
	c = BsMax_OT_CurveChamfer
	if register: 
		bpy.utils.register_class(c)
	else:
		bpy.utils.unregister_class(c)

if __name__ == '__main__':
	chamfer_cls(True)

__all__ = ["chamfer_cls"]