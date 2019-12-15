import bpy, numpy, math
from mathutils import Vector
from copy import deepcopy
from math import sin, cos, atan2, pi, sqrt
from bsmax.math import (get_3_points_angle_2d,get_lines_intersection,split_segment,point_on_line,
	point_on_vector,get_distance,get_3_points_angle_3d,get_segment_length)

def get_devide_range(a, b):
	m = a+((b-a)/2)
	return [a,m],[m,b]

def get_cros_time(start, end, ps, pe, cross):
	f = get_distance(ps, pe)
	c = get_distance(ps, cross)
	t = end - start
	return start + t*(c/f)

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

def get_curve_selection_index(splines, mode):
	selection = []
	if mode == 'point':
		for i, spline in enumerate(splines):
			sel = []
			for j, point in enumerate(spline.bezier_points):
				if point.select_control_point:
					sel.append(j)
			if len(sel) > 0:
				selection.append([i,sel])
	elif mode == 'segment':
		for i, spline in enumerate(splines):
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
					sel.append(j)
			if len(sel) > 0:
				selection.append([i,sel])
	elif mode == 'spline':
		for i, spline in enumerate(splines):
			istrue = True
			for point in spline.bezier_points:
				if not point.select_control_point:
					istrue = False
					break
			if istrue:
				selection.append(i)
	elif mode == 'close':
		for i, spline in enumerate(splines):
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

def get_boundingbox(points):
	findmin = lambda l: min(l)
	findmax = lambda l: max(l)
	x,y,z = [[p[i] for p in points] for i in range(3)]
	pmin = Vector([findmin(axis) for axis in [x,y,z]])
	pmax = Vector([findmax(axis) for axis in [x,y,z]])
	return BoundingBox(pmin, pmax)

def get_curve_activespline_index(splines):
	active = splines.active
	for i, spline in enumerate(splines):
		if spline == active:
			return i
	return None

def get_segments_intersection_points(segment1, segment2, tollerance):
	t = tollerance
	def scan(section1,section2):
		diva,divb,points = [],[],[]
		for s1s,s1e in section1:
			b1 = segment1.boundingbox(s1s,s1e,30)
			for s2s,s2e in section2:
				b2 = segment2.boundingbox(s2s,s2e,30)
				if b1.is_colide_with(b2):
					""" devide bonding box untill one of edge smaller than tollerance """
					diva = get_devide_range(s1s,s1e) if b1.width > t and b1.length > t else [[s1s,s1e]]
					divb = get_devide_range(s2s,s2e) if b2.width > t and b2.length > t else [[s2s,s2e]]
					if (b1.width <= t or b1.length <= t) and (b2.width <= t or b2.length <= t):
						""" if both bondig boxes are smaller then tollerance """
						""" get line between start and end of each bonding box """
						p1 = segment1.get_point_on(s1s)
						p2 = segment1.get_point_on(s1e)
						p3 = segment2.get_point_on(s2s)
						p4 = segment2.get_point_on(s2e)
						""" get cros point of lines """
						co = get_lines_intersection(p1,p2,p3,p4)
						time1 = get_cros_time(s1s, s1e, p1, p2, co)
						time2 = get_cros_time(s2s, s2e, p3, p4, co)
						points.append(CurveIntersectionPoint(segment1,time1,segment2,time2,co))
					else:
						""" rescan divided boxes """
						points += scan(diva,divb)
		""" remove doubles """
		retpoints = []
		for p in points:
			overlap = False
			for r in retpoints:
				if get_distance(p.co,r.co) < tollerance/10:
					overlap = True
					break
			if not overlap:
				retpoints.append(p)
		return retpoints
	return scan([[0,1]], [[0,1]])

def get_spline_segments(spline):
	segs = []
	count = len(spline.bezier_points) if spline.use_cyclic_u else len(spline.bezier_points)-1
	for i in range(count):
		segs.append(Segment(spline,i))
	return segs

def get_curves_intersection_points(spline1, spline2, tollerance):
	intsecs = []
	segs1 = spline1.get_as_segments()
	segs2 = spline2.get_as_segments()
	for s1 in segs1:
		for s2 in segs2:
			intsecs += get_segments_intersection_points(s1, s2, tollerance)
	return intsecs

class SegmentDivisions:
	def __init__(self, index, time):
		self.index = index
		self.times = [time]
	def append(self,time):
		if 0 < time < 1 and not time in self.times:
			self.times.append(time)
	def sort(self,reverse=False):
		self.times.sort(reverse=reverse)

class SplineDivisions:
	def __init__(self, spline, segsub):
		self.spline = spline
		self.segments = [segsub]
	def sort(self, reverse=False):
		indexes = [sd.index for sd in self.segments]
		indexes.sort(reverse=reverse)
		segments = []
		for i in indexes:
			for s in self.segments:
				if i == s.index:
					segments.append(s)
					break
		self.segments = deepcopy(segments)

def collect_splines_divisions(intersections):
	divisions = []
	def spappend(segment, time):
		isnewspline = True
		for div in divisions:
			if segment.spline == div.spline:
				isnewsegment = True
				for dseg in div.segments:
					if segment.index == dseg.index:
						dseg.times.append(time)
						isnewsegment = False
						break
				if isnewsegment:
					""" creat a new SegmentDivisions object """
					div.segments.append(SegmentDivisions(segment.index,time))
				isnewspline = False
		""" create a new SplineDivisions object """
		if isnewspline:
			newdiv = SplineDivisions(segment.spline,SegmentDivisions(segment.index,time))
			divisions.append(newdiv)

	for i in intersections:
		spappend(i.segment1, i.time1)
		spappend(i.segment2, i.time2)

	for d in divisions:
		d.sort(reverse=True)
		for ds in d.segments:
			ds.sort()
		
	return divisions

class Line:
	def __init__(self,a,b):
		self.a = a
		self.b = b

	def point_on_line(self,t):
		return self.a+(self.b-self.a)*t

	def get_length(self):
		x,y,z = self.a.x-self.b.x, self.a.y-self.b.y, self.a.z-self.b.z
		return sqrt(x**2 + y**2 + z**2)

	def get_angel_2d(self):
		return atan2(self.b.x-self.a.x, self.a.y-self.b.y)

	def get_intersection_with(self, target):
		""" 2D lines only """
		p1,p2,p3,p4= self.a, self.b, target.a, target.b
		delta = ((p1.x-p2.x)*(p3.y-p4.y)-(p1.y-p2.y)*(p3.x-p4.x))
		if delta == 0:
			return None
		else:
			x=((p1.x*p2.y-p1.y*p2.x)*(p3.x-p4.x)-(p1.x-p2.x)*(p3.x*p4.y-p3.y*p4.x))/delta
			y=((p1.x*p2.y-p1.y*p2.x)*(p3.y-p4.y)-(p1.y-p2.y)*(p3.x*p4.y-p3.y*p4.x))/delta
		return Vector((x,y,0))

class BoundingBox:
	def __init__(self, start, end):
		self.start = start
		self.end = end
		self.width = end.x-start.x
		self.length = end.y-start.y
		self.height = end.z-start.z
		self.center = (start+end)/2
	def is_inside_of(self, target):
		return False
	def is_cover_the(self, target):
		return False
	def is_colide_with(self, target):
		xin, yin = False, False
		if 	target.start.x < self.start.x < target.end.x or\
			target.start.x < self.end.x < target.end.x or\
			self.start.x < target.start.x < self.end.x or\
			self.start.x < target.end.x < self.end.x:
			xin = True
		if 	target.start.y < self.start.y < target.end.y or\
			target.start.y < self.end.y < target.end.y or\
			self.start.y < target.start.y < self.end.y or\
			self.start.y < target.end.y < self.end.y:
			yin = True
		return (xin and yin)

class CurveIntersectionPoint:
	def __init__(self, segment1,time1,segment2,time2,co):
		self.segment1 = segment1
		self.time1 = time1
		self.segment2 = segment2
		self.time2 = time2
		self.co = co

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
	def __init__(self, spline, index):
		start,end = index,spline.get_rigth_index(index)
		self.spline = spline
		self.index = index
		self.a = spline.bezier_points[start].co
		self.b = spline.bezier_points[start].handle_right
		self.c = spline.bezier_points[end].handle_left
		self.d = spline.bezier_points[end].co
		self.start = Bezier_point(spline.bezier_points[start])
		self.end = Bezier_point(spline.bezier_points[end])
	
	def boundingbox(self, start, end, divid):
		step = (end-start)/divid
		cuts = [point_on_vector(self.a,self.b,self.c,self.d,start+t*step) for t in range(divid+1)]
		return get_boundingbox(cuts)
	
	def get_point_on(self, t):
		p1 = self.d-3*self.c+3*self.b-self.a
		p2 = 3*self.c-6*self.b+3*self.a
		p3 = 3*self.b-3*self.a
		p4 = self.a
		return p1*t**3+p2*t*t+p3*t+p4
		#return self.spline.get_point_on_segment(self.index, t)
	
	def get_section_line(self, start, end):
		a = point_on_vector(self.a,self.b,self.c,self.d,start)
		b = point_on_vector(self.a,self.b,self.c,self.d,end)
		return Line(a,b)

class Spline:
	def __init__(self, spline):
		if spline != None:
			""" create mirror of ariginal spline """
			self.points = []
			self.bezier_points = self.get_bezier_points(spline)
			self.tilt_interpolation = spline.tilt_interpolation
			self.radius_interpolation = spline.radius_interpolation
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
		else:
			""" create a default empty spline """
			self.points = []
			self.bezier_points = []
			self.tilt_interpolation = 'LINEAR'
			self.radius_interpolation = 'LINEAR'
			self.type = 'BEZIER'
			self.point_count_u = 2
			self.point_count_v = 1
			self.order_u = 4
			self.order_v = 4
			self.resolution_u = 12
			self.resolution_v = 12
			self.use_cyclic_u = False
			self.use_cyclic_v = False
			self.use_endpoint_u = False
			self.use_endpoint_v = False
			self.use_bezier_u = False
			self.use_bezier_v = False
			self.use_smooth = True
			self.hide = False
			self.material_index = 0
			self.character_index = 0

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

	def get_segment_indexes(self, index):
		""" return start and end point index of segment """
		return [index, self.get_rigth_index(index)]

	def get_segment(self, index):
		start,end = self.get_segment_indexes(index)
		a = self.bezier_points[start].co
		b = self.bezier_points[start].handle_right
		c = self.bezier_points[end].handle_left
		d = self.bezier_points[end].co
		return a, b, c, d

	def get_as_segments(self):
		segs = []
		count = len(self.bezier_points) if self.use_cyclic_u else len(self.bezier_points)-1
		return [Segment(self,i) for i in range(count)]

	def get_segment_length(self, index, steps=100):
		if index <= len(self.bezier_points)-2:
			a,b,c,d = get_segment(index)
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

	def get_point_on_segment(self, index, t):
		a,b,c,d = self.get_segment(index)
		p1 = d-3*c+3*b-a
		p2 = 3*c-6*b+3*a
		p3 = 3*b-3*a
		p4 = a
		return p1*t**3+p2*t*t+p3*t+p4

	def get_point_on_spline(self, time):
		return None

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

	def append(self, bezier_point):
		self.bezier_points.append(bezier_point)

	def prepend(self, bezier_points):
		self.bezier_points.prepend(bezier_points)
	
	def insert(self, index, bezier_points):
		self.bezier_points.insert(index, bezier_points)

	def clear(self):
		self.points.clear()
		self.bezier_points.clear()

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

	def divid(self, index, time):
		start,end = self.get_segment_indexes(index)
		a,b,c,d = self.get_segment(index)
		p = split_segment(a,b,c,d,time)
		pa = self.bezier_points[start]
		pc = Bezier_point(pa)
		pe = self.bezier_points[end]
		#pa.co = p[0]
		pa.handle_right_type = 'FREE'
		pa.handle_right = p[1]
		pc.handle_left_type = 'FREE'
		pc.handle_left = p[2]
		pc.co = p[3]
		pc.handle_right_type = 'FREE'
		pc.handle_right = p[4]
		pe.handle_left_type = 'FREE'
		pe.handle_left = p[5]
		#pe.co = p[6]
		self.bezier_points.insert(index+1, pc)

	def multi_division(self, index, times):
		start,end = self.get_segment_indexes(index)
		a,b,c,d = self.get_segment(index)
		ps = self.bezier_points[start]
		pc = []
		pe = self.bezier_points[end]
		ps.handle_left_type = "FREE"
		pe.handle_right_type = "FREE"
		""" conver count to array of numbers """
		if type(times)==int:
			if times > 0:
				count = times+1
				times = []
				step = 1/count
				times = [t*step for t in range(1,count)]
		if type(times)==list:
			times.sort()
			times = [t for t in times if 0 < t < 1]
		else:
			times = []
		if len(times) > 0:
			segs = []
			remain = [ps.co, ps.handle_right, pe.handle_left, pe.co]
			for i, time in enumerate(times):
				a,b,c,d = remain
				t = 1-((1-time)/(1-times[i-1])) if i > 0 else time
				p = split_segment(a,b,c,d,t)
				remain = [p[3],p[4],p[5],p[6]]
				segs.append(p)
			ps.handle_right = segs[0][1] # fix start pionts right handle
			for i, seg in enumerate(segs):
				newpoint = Bezier_point(None)
				newpoint.handle_left_type = "FREE"
				newpoint.handle_right_type = "FREE"
				if len(pc) > 0:
					pc[-1].handle_right = seg[1]
				newpoint.handle_left = seg[2]
				newpoint.co = seg[3]
				newpoint.handle_right = seg[4]
				pc.append(newpoint)
			pe.handle_left = segs[-1][-2] # fix last pionts left handle
		for i in range(len(pc)):
			self.bezier_points.insert(index+i+1, pc[i])

class Curve:
	def __init__(self, obj):
		self.obj = obj
		self.splines = self.get_splines(obj.data.splines)
		self.original = deepcopy(self.splines)

	def get_splines(self, splines):
		return [Spline(sp) for sp in splines]

	def selection(self, mode):
		return get_curve_selection_index(self.splines,mode)

	def active(self):
		return get_curve_activespline_index(self.obj.data.splines)

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

	def boolean(self, index1, index2, mode, tollerance):
		spline1, spline2 = self.splines[index1], self.splines[index2]
		intersections = get_curves_intersection_points(spline1, spline2, tollerance)
		divisions = collect_splines_divisions(intersections)
		for d in divisions:
			for s in d.segments:
				d.spline.multi_division(s.index, s.times)

__all__ = ["Bezier_point", "Line", "Segment", "Spline", "Curve"]