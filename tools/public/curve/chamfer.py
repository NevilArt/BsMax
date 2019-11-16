import bpy, numpy, copy, math
from bpy.types import Operator, Menu
from mathutils import Vector
from bpy.props import BoolProperty, FloatProperty
from bsmax.math import get_segment_length, split_segment, get_3_points_angle, point_on_line

class Point:
	def __init__(self, point):
		self.select_left_handle = point.select_left_handle
		self.select_right_handle = point.select_right_handle
		self.select_control_point = point.select_control_point
		self.hide = point.hide
		self.handle_left_type = point.handle_left_type
		self.handle_right_type = point.handle_right_type
		self.handle_left = Vector(point.handle_left)
		self.co = Vector(point.co)
		self.handle_right = Vector(point.handle_right)
		self.tilt = point.tilt
		self.weight_softbody = point.weight_softbody
		self.radius = point.radius

	def get_bezier_point(self, bezier_point):
		bezier_point.select_left_handle = self.select_left_handle
		bezier_point.select_right_handle = self.select_right_handle
		bezier_point.select_control_point = self.select_control_point
		bezier_point.hide = self.hide
		bezier_point.handle_left_type = self.handle_left_type
		bezier_point.handle_right_type = self.handle_right_type
		bezier_point.handle_left = self.handle_left
		bezier_point.co = self.co
		bezier_point.handle_right = self.handle_right
		bezier_point.tilt = self.tilt
		bezier_point.weight_softbody = self.weight_softbody
		bezier_point.radius = self.radius

class Spline:
	def __init__(self, spline):
		self.points = []
		self.bezier_points = []
		self.tilt_interpolation = spline.tilt_interpolation
		self.radius_interpolatio = spline.radius_interpolation
		self.type = spline.type
		self.point_count_u = spline.point_count_u
		self.point_count_v = spline.point_count_v
		self.order_u = spline.order_u
		self.order_v = spline.order_v
		self.resolution_u = spline.resolution_u
		self.resolution_v = spline.resolution_v
		self.use_cyclic_u = spline.use_cyclic_u
		self.use_cyclic_v = spline.use_cyclic_v
		self.use_endpoint_u = spline.use_endpoint_u
		self.use_endpoint_v = spline.use_endpoint_v
		self.use_bezier_u = spline.use_bezier_u
		self.use_bezier_v = spline.use_bezier_v
		self.use_smooth = spline.use_smooth
		self.hide = spline.hide
		self.material_index = spline.material_index
		self.character_index = spline.character_index
		self.read_bezier_points(spline)

	def read_bezier_points(self, spline):
		for bp in spline.bezier_points:
			self.bezier_points.append(Point(bp))
	
	def insert(self, index, point):
		self.bezier_points.insert(index, point)

	def remove(self, index):
		self.bezier_points.pop(index)

	def create_new_spline(self, data):
		spline = data.splines.new(self.type)
		spline.bezier_points.add(len(self.bezier_points) - 1)
		for i in range(len(self.bezier_points)):
			point = self.bezier_points[i]
			point.get_bezier_point(spline.bezier_points[i])
		spline.tilt_interpolation = self.tilt_interpolation
		#spline.radius_interpolatio = self.radius_interpolation
		#spline.point_count_u = self.point_count_u
		#spline.point_count_v = self.point_count_v
		spline.order_u = self.order_u
		spline.order_v = self.order_v
		spline.resolution_u = self.resolution_u
		spline.resolution_v = self.resolution_v
		spline.use_cyclic_u = self.use_cyclic_u
		spline.use_cyclic_v = self.use_cyclic_v
		spline.use_endpoint_u = self.use_endpoint_u
		spline.use_endpoint_v = self.use_endpoint_v
		spline.use_bezier_u = self.use_bezier_u
		spline.use_bezier_v = self.use_bezier_v
		spline.use_smooth = self.use_smooth
		spline.hide = self.hide
		spline.material_index = self.material_index
		#spline.character_index = self.character_index

class Shape:
	def __init__(self, obj, splines):
		self.obj = obj
		self.splines = []
		self.read_splines(splines)

	def read_splines(self, splines):
		for spline in splines:
			self.splines.append(Spline(spline))

	def deepcopy(self):
		NewShape = Shape(self.obj, [])
		for spline in self.splines:
			newspline = copy.deepcopy(spline)
			NewShape.splines.append(newspline)
		return NewShape

	def create_shape(self):
		self.obj.data.splines.clear()
		for spline in self.splines:
			spline.create_new_spline(self.obj.data)

class BsMax_OT_CurveChamfer(Operator):
	bl_idname = "curve.chamfer"
	bl_label = "Fillet/Chamfer (Curve)"
	fillet: BoolProperty(name="Fillet:",default = False)
	value: FloatProperty(name="Value:",unit='LENGTH')
	typein: BoolProperty(name="Type In:",default = False)
	start = False
	finish = False
	obj = None
	shape = None
	start_y = 0

	def get_data(self, ctx):
		self.obj = ctx.active_object
		self.shape = Shape(self.obj, self.obj.data.splines)

	def get_left_index(self, spline, index):
		left = index - 1
		if index == 0:
			left = len(spline.bezier_points) - 1 if spline.use_cyclic_u else index
		return left

	def get_rigth_index(self, spline, index):
		right = index + 1
		if index >= len(spline.bezier_points) - 1:
			right = 0 if spline.use_cyclic_u else index
		return right

	def chamfer(self):
		shape = self.shape.deepcopy()
		selection = []
		for i in range(len(shape.splines)):
			for j in range(len(shape.splines[i].bezier_points)):
				point = shape.splines[i].bezier_points[j]
				if point.select_control_point:
					selection.append([i, j, point])

		for i, j, point in reversed(selection):
			left = self.get_left_index(shape.splines[i], j)
			right = self.get_rigth_index(shape.splines[i], j)

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

def camfer_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("curve.chamfer", text="Chamfer/Fillet").typein=True
		
def chamfer_cls(register):
	c = BsMax_OT_CurveChamfer
	if register: 
		bpy.utils.register_class(c)
		bpy.types.VIEW3D_MT_edit_curve_ctrlpoints.append(camfer_menu)
	else:
		bpy.types.VIEW3D_MT_edit_curve_ctrlpoints.remove(camfer_menu)
		bpy.utils.unregister_class(c)

if __name__ == '__main__':
	chamfer_cls(True)

__all__ = ["chamfer_cls"]