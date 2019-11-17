import bpy, numpy, math
from mathutils import Vector
from copy import deepcopy

class Knot:
	in_type = ""
	invec = Vector((0,0,0))
	co = Vector((0,0,0))
	out_type = ""
	outvec = Vector((0,0,0))

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
			newspline = deepcopy(spline)
			NewShape.splines.append(newspline)
		return NewShape

	def create_shape(self):
		self.obj.data.splines.clear()
		for spline in self.splines:
			spline.create_new_spline(self.obj.data)

__all__ = ["Knot", "Point", "Spline", "Shape"]