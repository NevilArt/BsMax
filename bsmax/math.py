from math import sqrt, acos
from mathutils import Vector

def point_on_line(a, b, t):
	return a + (b - a) * t

def point_on_vector(a, b, c, d, t):
	C1 = d - (3.0 * c) + (3.0 * b) - a
	C2 = (3.0 * c) - (6.0 * b) + (3.0 * a)
	C3 = (3.0 * b) - (3.0 * a)
	C4 = a
	return C1 * t * t * t + C2 * t * t + C3 * t + C4

def split_segment(p1, p2, p3, p4, t):
	# start.co start.out end.in end.co
	p12 = (p2 - p1) * t + p1
	p23 = (p3 - p2) * t + p2
	p34 = (p4 - p3) * t + p3
	p123 = (p23 - p12) * t + p12
	p234 = (p34 - p23) * t + p23
	p1234 = (p234 - p123) * t + p123
	# start.co start.out center.in center.co center.out end.in end.co
	return [p1,p12,p123,p1234,p234,p34,p4]

def get_distance(a, b):
	x,y,z = a.x - b.x, a.y - b.y, a.z - b.z
	return sqrt(x**2 + y**2 + z**2)

def get_2_pont_size(pmin, pmax):
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
	return lenght

def get_3_points_angle(a, b, c):
	v1 = Vector((a.x - b.x, a.y - b.y, a.z - b.z))
	v2 = Vector((c.x - b.x, c.y - b.y, c.z - b.z))
	v1mag = sqrt(v1.x**2 + v1.y**2 + v1.z**2)
	v1mag = 0.0001 if v1mag == 0 else v1mag
	v1norm = Vector((v1.x / v1mag, v1.y / v1mag, v1.z / v1mag))
	v2mag = sqrt(v2.x**2 + v2.y**2 + v2.z**2)
	v2mag = 0.0001 if v2mag == 0 else v2mag
	v2norm = Vector((v2.x / v2mag, v2.y / v2mag, v2.z / v2mag))
	res = v1norm.x * v2norm.x + v1norm.y * v2norm.y + v1norm.z * v2norm.z
	return acos(res)

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

def get_offset_by_orient(offset ,orient):
	x, y, z = offset
	# Z cheked x and y not tested yet
	if orient == 'FRONT': 
		return Vector((x, z, -y))
	elif orient == 'BACK':
		return Vector((-x, -z, y))
	elif orient == 'LEFT':
		return Vector((z, -y, -x))
	elif orient == 'RIGHT':
		return Vector((-z, y, x))
	elif orient == 'TOP':
		return Vector((x, y, z))
	elif orient == 'BOTTOM':
		return Vector((x, -y, -z))
	else:
		return offset

__all__ = ["point_on_line",
		"point_on_vector",
		"split_segment",
		"get_2_point_center",
		"get_distance",
		"get_segment_length",
		"get_3_points_angle",
		"get_axis_constraint",
		"get_offset_by_orient"]