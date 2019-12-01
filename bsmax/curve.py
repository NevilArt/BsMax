import bpy, numpy, math
from mathutils import Vector
from copy import deepcopy
from math import sin, cos, atan2, pi, sqrt
from bsmax.math import (get_3_points_angle_2d,get_lines_intersection,split_segment,point_on_line,
	point_on_vector,get_distance,get_3_points_angle_3d,get_segment_length)

def get_line_offset(p1, p2, val):
	a,b = p1.y-p2.y, p2.x-p1.x
	d = atan2(b,a)
	x,y = cos(d),sin(d)
	return Vector((x,y,0))*val

def get_corner_position(p1, p2, p3, val):
	teta = get_3_points_angle_2d(p1, p2, p3)
	if False:#(pi - abs(teta)) < 0.001:
		o3 = get_line_offset(p1,p3,val)
		position = o3 + p2
	else:
		o1 = get_line_offset(p1,p2,val)
		o2 = get_line_offset(p2,p3,val)
		lp1 = Vector((p1.x+o1.x, p1.y+o1.y, 0))
		lp2 = Vector((p2.x+o1.x, p2.y+o1.y, 0))
		lp3 = Vector((p2.x+o2.x, p2.y+o2.y, 0))
		lp4 = Vector((p3.x+o2.x, p3.y+o2.y, 0))
		position = get_lines_intersection(lp1,lp2,lp3,lp4)
	if position == None:
		# avod the not spected errores
		position = o1 + p2
	return position

def get_curve_selection_index(curve, mode):
	selection = []
	if mode == 'point':
		for i, spline in enumerate(curve.splines):
			sel = []
			for j, point in enumerate(spline.bezier_points):
				if point.select_control_point:
					sel.append(j)
			if len(sel) > 0:
				selection.append([i,sel])
	elif mode == 'segment':
		for i, spline in enumerate(curve.splines):
			sel = []
			count = len(spline.bezier_points)
			for j in range(count):
				k = j + 1
				if k >= count:
					if spline.use_cyclic_u:
						k = -1
					else:
						break
				point1 = spline.bezier_points[j].select_control_point
				point2 = spline.bezier_points[k].select_control_point
				if point1 and point2:
					sel.append([j,k])
			if len(sel) > 0:
				selection.append([i,sel])
	elif mode == 'spline':
		for i, spline in enumerate(curve.splines):
			istrue = True
			for point in spline.bezier_points:
				if not point.select_control_point:
					istrue = False
					break
			if istrue:
				selection.append(i)
	elif mode == 'close':
		for i, spline in enumerate(curve.splines):
			if not spline.use_cyclic_u:
				break
			istrue = True
			for point in spline.bezier_points:
				if not point.select_control_point:
					istrue = False
					break
			if istrue:
				selection.append(i)
	return selection

def get_curve_activespline_index(curve):
	splines = curve.splines
	active = splines.active
	for i, spline in enumerate(curve.splines):
		if spline == active:
			return i
	return None

class Bezier_point:
	def __init__(self, bpoint):
		if bpoint != None:
			self.select_left_handle = bpoint.select_left_handle
			self.select_right_handle = bpoint.select_right_handle
			self.select_control_point = bpoint.select_control_point
			self.hide = bpoint.hide
			self.handle_left_type = bpoint.handle_left_type
			self.handle_right_type = bpoint.handle_right_type
			self.handle_left = Vector(bpoint.handle_left)
			self.co = Vector(bpoint.co)
			self.handle_right = Vector(bpoint.handle_right)
			self.tilt = bpoint.tilt
			self.weight_softbody = bpoint.weight_softbody
			self.radius = bpoint.radius
		else:
			self.select_left_handle = False
			self.select_right_handle = False
			self.select_control_point = False
			self.hide = False
			self.handle_left_type = 'VECTOR'
			self.handle_right_type = 'VECTOR'
			self.handle_left = Vector((0,0,0))
			self.co = Vector((0,0,0))
			self.handle_right = Vector((0,0,0))
			self.tilt = 0
			self.weight_softbody = 0.001
			self.radius = 1

	def get_bezier_point(self, bezier_point):
		bezier_point.hide = self.hide
		bezier_point.tilt = self.tilt
		bezier_point.radius = self.radius
		bezier_point.co = self.co
		bezier_point.handle_left_type = self.handle_left_type
		bezier_point.handle_right_type = self.handle_right_type
		bezier_point.handle_left = self.handle_left
		bezier_point.handle_right = self.handle_right
		bezier_point.select_left_handle = self.select_left_handle
		bezier_point.select_control_point = self.select_control_point
		bezier_point.select_right_handle = self.select_right_handle
		bezier_point.weight_softbody = self.weight_softbody

class Segment:
	def __init__(self, spline, indexs):
		self.spline = spline
		self.a = spline.bezier_points[indexs[0]].co
		self.b = spline.bezier_points[indexs[0]].handle_right
		self.c = spline.bezier_points[indexs[1]].handle_left
		self.d = spline.bezier_points[indexs[1]].co
		self.cuts = []
	def split(self, divide):
		self.cuts = [point_on_vector(self.a,self.b,self.c,self.d,self.t) for t in range(divide)]
	def length(self, divide):
		return get_segment_length(self.a,self.b,self.c,self.d,divide)

class Spline:
	def __init__(self, spline):
		self.points = []
		self.bezier_points = self.get_bezier_points(spline)
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

	def get_bezier_points(self, spline):
		return [Bezier_point(bp) for bp in spline.bezier_points]

	def get_left_index(self, index):
		left = index - 1
		if index == 0:
			return len(self.bezier_points) - 1 if self.use_cyclic_u else index
		return left

	def get_rigth_index(self, index):
		right = index + 1
		if index >= len(self.bezier_points) - 1:
			right = 0 if self.use_cyclic_u else index
		return right

	def get_segment_length(self, index, steps=100):
		if index <= len(self.bezier_points)-2:
			a = self.bezier_points[index].co
			b = self.bezier_points[index].handle_right
			c = self.bezier_points[index+1].handle_left
			d = self.bezier_points[index+1].co
			points = [a]
			s = 1 / steps
			for i in range(1, steps + 1):
				t = i * s
				p = point_on_vector(a, b, c, d, t)
				points.append(p)
			lenght = 0
			for i in range(len(points) - 1):
				lenght += get_distance(points[i], points[i - 1])
			return lenght
			#bpy.context.active_object.data.splines[0].calc_length()
		return 0

	def set_free(self, full=False):
		if len(self.bezier_points) > 0:
			if full:
				for point in self.bezier_points:
					point.handle_left_type = 'FREE'
					point.handle_right_type = 'FREE'
			if not self.use_cyclic_u:
				ps,pe = self.bezier_points[0], self.bezier_points[-1]
				ps.handle_left_type = 'VECTOR'
				if ps.handle_right_type in {'AUTO','ALIGNED'}:
					ps.handle_right_type = 'FREE'
				if ps.handle_left_type in {'AUTO','ALIGNED'}:
					pe.handle_left_type = 'FREE'
				pe.handle_right_type = 'VECTOR'

	def append(self, bezier_points):
		self.bezier_points.append(bezier_points)

	def prepend(self, bezier_points):
		self.bezier_points.prepend(bezier_points)
	
	def insert(self, index, bezier_points):
		self.bezier_points.insert(index, bezier_points)

	def join(self, spline):
		for point in spline.bezier_points:
			self.bezier_points.append(point)

	def remove(self, index):
		self.bezier_points.pop(index)

	def reverse(self):
		bezier_points = deepcopy(self.bezier_points)
		self.bezier_points.clear()
		for point in reversed(bezier_points):
			ltype = point.handle_right_type
			rtype = point.handle_left_type
			left = point.handle_right
			right = point.handle_left
			point.handle_left = left
			point.handle_right = right
			point.handle_left_type = ltype
			point.handle_right_type = rtype
			self.bezier_points.append(point)

	def select(self, select):
		for point in self.bezier_points:
			point.select_left_handle = select
			point.select_right_handle = select
			point.select_control_point = select

	def create(self, data):
		newspline = data.splines.new(self.type)
		newspline.bezier_points.add(len(self.bezier_points) - 1)
		for i in range(len(self.bezier_points)):
			point = self.bezier_points[i]
			point.get_bezier_point(newspline.bezier_points[i])
		newspline.tilt_interpolation = self.tilt_interpolation
		#newspline.radius_interpolatio = self.radius_interpolation
		#newspline.point_count_u = self.point_count_u
		#newspline.point_count_v = self.point_count_v
		newspline.order_u = self.order_u
		newspline.order_v = self.order_v
		newspline.resolution_u = self.resolution_u
		newspline.resolution_v = self.resolution_v
		newspline.use_cyclic_u = self.use_cyclic_u
		newspline.use_cyclic_v = self.use_cyclic_v
		newspline.use_endpoint_u = self.use_endpoint_u
		newspline.use_endpoint_v = self.use_endpoint_v
		newspline.use_bezier_u = self.use_bezier_u
		newspline.use_bezier_v = self.use_bezier_v
		newspline.use_smooth = self.use_smooth
		newspline.hide = self.hide
		newspline.material_index = self.material_index
		#newspline.character_index = self.character_index

	def offset(self, value):
		points = self.bezier_points
		refpoints = deepcopy(points)
		for index, point in enumerate(points):
			# check for start and end of spline
			hasleft = True if self.use_cyclic_u else (index > 0)
			hasright = True if self.use_cyclic_u else (index < len(points) - 1)

			# get nex and previews besier point index
			left = self.get_left_index(index)
			right = self.get_rigth_index(index)

			p0 = refpoints[left].handle_right
			p1 = refpoints[index].handle_left
			p2 = refpoints[index].co
			p3 = refpoints[index].handle_right
			p4 = refpoints[right].handle_left

			if not hasleft and hasright:
				point.co += get_line_offset(p2,p3,value)
				if point.handle_right_type != 'VECTOR':
					point.handle_right = get_corner_position(p2,p3,p4,value)
					
			elif hasleft and hasright:
				if point.handle_left_type != 'VECTOR':
					point.handle_left = get_corner_position(p0,p1,p2,value)

				if point.handle_left_type in {'FREE', 'VECTOR'}:
					point.co = get_corner_position(p1,p2,p3,value)
				else:
					point.co += get_line_offset(p2,p3,value)

				if point.handle_right_type != 'VECTOR':
					point.handle_right = get_corner_position(p2,p3,p4,value)

			elif hasleft and not hasright:
				if point.handle_left_type != 'VECTOR':
					point.handle_left = get_corner_position(p0,p1,p2,value)
				point.co += get_line_offset(p1,p2,value)

	def chamfer(self, indexs, value, tention):
		# TODO need to optimize and add tention functinality
		for i in reversed(indexs):
			point = self.bezier_points[i]
			left = self.get_left_index(i)
			right = self.get_rigth_index(i)

			point_start = self.bezier_points[left]
			point_center = self.bezier_points[i]
			point_end = self.bezier_points[right]

			segment1 = [point_start]
			segment1.append(point_center)
			a1 = segment1[0].co
			b1 = segment1[0].handle_right
			c1 = segment1[1].handle_left
			d1 = segment1[1].co
			length1 = self.get_segment_length(left)
			val = value if value <= length1 else length1
			t1 = 1 - (val / length1) if length1 != 0 else 0

			segment2 = [point_center]
			segment2.append(point_end)
			a2 = segment2[0].co
			b2 = segment2[0].handle_right
			c2 = segment2[1].handle_left
			d2 = segment2[1].co
			length2 = self.get_segment_length(i)
			val = value if value <= length2 else length2
			t2 = val / length2 if length2 != 0 else 1

			l = split_segment(a1, b1, c1, d1, t1)
			r = split_segment(a2, b2, c2, d2, t2)

			a = r[2]
			c = Vector(point_center.co)
			b = l[4]
			angle = get_3_points_angle_3d(a, c, b)

			# not a perfect solution
			t = 0.551786 * (angle/(pi/2))

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

			handle_type = 'FREE' if tention > 0 else 'VECTOR'

			NewPoint = Bezier_point(point)
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

			self.bezier_points.insert(i, NewPoint)


class Curve:
	def __init__(self, obj):
		self.obj = obj
		self.splines = self.get_splines(obj.data.splines)
		self.original = deepcopy(self.splines)

	def get_splines(self, splines):
		return [Spline(sp) for sp in splines]

	def append(self, spline):
		self.splines.append(spline)

	def prepend(self, spline):
		self.splines.prepend(spline)

	def insert(self, index, spline):
		self.splines.insert(index, spline)

	def join(self, index, spline):
		self.splines[index].join(spline)

	def restore(self):
		self.splines = deepcopy(self.original)

	def reset(self):
		self.obj.data.splines.clear()
		for spline in self.original:
			spline.create(self.obj.data)

	def update(self):
		self.obj.data.splines.clear()
		for spline in self.splines:
			spline.create(self.obj.data)

	def clone(self, index):
		if index < len(self.splines):
			return deepcopy(self.splines[index])
		return None

	def swap(self, index1, index2):
		count = len(self.splines)
		if index1 < count and index1 < count:
			temp = self.splines[index1]
			self.splines[index1] = self.splines[index2]
			self.splines[index2] = temp
			return True
		return False

__all__ = ["Bezier_point", "Segment", "Spline", "Curve"]