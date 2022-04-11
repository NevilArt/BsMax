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

import numpy
from math import sin, cos, sqrt, acos, atan2
from mathutils import Vector, Matrix



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
	
	def set(self, frames):
		""" check the string """
		self.string = ""
		for l in frames:
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
					for i in range(n1,n2+1):
						self.ints.append(i)
		self.ints.sort()
	
	def get(self):
		return self.ints



def point_on_line(a, b, t):
	return a+(b-a)*t



def point_on_vector(a, b, c, d, t):
	C1 = d-3*c+3*b-a
	C2 = 3*c-6*b+3*a
	C3 = 3*b-3*a
	C4 = a
	return C1*t**3+C2*t*t+C3*t+C4



def point_rotation_on_segment(a, b, c, d, time):
	# Get segment and time return direction
	# Tamprary solution but its work for now
	t1, t2 = time - 0.001, time + 0.001
	if t1 < 0:
		t1, t2 = 0, 0.001
	if t2 > 1:
		t1, t2 = 0.999, 1
	p1 = point_on_vector(a, b, c, d, t1)
	p2 = point_on_vector(a, b, c, d, t2)
	lx, ly, lz = p2 - p1
	x = atan2(lz, ly)
	y = atan2(lz, lx)
	z = atan2(ly, lx)
	return Vector((x, y, z))


def point_on_spline(spline, time):
	""" arguments(Spline, time) return: Location, Rotation, Scale """
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
		l = get_segment_length(a,b,c,d,100)
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
	location = point_on_vector(a, b, c, d, t)
	
	# Calculate Point Rotation on Secmetn/Splie/Curve
	rotaion = point_rotation_on_segment(a, b, c, d, time)
	
	scale = Vector((1,1,1))
	
	return location, rotaion, scale



def point_on_curve(curve, index, time):
	""" Arguments(Curve Object, Spline index, time) return: Location, Rotation, Scale """
	# Safty Check
	if not curve.data.splines:
		return Vector((0, 0, 0)), Vector((0, 0, 0)), Vector((1, 1, 1))

	return point_on_spline(curve.data.splines[index])



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
	""" Get 2 point Vector3 and return distance as float """
	x,y,z = a.x - b.x, a.y - b.y, a.z - b.z
	return sqrt(x**2 + y**2 + z**2)


def value_by_percent(orig, targ, percent):
	""" Return a number between argoments by percent """
	return (targ - orig) * percent + orig


def scale_vector_to_float(scale):
	""" return avrage of 3 scale element as float """
	return ((scale.x + scale.y + scale.z) / 3)



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
		p = point_on_vector(a, b, c, d, t)
		points.append(p)
	lenght = 0
	for i in range(len(points) - 1):
		lenght += get_distance(points[i], points[i - 1])
	#bpy.context.active_object.data.splines[0].calc_length()
	return lenght



def get_2_points_angel_2d(p1, p2):
	return atan2(p2.x-p1.x, p1.y-p2.y)



def get_3_points_angle_2d(a, b, c):
	return atan2(c.y-b.y, c.x-b.x) - atan2(a.y-b.y, a.x-b.x)



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



def get_lines_intersection(p1,p2,p3,p4):
	delta = ((p1.x-p2.x)*(p3.y-p4.y)-(p1.y-p2.y)*(p3.x-p4.x))
	if delta == 0:
		return None
	else:
		x=((p1.x*p2.y-p1.y*p2.x)*(p3.x-p4.x)-(p1.x-p2.x)*(p3.x*p4.y-p3.y*p4.x))/delta
		y=((p1.x*p2.y-p1.y*p2.x)*(p3.y-p4.y)-(p1.y-p2.y)*(p3.x*p4.y-p3.y*p4.x))/delta
	return Vector((x,y,0))



#############################################
# def get_2_line_intersection(line1, line2):
# 	def line1(x1,y1,x2,y2,x3,y3,x4,y4):
# 		nx=(x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4),
# 		ny=(x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4),
# 		d=(x1-x2)*(y3-y4)-(y1-y2)*(x3-x4);
# 		if d==0:
# 			return False
# 		return point(nx/d, ny/d)
# 	def line2(p1, p2, p3, p4):
# 		x1 = p1.x, y1 = p1.y,
# 		x2 = p2.x, y2 = p2.y,
# 		x3 = p3.x, y3 = p3.y,
# 		x4 = p4.x, y4 = p4.y;
# 		return line1(x1,y1,x2,y2,x3,y3,x4,y4)
# 	return line2(line1.p1, line1.p2, line2.p1, line2.p2)
###############################################


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
	return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z



def matrix_from_elements(location, euler_rotation, scale):
	""" Return Transform Matrix from argoments """
	roll, pitch, yaw = euler_rotation

	Rz_yaw = numpy.array([
		[cos(yaw), -sin(yaw), 0],
		[sin(yaw), cos(yaw), 0],
		[0, 0, 1]])
	
	Ry_pitch = numpy.array([
		[cos(pitch), 0, sin(pitch)],
		[0, 1, 0],
		[-sin(pitch), 0, cos(pitch)]])

	Rx_roll = numpy.array([
		[1, 0, 0],
		[0, cos(roll), -sin(roll)],
		[0, sin(roll), cos(roll)]])

	m = numpy.dot(Rz_yaw, numpy.dot(Ry_pitch, Rx_roll))

	# Convert Arry to Matrix and apply location and scale
	lx, ly, lz = location
	sx, sy, sz = scale

	matrix = Matrix((
		(m[0][0]*sx, m[0][1]*sy, m[0][2]*sz, lx),
		(m[1][0]*sx, m[1][1]*sy, m[1][2]*sz, ly),
		(m[2][0]*sx, m[2][1]*sy, m[2][2]*sz, lz),
		(0, 0, 0, 1)))

	return matrix



def transform_points_to_matrix(points, matrix):
	m = matrix
	rxv = Vector((m[0][0], m[0][1], m[0][2]))
	ryv = Vector((m[1][0], m[1][1], m[1][2]))
	rzv = Vector((m[2][0], m[2][1], m[2][2]))
	tv  = Vector((m[0][3], m[1][3], m[2][3]))
	new_points = []
	for pv in points:
		x = dot(pv, rxv) + tv.x
		y = dot(pv, ryv) + tv.y
		z = dot(pv, rzv) + tv.z
		new_points.append(Vector((x, y, z)))
	return new_points



def transform_point_to_matrix(point, matrix):
	m = matrix
	rxv = Vector((m[0][0], m[0][1], m[0][2]))
	ryv = Vector((m[1][0], m[1][1], m[1][2]))
	rzv = Vector((m[2][0], m[2][1], m[2][2]))
	tv  = Vector((m[0][3], m[1][3], m[2][3]))
	x = dot(point, rxv) + tv.x
	y = dot(point, ryv) + tv.y
	z = dot(point, rzv) + tv.z
	return Vector((x, y, z))



def to_local_matrix(point, matrix):
	# Untranslating
	p = point - matrix.translation

	euler = matrix.to_euler()
	# UnYawing
	s, c = sin(-euler.z), cos(-euler.z)
	p = Vector((p.x*c - p.y*s, p.y*c + p.x*s, p.z))

	# Unpinching
	s, c = sin(-euler.x), cos(-euler.x)
	p = Vector((p.x, p.y*c - p.z*s, p.z*c + p.y*s))

	# Unrolling
	s, c = sin(-euler.y), cos(-euler.y)
	p = Vector((p.x*c + p.z*s, p.y, p.z*c - p.x*s))

	scale = matrix.to_scale()
	# UnScaling and return
	s = Vector((1/scale.x, 1/scale.y, 1/scale.z))
	return Vector((p.x*s.x, p.y*s.y, p.z*s.z))


def inverse_transform_matrix(matrix):
	m = matrix
	n = Matrix((
		(1, 0, 0, -m[0][3]),
		(0, 1, 0, -m[1][3]),
		(0, 0, 1, -m[2][3]),
		(0, 0, 0, 1)))

	m00, m01, m02, _ = m[0]
	m10, m11, m12, _ = m[1]
	m20, m21, m22, _ = m[2]
	
	a1 = m00*m11*m22 + m01*m12*m20 + m02*m10*m21
	a2 = m20*m11*m02 + m21*m12*m00 + m22*m10*m01
	a = 1/(a1-a2)

	n[0][0] =  (m11*m22 - m12*m21) * a
	n[1][0] = -(m10*m22 - m12*m20) * a
	n[2][0] =  (m10*m21 - m11*m20) * a

	n[0][1] = -(m01*m22 - m02*m21) * a
	n[1][1] =  (m00*m22 - m02*m20) * a
	n[2][1] = -(m00*m21 - m01*m20) * a

	n[0][2] =  (m01*m22 - m02*m21) * a
	n[1][2] = -(m00*m12 - m02*m10) * a
	n[2][2] =  (m00*m11 - m01*m10) * a

	return n


class BsMatrix:
	def __init__(self):
		self.matrix = [
			[1, 0, 0, 0],
			[0, 1, 0, 0],
			[0, 0, 1, 0],
			[0, 0, 0, 1]]
	
	def as_matrix(self):
		m = self.matrix
		return Matrix((
			(m[0][0], m[0][1], m[0][2], m[0][3]),
			(m[1][0], m[1][1], m[1][2], m[1][3]),
			(m[2][0], m[2][1], m[2][2], m[2][3]),
			(m[3][0], m[3][1], m[3][2], m[3][3]))) 
	
	def from_euler(self, yaw, pitch, roll):
		sy, cy = sin(yaw), cos(yaw)
		Rz_yaw = (
			Vector((cy, -sy, 0)),
			Vector((sy,  cy, 0)),
			Vector((0,    0, 1)))

		sp, cp = sin(pitch), cos(pitch)
		Ry_pitch = (
			Vector(( cp, 0, sp)),
			Vector((  0, 1, 0)),
			Vector((-sp, 0, cp)))

		sr, cr = sin(roll), cos(roll) 
		Rx_roll = (
			Vector((1,  0,   0)),
			Vector((0, cr, -sr)),
			Vector((0, sr,  cr)))
			
		m = numpy.dot(Rz_yaw, numpy.dot(Ry_pitch, Rx_roll))

		mt = self.matrix
		mt[0][0], mt[0][1], mt[0][2] = m[0][0], m[0][1], m[0][2]
		mt[1][0], mt[1][1], mt[1][2] = m[1][0], m[1][1], m[1][2]
		mt[2][0], mt[2][1], mt[2][2] = m[2][0], m[2][1], m[2][2]