from math import sqrt, acos, atan2
from mathutils import Vector

def point_on_line(a, b, t):
	return a+(b-a)*t

def point_on_vector(a, b, c, d, t):
	C1 = d-3*c+3*b-a
	C2 = 3*c-6*b+3*a
	C3 = 3*b-3*a
	C4 = a
	return C1*t**3+C2*t*t+C3*t+C4

def point_on_curve(curve, index, time):
	spline = curve.data.splines[index]
	lengths, totallength = [], 0
	if time <= 0:
		return spline.bezier_points[0].co.copy()
	if time >= 1:
		return spline.bezier_points[-1].co.copy()
	else:
		segs = [point for point in spline.bezier_points]
		if spline.use_cyclic_u:
			segs.append(spline.bezier_points[0])
		# collect the segment length
		for i in range(len(segs) - 1):
			a = segs[i].co
			b = segs[i].handle_right
			c = segs[i+1].handle_left
			d = segs[i+1].co
			l = get_segment_length(a,b,c,d,100)
			lengths.append(l)
			totallength += l
		length = totallength*time
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
		return point_on_vector(a, b, c, d, t)

# def get_spline_left_index(spline, index):
# 	left = index - 1
# 	if index == 0:
# 		left = len(spline.bezier_points) - 1 if spline.use_cyclic_u else index
# 	return left

# def get_spline_rigth_index(spline, index):
# 	right = index + 1
# 	if index >= len(spline.bezier_points) - 1:
# 		right = 0 if spline.use_cyclic_u else index
# 	return right

# def get_line_tilt(p1, p2):
# 	a,b = p1.y-p2.y, p2.x-p1.x
# 	return atan2(b,a)

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
		a = ((p1.x*p2.y-p1.y*p2.x)*(p3.x-p4.x)-(p1.x-p2.x)*(p3.x*p4.y-p3.y*p4.x))
		b = ((p1.x*p2.y-p1.y*p2.x)*(p3.y-p4.y)-(p1.y-p2.y)*(p3.x*p4.y-p3.y*p4.x))
		x=((p1.x*p2.y-p1.y*p2.x)*(p3.x-p4.x)-(p1.x-p2.x)*(p3.x*p4.y-p3.y*p4.x))/delta
		y=((p1.x*p2.y-p1.y*p2.x)*(p3.y-p4.y)-(p1.y-p2.y)*(p3.x*p4.y-p3.y*p4.x))/delta
	return Vector((x,y,0))

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
		"point_on_curve",
		"split_segment",
		"get_2_point_center",
		"get_distance",
		"get_segment_length",
		"get_2_points_angel_2d",
		"get_3_points_angle_2d",
		"get_3_points_angle_3d",
		"get_axis_constraint",
		"get_offset_by_orient"]