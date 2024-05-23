############################################################################
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################################################
# 2024/05/20

from math import sqrt, acos, atan2
from mathutils import Vector


class BoolVector:
	def __init__(self):
		self.x = False
		self.y = False
		self.z = False

	def set(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z


class BitArray:
	def __init__(self):
		self.string = ""
		self.ints = []
	
	def set(self, numString):
		""" check the string """
		self.string = ""
		for l in numString:
			if l in '0123456789,-':
				self.string += l

		""" convert strings to integers """
		self.string = self.string.strip()
		ranges = self.string.split(",")
		numstr = [r.split("-") for r in ranges]
		self.ints.clear()
		for n in numstr:
			if len(n) == 1:
				if n[0] != '':
					self.ints.append(int(n[0]))
			elif len(n) == 2:
				n1,n2 = int(n[0]),int(n[1])
				if n2 > n1:
					for i in range(n1, n2+1):
						self.ints.append(i)
		self.ints.sort()
	
	def get(self):
		return self.ints
	
	def as_string(self):
		return ""


def point_on_line(start, end, time):
	""" Get point coordinate on line by time

		args:
			start: Point2 or Point3
			end: Point2 or Point3
			time: float 0 to 1.0
		return:
			Same as start argument
	"""
	return start + (end - start) * time


def point_on_cubic_bezier_curve(a, b, c, d, t):
	""" get point coordinate on cubic bezier curve

		args:
			a: Vector3 start point
			b: Vector3 start point out handle
			c: Vector3 end point in handle
			d: Vector3 end pont
			t: Float 0 ~ 1 time
		return:
			Vector3
	"""
	C1 = d - 3*c + 3*b - a
	C2 = 3*c - 6*b + 3*a
	C3 = 3*b - 3*a
	C4 = a
	return C1*t**3 + C2*t*t + C3*t + C4


def point_rotation_on_segment(a, b, c, d, time):
	# Get segment and time return direction
	# Tamprary solution but its work for now
	t1, t2 = time - 0.001, time + 0.001
	if t1 < 0:
		t1, t2 = 0, 0.001
	if t2 > 1:
		t1, t2 = 0.999, 1
	p1 = point_on_cubic_bezier_curve(a, b, c, d, t1)
	p2 = point_on_cubic_bezier_curve(a, b, c, d, t2)
	lx, ly, lz = p2 - p1
	x = atan2(lz, ly)
	y = atan2(lz, lx)
	z = atan2(ly, lx)
	return Vector((x, y, z))


def point_on_spline(spline, time):
	""" 
		args:
			Spline
			time

		return:
			Location, Rotation, Scale
			#TODO convert to transform
	"""
	# Safty Check
	if len(spline.bezier_points) < 2:
		return Vector((0, 0, 0)), Vector((0, 0, 0)), Vector((1, 1, 1))
	
	lengths, total_length = [], 0

	# Add one more segment if spline is close
	segs = [point for point in spline.bezier_points]
	if spline.use_cyclic_u:
		segs.append(spline.bezier_points[0])
	
	# Fast solution for speciyal conditions
	if time <= 0:
		location = spline.bezier_points[0].co.copy()
		a = segs[0].co
		b = segs[0].handle_right
		c = segs[1].handle_left
		d = segs[1].co
		rotaion = point_rotation_on_segment(a, b, c, d, 0)
		scale = Vector((1, 1, 1))
		return location, rotaion, scale

	if time >= 1:
		location = spline.bezier_points[-1].co.copy()
		a = segs[-2].co
		b = segs[-2].handle_right
		c = segs[-1].handle_left
		d = segs[-1].co
		rotaion = point_rotation_on_segment(a, b, c, d, 1)
		scale = Vector((1, 1, 1))
		return location, rotaion, scale

	# Sum segment lengths
	for i in range(len(segs) - 1):
		a = segs[i].co
		b = segs[i].handle_right
		c = segs[i+1].handle_left
		d = segs[i+1].co
		l = get_segment_length(a, b, c, d, 100)
		lengths.append(l)
		total_length += l

	# Find segment that point on it	
	length = total_length * time
	for i in range(len(lengths)):
		if length >= lengths[i]:
			length -= lengths[i]
		else:
			index = i
			break

	# Calculate point location on segment
	a = segs[index].co
	b = segs[index].handle_right
	c = segs[index+1].handle_left
	d = segs[index+1].co
	t = length / lengths[index]
	location = point_on_cubic_bezier_curve(a, b, c, d, t)
	
	# Calculate Point Rotation on Secmetn/Splie/Curve
	rotaion = point_rotation_on_segment(a, b, c, d, time)
	
	scale = Vector((1, 1, 1))
	
	return location, rotaion, scale


def point_on_curve(curve, index, time):
	""" get point on curve by time
		
		args:
			Curve: Object
			Spline: index
			time: 0-1
		return:
			Location, Rotation, Scale
	"""
	# Safty Check
	if not curve.data.splines:
		return Vector((0, 0, 0)), Vector((0, 0, 0)), Vector((1, 1, 1))

	return point_on_spline(curve.data.splines[index], time)


def get_bezier_tangent(a, b, c, d, t):
	s = 1-t
	return s*s*(b-a) + 2*s*t*(c-b) + t*t*(d-c)


def split_segment(p1, p2, p3, p4, t):
	""" Split Cubic bezier on given time """
	# start.co start.out end.in end.co
	p12 = (p2 - p1) * t + p1
	p23 = (p3 - p2) * t + p2
	p34 = (p4 - p3) * t + p3
	p123 = (p23 - p12) * t + p12
	p234 = (p34 - p23) * t + p23
	p1234 = (p234 - p123) * t + p123
	# start.co start.out center.in center.co center.out end.in end.co
	return [p1, p12, p123, p1234, p234, p34, p4]


def get_distance(a, b):
	""" Get distance of 2 point3 (Vector3)
	
		args:
			a: point3
			b: point3
		return:
			float
	"""
	x, y, z = a.x - b.x, a.y - b.y, a.z - b.z
	return sqrt(x**2 + y**2 + z**2)


def value_by_percent(orig, targ, percent):
	""" Return a number between argoments by percent """
	return (targ - orig) * percent + orig


def scale_vector_to_float(scale):
	""" return avrage of 3 scale element as float """
	return ((scale.x + scale.y + scale.z) / 3)


def isfloat(value):
	try:
		float(value)
		return True
	except ValueError:
		return False


def get_2_pont_size(pmin, pmax):
	""" Get min max point return Bounding box dimansions """
	w = pmax[0] - pmin[0]
	l = pmax[1] - pmin[1]
	h = pmax[2] - pmin[2]
	return Vector((w, l, h))


def get_2_point_center(sp, ep):
	x = sp.x + ((ep.x - sp.x) / 2)
	y = sp.y + ((ep.y - sp.y) / 2)
	z = sp.z + ((ep.z - sp.z) / 2)
	return Vector((x, y, z))


def get_segment_length(a, b, c, d, steps):
	points = [a]
	s = 1 / steps
	for i in range(1, steps + 1):
		t = i * s
		p = point_on_cubic_bezier_curve(a, b, c, d, t)
		points.append(p)
	lenght = 0
	for i in range(len(points) - 1):
		lenght += get_distance(points[i], points[i - 1])
	#bpy.context.active_object.data.splines[0].calc_length()
	return lenght


def get_2_points_angel_2d(p1, p2):
	return atan2(p2.x - p1.x, p1.y - p2.y)


def get_3_points_angle_2d(a, b, c):
	return atan2(c.y - b.y, c.x - b.x) - atan2(a.y - b.y, a.x - b.x)


def get_3_points_angle_3d(a, b, c):
	v1 = Vector((a.x - b.x, a.y - b.y, a.z - b.z))
	v2 = Vector((c.x - b.x, c.y - b.y, c.z - b.z))
	v1mag = sqrt(v1.x**2 + v1.y**2 + v1.z**2)
	v1mag = 0.00000000000001 if v1mag == 0 else v1mag
	v1norm = Vector((v1.x / v1mag, v1.y / v1mag, v1.z / v1mag))
	v2mag = sqrt(v2.x**2 + v2.y**2 + v2.z**2)
	v2mag = 0.00000000000001 if v2mag == 0 else v2mag
	v2norm = Vector((v2.x / v2mag, v2.y / v2mag, v2.z / v2mag))
	res = v1norm.x * v2norm.x + v1norm.y * v2norm.y + v1norm.z * v2norm.z
	res = 1 if res > 1 else res
	res = -1 if res < -1 else res
	return acos(res)


def get_lines_intersection(p1, p2, p3, p4):
	""" Get 2 line intersection point
		Note: for now 2D lines only Z count as 0

		args:
			p1: Vector3 Line A Start point
			p2: Vector3 Line A End point
			p3: Vector3 Line B Start point
			p4: Vector3 Line B End point
		return:
			Vector3
	"""
	#TODO Count Z too
	delta = ((p1.x - p2.x)*(p3.y - p4.y) - (p1.y - p2.y)*(p3.x - p4.x))
	if delta == 0:
		return None
	else:
		x = ((p1.x*p2.y - p1.y*p2.x)*(p3.x - p4.x) -
			(p1.x - p2.x)*(p3.x*p4.y - p3.y*p4.x)) / delta

		y = ((p1.x*p2.y - p1.y*p2.x)*(p3.y - p4.y) - 
			(p1.y - p2.y)*(p3.x*p4.y - p3.y*p4.x)) / delta

	return Vector((x, y, 0))


def get_axis_constraint(oring, current):
	# Keep bigger axis and set the other zero
	delta_x = abs(oring.x - current.x)
	delta_y = abs(oring.y - current.y)
	delta_z = abs(oring.z - current.z)
	side = max(delta_x, delta_y, delta_z)
	if side == delta_x:
		current.y, current.z = oring.y, oring.z
	elif side == delta_y:
		current.x, current.z = oring.x, oring.z
	elif side == delta_z:
		current.x, current.y = oring.x, oring.y
	return current


def get_bias(bias, time):
	if bias > 0:
		return 1 - pow(1 - time, 9*bias + 1)
	elif bias < 0:
		return pow(time, 1 - 9*bias)
	else:
		return time


def shift_number(number, value, minimum, maximum):
	number += value
	if number > maximum:
		number -= maximum - minimum + 1
	if number < minimum:
		number += maximum - minimum + 1
	return number


def get_index_str(count, index):
	length = len(str(index))
	string = ""
	if length < count:
		for i in range(length, count):
			string += "0"
	return (string + str(index))


def dot(v1, v2):
	""" return Dot product of two vectors
		
		args:
			v1: Vector()
			v2: Vector()
		
		return:
			Float
	"""
	return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z


def bounding_box_colide_with(box_a, box_b, ignore_z=False):
	""" check dose 2 boundig box has intersect

		args:
			box_a: BoundingBox class
			box_b: BoundingBox class
			ignore_z: boolean ignore z if true

		return:
			boolean
	"""
	xin, yin, zin = False, False, False

	if 	box_b.start.x < box_a.start.x < box_b.end.x or\
		box_b.start.x < box_a.end.x < box_b.end.x or\
		box_a.start.x < box_b.start.x < box_a.end.x or\
		box_a.start.x < box_b.end.x < box_a.end.x:

		xin = True

	if 	box_b.start.y < box_a.start.y < box_b.end.y or\
		box_b.start.y < box_a.end.y < box_b.end.y or\
		box_a.start.y < box_b.start.y < box_a.end.y or\
		box_a.start.y < box_b.end.y < box_a.end.y:

		yin = True
	
	if ignore_z:
		return (xin and yin)

	if 	box_b.start.z < box_a.start.z < box_b.end.z or\
		box_b.start.z < box_a.end.z < box_b.end.z or\
		box_a.start.z < box_b.start.z < box_a.end.z or\
		box_a.start.z < box_b.end.z < box_a.end.z:

		zin = True
	
	if ignore_z:
		return (xin and yin and zin)


def get_cubic_bezier_curve_length(a, b, c, d, steps=100):
	""" calculate cubic bezier curve length

		args:
			a: Vector3 start point
			b: Vector3 start point out handle
			c: Vector3 end point in handle
			d: Vector3 end pont
			steps: int number of devide heigher number solwer but better result
		return:
			float
	"""
	points = [a]
	s = 1 / steps

	for i in range(1, steps + 1):
		t = i * s
		p = point_on_cubic_bezier_curve(a, b, c, d, t)
		points.append(p)
	lenght = 0

	for i in range(len(points) - 1):
		lenght += get_distance(points[i], points[i - 1])

	return lenght


def get_point_on_spline(spline, time, devide_steps=100):
	lengths, total_length = [], 0
	if time <= 0:
		return spline.bezier_points[0].co.copy()
	
	if time >= 1:
		return spline.bezier_points[-1].co.copy()
	
	segs = [point for point in spline.bezier_points]
	
	if spline.use_cyclic_u:
		segs.append(spline.bezier_points[0])
	
	# collect the segment length
	for i in range(len(segs) - 1):
		a = segs[i].co
		b = segs[i].handle_right
		c = segs[i+1].handle_left
		d = segs[i+1].co
		l = get_segment_length(a, b, c, d, devide_steps)
		lengths.append(l)
		total_length += l

	length = total_length * time
	
	for i in range(len(lengths)):
		if length >= lengths[i]:
			length -= lengths[i]
		else:
			index = i
			break
	
	a = segs[index].co
	b = segs[index].handle_right
	c = segs[index+1].handle_left
	d = segs[index+1].co
	t = length / lengths[index]	

	return point_on_cubic_bezier_curve(a, b, c, d, t)