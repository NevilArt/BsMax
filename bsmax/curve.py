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
# 2024/06/17

import math
import cmath
from mathutils import Vector
from copy import deepcopy
from math import sin, cos, atan2, pi
from itertools import product

from bsmax.math import (
	get_lines_intersection,
	split_segment,
	point_on_line,
	point_on_cubic_bezier_curve,
	get_distance,
	get_3_points_angle_3d,
	shift_number,
	bounding_box_colide_with,
	get_cubic_bezier_curve_length,
	get_point_on_spline,
	get_bezier_tangent
)


############################################################################################
## temprary function need to simplifying ###################################################
############################################################################################
param_tollerance = 0.0001
cubic_roots_of_unity = [
	complex(1, 0),
	complex(-1, math.sqrt(3))*0.5,
	complex(-1, -math.sqrt(3))*0.5
]


def get_bezier_roots(dists, tollerance=0.0001):
	# https://en.wikipedia.org/wiki/Cubic_function
	# y(t) = a*t^3 +b*t^2 +c*t^1 +d*t^0
	a = 3*(dists[1]-dists[2])+dists[3]-dists[0]
	b = 3*(dists[0]-2*dists[1]+dists[2])
	c = 3*(dists[1]-dists[0])
	d = dists[0]

	if abs(a) > tollerance: # Cubic
		E2 = a*c
		E3 = a*a*d
		A = (2*b*b-9*E2)*b+27*E3
		B = b*b-3*E2
		C = ((A+cmath.sqrt(A*A-4*B*B*B))*0.5) ** (1/3)
		roots = []

		for root in cubic_roots_of_unity:
			root *= C
			root = -1/(3*a)*(b+root+B/root)

			if abs(root.imag) < tollerance and \
				root.real > -param_tollerance and \
				root.real < 1.0+param_tollerance:
				roots.append(max(0.0, min(root.real, 1.0)))

		# Remove doubles
		roots.sort()
		for index in range(len(roots)-1, 0, -1):
			if abs(roots[index-1]-roots[index]) < param_tollerance:
				roots.pop(index)

		return roots

	elif abs(b) > tollerance: # Quadratic
		disc = c*c-4*b*d
		if disc < 0:
			return []

		disc = math.sqrt(disc)

		return [(-c-disc)/(2*b), (-c+disc)/(2*b)]

	elif abs(c) > tollerance: # Linear
		root = -d/c
		return [root] if root >= 0.0 and root <= 1.0 else []

	else: # Constant / Parallel
		return [] if abs(d) > tollerance else float('inf')


def get_bezier_point1(points, t):
	s = 1-t
	p0, p1, p2, p3 = points
	return s**3*p0 + 3*s*s*t*p1 + 3*s*t*t*p2 + t**3*p3


def are_intersections_adjacent(intersections, index):
	if len(intersections) < 2:
		return

	prev = intersections[index-1]
	current = intersections[index]

	if prev[1] == current[0] and \
		prev[2] > 1.0-param_tollerance and \
		current[2] < param_tollerance and \
		((prev[3] < 0 and current[3] < 0) or \
		(prev[3] > 0 and current[3] > 0)):
		intersections.pop(index)


def append_intersection(
	spline_points ,intersections, origin,
	index, root, tangentY, intersectionX):

	startpoint = spline_points[index-1]
	endPoint = spline_points[index]

	if root == float('inf'): # Segment is parallel to ray
		# if index == 0 and spline.use_cyclic_u:
		# 	cyclic_parallel_fix_flag = True
		if len(intersections) > 0 and intersections[-1][1] == startpoint:
			intersections[-1][1] = endPoint # Skip in adjacency test

	elif intersectionX >= origin.x:
		intersections.append(
			[startpoint, endPoint, root, tangentY, intersectionX]
		)
		
		are_intersections_adjacent(intersections, len(intersections)-1)


def xray_spline_intersection(spline, origin):
	spline_points = spline.bezier_points \
		if spline.type == 'BEZIER' else spline.points

	cyclic_parallel_fix_flag = False
	intersections = []

	if spline.type == 'BEZIER':
		for index, endPoint in enumerate(spline.bezier_points):
			if index == 0 and not spline.use_cyclic_u:
				continue

			startpoint = spline_points[index-1]

			points = (
				startpoint.co, 
				startpoint.handle_right,
				endPoint.handle_left,
				endPoint.co
			)

			a, b, c, d = points
			roots = get_bezier_roots((
				points[0].y - origin.y,
				points[1].y - origin.y,
				points[2].y - origin.y,
				points[3].y - origin.y
			))

			if roots == float('inf'): # Intersection
				append_intersection(
					spline_points ,intersections, origin,
					index, float('inf'), None, None
				)
			else:
				for root in roots:
					append_intersection(
						spline_points,
						intersections, origin,
						index, root,
						get_bezier_tangent(a, b, c, d, root)[1],
						get_bezier_point1(points, root)[0]
					)

	elif spline.type == 'POLY':
		for index, endPoint in enumerate(spline.points):
			if index == 0 and not spline.use_cyclic_u:
				continue

			startpoint = spline_points[index-1]
			points = (startpoint.co, endPoint.co)

			if (points[0].x < origin.x and points[1].x < origin.x) or \
			   (points[0].y < origin.y and points[1].y < origin.y) or \
			   (points[0].y > origin.y and points[1].y > origin.y):
				continue

			diff = points[1]-points[0]
			height = origin[1]-points[0].y

			if diff[1] == 0: # Parallel
				if height == 0: # Intersection
					append_intersection(index, float('inf'), None, None)

			else: # Not parallel
				root = height/diff[1]
				append_intersection(
					spline_points ,intersections, origin,
					index, root, diff[1], points[0].x + diff[0]*root
				)

	if cyclic_parallel_fix_flag:
		append_intersection(
			spline_points ,intersections, origin,
			0, float('inf'), None, None
		)

	are_intersections_adjacent(intersections, 0)

	return intersections


def is_point_in_spline(point, spline):
	return spline.use_cyclic_u and \
		len(xray_spline_intersection(spline, point))%2 == 1


def get_inout_segments(spline, targ):
	inner,outer = [],[]

	for index in range(len(spline.bezier_points)):
		a, b, c, d = get_spline_segment(spline, index)
		p = point_on_cubic_bezier_curve(a, b, c, d, 0.5)

		if is_point_in_spline(p, targ):
			inner.append(index)
		else:
			outer.append(index)

	return inner,outer

############################################################################################
############################################################################################
############################################################################################

def get_devide_range(a, b):
	m = a + ((b-a)/2)
	return [a, m], [m, b]


def get_cros_time(start, end, ps, pe, cross):
	f = get_distance(ps, pe)
	c = get_distance(ps, cross)
	t = end - start
	return start + t*(c/f)


def get_line_offset(p1, p2, val):
	a, b = p1.y-p2.y, p2.x-p1.x
	d = atan2(b, a)
	x, y = cos(d), sin(d)
	return Vector((x, y, 0)) * val


def get_corner_position(p1, p2, p3, val):
	#TODO 
	# teta = get_3_points_angle_2d(p1, p2, p3)
	if False:#(pi - abs(teta)) < 0.001:
		o3 = get_line_offset(p1,p3,val)
		position = o3 + p2
	else:
		o1 = get_line_offset(p1, p2, val)
		o2 = get_line_offset(p2, p3, val)
		lp1 = Vector((p1.x+o1.x, p1.y+o1.y, 0))
		lp2 = Vector((p2.x+o1.x, p2.y+o1.y, 0))
		lp3 = Vector((p2.x+o2.x, p2.y+o2.y, 0))
		lp4 = Vector((p3.x+o2.x, p3.y+o2.y, 0))
		position = get_lines_intersection(lp1, lp2, lp3, lp4)
	
	if position == None:
		# avoid the not spected errores
		position = o1 + p2
	
	return position


def is_spline_selected(spline):
	for point in spline.bezier_points:
		if not point.select_control_point:
			return False
	return True


def get_curve_object_selection(curve, mode:str):
	splines = curve.data.splines
	selection = []
	
	if mode == 'point':
		for spline_index, spline in enumerate(splines):
			bezier_points = spline.bezier_points
			point_indexes = [
				point_index for point_index, point in enumerate(bezier_points)
					if point.select_control_point
			]

			if len(point_indexes) > 0:
				selection.append([spline_index, point_indexes])
			return selection
	
	if mode == 'segment':
		for i, spline in enumerate(splines):
			sel = []
			count = len(spline.bezier_points)

			for j in range(count):
				k = j+1
				if k >= count:

					if spline.use_cyclic_u:
						k = 0
					else:
						break

				point1 = spline.bezier_points[j].select_control_point
				point2 = spline.bezier_points[k].select_control_point

				if point1 and point2:
					sel.append(j)

			if len(sel) > 0:
				selection.append([i, sel])
		return selection
	
	if mode == 'spline':
		for spline in splines:
			if is_spline_selected(spline):
				selection.append(spline)
		return selection
	
	if mode == 'close':
		for spline in splines:
			if not spline.use_cyclic_u:
				continue

			if is_spline_selected(spline):
				selection.append(spline)
		return selection

	return []


def get_boundingbox(points):
	find_min = lambda l: min(l)
	find_max = lambda l: max(l)
	x, y, z = [[p[i] for p in points] for i in range(3)]
	min_point = Vector([find_min(axis) for axis in [x, y, z]])
	max_point = Vector([find_max(axis) for axis in [x, y, z]])
	return BoundingBox(min_point, max_point)


def get_curve_object_active_spline_index(curve):
	active = curve.data.splines.active
	for index, spline in enumerate(curve.data.splines):
		if spline == active:
			return index
	return None


def get_segments_intersection_points(segment_a, segment_b,
		tollerance:float, section_a, section_b):

	diva, divb = [], []
	points = []
	tol = tollerance
	for section_a_start, section_a_end in section_a:
		boundbox_a = get_segment_boundbox(
			segment_a, section_a_start, section_a_end, 30
		)

		for section_b_start, section_b_end in section_b:
			boundbox_b = get_segment_boundbox(
				segment_b, section_b_start, section_b_end, 30
			)

			if not boundbox_a.is_colide_with(boundbox_b):
				continue
			#TODO check and replace
			# bounding_box_colide_with(boundbox_a, boundbox_b, ignore_z=True)

			""" devide bonding box untill one of edge smaller than tollerance """
			diva = get_devide_range(section_a_start, section_a_end) \
				if boundbox_a.width > tol and boundbox_a.length > tol else \
					[[section_a_start, section_a_end]]

			divb = get_devide_range(section_b_start, section_b_end) \
				if boundbox_b.width > tol and boundbox_b.length > tol else \
					[[section_b_start, section_b_end]]

			if (boundbox_a.width <= tol or boundbox_a.length <= tol) and \
				(boundbox_b.width <= tol or boundbox_b.length <= tol):

				""" if both bondig boxes are smaller then tollerance """
				""" get line between start and end of each bonding box """
				point_1 = segment_a.get_point_on(section_a_start)
				point_2 = segment_a.get_point_on(section_a_end)
				point_3 = segment_b.get_point_on(section_b_start)
				point_4 = segment_b.get_point_on(section_b_end)

				""" get cros point of lines """
				co = get_lines_intersection(
					point_1, point_2, point_3, point_4
				)
				
				time1 = get_cros_time(
					section_a_start, section_a_end, point_1, point_2, co
				)
				
				time2 = get_cros_time(
					section_b_start, section_b_end, point_3, point_4, co
				)

				points.append(
					CurveIntersectionPoint(
						segment_a, time1, segment_b, time2, co
					)
				)

			else:
				""" rescan divided boxes """
				points += get_segments_intersection_points(
					segment_a, segment_b, tollerance, diva, divb
				)
	
	# Remove Doubles
	retpoints = []
	for point in points:
		for ret_point in retpoints:
			if get_distance(point.co, ret_point.co) < tollerance/10:
				continue
		retpoints.append(point)

	return retpoints


def get_spline_segments(spline):
	segs = []
	count = len(spline.bezier_points) \
		if spline.use_cyclic_u else len(spline.bezier_points)-1

	for i in range(count):
		segs.append(Segment(spline, i))

	return segs


def get_splines_intersection_points(spline1, spline2, tollerance):
	intsecs = []
	for s1 in get_spline_as_segments(spline1):
		for s2 in get_spline_as_segments(spline2):
			intsecs += get_segments_intersection_points(
				s1, s2, tollerance, [[0, 1]], [[0, 1]]
			)

	return intsecs

#TODO offset do not work properly need to refactor
def spline_offset(spline, value:float):
	if spline.type == 'BEZIER':
		bezier_points = spline.bezier_points
		refrence_points = [
			BezierPoint(bezier_point) for bezier_point in bezier_points
		]

		for index, point in enumerate(bezier_points):
			# check for start and end of spline
			hasleft = True if spline.use_cyclic_u else (index > 0)

			hasright = True if spline.use_cyclic_u \
						else (index < len(bezier_points) - 1)

			# get next and previews besier point index
			left = get_next_index_on_spline(spline, index, riverce=True)
			right = get_next_index_on_spline(spline, index)

			p0 = refrence_points[left].handle_right
			p1 = refrence_points[index].handle_left
			p2 = refrence_points[index].co
			p3 = refrence_points[index].handle_right
			p4 = refrence_points[right].handle_left

			if not hasleft and hasright:
				point.co += get_line_offset(p2, p3, value)
				if point.handle_right_type != 'VECTOR':
					point.handle_right = get_corner_position(
						p2, p3, p4, value
					)
					
			elif hasleft and hasright:
				if point.handle_left_type != 'VECTOR':
					point.handle_left = get_corner_position(
						p0, p1, p2, value
					)

				if point.handle_left_type in {'FREE', 'VECTOR'}:
					point.co = get_corner_position(
						p1, p2, p3, value
					)
				else:
					point.co += get_line_offset(p2, p3, value)

				if point.handle_right_type != 'VECTOR':
					point.handle_right = get_corner_position(
						p2, p3, p4, value
					)

			elif hasleft and not hasright:
				if point.handle_left_type != 'VECTOR':
					point.handle_left = get_corner_position(
						p0, p1, p2, value
					)

				point.co += get_line_offset(p1, p2, value)
	
	if spline.type == 'POLY':
		pass


def bezier_point_normalized(left, co, right):
	n = ((right - co).normalized() - (left - co).normalized()).normalized()
	return Vector((-n[1], n[0], n[2]))


def spline_reverse(spline):
	if not spline:
		return None

	if spline.type == 'BEZIER':
		catche_bezier_point = [
			BezierPoint(bezier_point)
				for bezier_point in reversed(spline.bezier_points)
		]
		
		for index, point in enumerate(catche_bezier_point):
			copy_bezier_point_to(point, spline.bezier_points[index], True)

	if spline.type == 'POLY':
		catche_point = [PolyPoint(point)for point in reversed(spline.points)]
	
		for index, point in enumerate(catche_point):
			copy_poly_point_to(point, spline.points[index])


def copy_bezier_point_to(source, target, mirror:bool=False):
	"Source & Target are bezier_point"
	target.select_control_point = source.select_control_point
	target.hide = source.hide
	target.co = source.co.copy()
	target.tilt = source.tilt
	target.weight_softbody = source.weight_softbody
	target.radius = source.radius

	if mirror:
		target.select_left_handle = source.select_right_handle
		target.select_right_handle = source.select_left_handle
		target.handle_left_type = source.handle_right_type
		target.handle_right_type = source.handle_left_type
		target.handle_left = source.handle_right.copy()
		target.handle_right = source.handle_left.copy()
	else:
		target.select_left_handle = source.select_left_handle
		target.select_right_handle = source.select_right_handle
		target.handle_left_type = source.handle_left_type
		target.handle_right_type = source.handle_right_type
		target.handle_left = source.handle_left.copy()
		target.handle_right = source.handle_right.copy()


def copy_poly_point_to(source, target):
	"Source & Target are poly point"
	#TODO fill with all data
	target.co = source.co.copy()
	target.tilt = source.tilt
	target.weight_softbody = source.weight_softbody	


def spline_insert_bezierpoints(spline, points:list, index:int):
	bezier_points = spline.bezier_points
	count = len(points)
	bezier_points.add(count)

	for i in range(len(bezier_points) - 1, index + count - 1, -1):
		copy_bezier_point_to(bezier_points[i - count], bezier_points[i])

	for i ,point in enumerate(points):
		copy_bezier_point_to(point, bezier_points[index + i])


def spline_divid(spline, index, time):
	start = index
	end = get_next_index_on_spline(spline, index)
	a, b, c, d = get_spline_segment(spline, index)
	p = split_segment(a, b, c, d, time)
	pa = spline.bezier_points[start]
	pc = BezierPoint(pa)
	pe = spline.bezier_points[end]
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
	# spline.bezier_points.insert(index+1, pc)
	spline_insert_bezierpoints(spline, [pc], index+1)


def spline_multi_division(spline, index, times, cos=[]):
	start = index
	end = get_next_index_on_spline(spline, index)
	a, b, c, d = get_spline_segment(spline, index)
	start_point = spline.bezier_points[start]
	center_points = []
	end_point = spline.bezier_points[end]
	start_point.handle_left_type = 'FREE'
	end_point.handle_right_type = 'FREE'

	""" conver count to array of numbers """
	if type(times) == int:
		if times > 0:
			count = times + 1
			times = []
			step = 1 / count
			times = [t*step for t in range(1, count)]

	if type(times) == list:
		if len(cos) == 0:
			times.sort()
			times = [t for t in times if 0 < t < 1]
	else:
		times = []

	if len(times) > 0:
		segs = []
		remain = [
			start_point.co,
			start_point.handle_right,
			end_point.handle_left,
			end_point.co
		]

		for i, time in enumerate(times):
			a, b, c, d = remain
			t = 1 - ((1 - time) / (1 - times[i-1])) if i > 0 else time
			p = split_segment(a, b, c, d, t)
			remain = [p[3].copy(), p[4], p[5], p[6]]
			""" replace co if there was a coorection value """
			if len(cos) > 0:
				p[3] = cos[i]
			segs.append(p)

		start_point.handle_right = segs[0][1] # fix start pionts right handle

		for i, seg in enumerate(segs):
			newpoint = BezierPoint(None)
			newpoint.handle_left_type = 'FREE'
			newpoint.handle_right_type = 'FREE'

			if len(center_points) > 0:
				center_points[-1].handle_right = seg[1]

			newpoint.handle_left = seg[2]
			newpoint.co = seg[3]
			newpoint.handle_right = seg[4]
			center_points.append(newpoint)

		end_point.handle_left = segs[-1][-2] # fix last pionts left handle

	spline_insert_bezierpoints(spline, center_points, index+1)


def spline_merge_bezier_points_by_distance(
		spline, distance:float, selected_only:bool):

	dellist = []

	if len(spline.bezier_points) < 2:
		return

	for index in range(len(spline.bezier_points)):
		if index == 0:
			next_index = len(spline.bezier_points) - 1
		else:
			next_index = index - 1

		dot = spline.bezier_points[index]
		dot1 = spline.bezier_points[next_index]

		while dot1 in dellist and index != next_index:
			next_index -= 1
			if next_index < 0:
				next_index = len(spline.bezier_points)-1
			dot1 = spline.bezier_points[next_index]
		
		if selected_only:
			allowed = (
				dot.select_control_point and dot1.select_control_point
			)
		else:
			allowed = True

		if allowed and (index !=0 or spline.use_cyclic_u):
			if (dot.co-dot1.co).length < distance:
				# remove points and recreate handles
				dot1.handle_right_type = "FREE"
				dot1.handle_right = dot.handle_right
				dot1.co = (dot.co + dot1.co) / 2
				dellist.append(dot)
			else:
				# Handles that are on main point position converts to vector,
				# if next handle are also vector
				
				if dot.handle_left_type == 'VECTOR' and\
					(dot1.handle_right - dot1.co).length < distance:
					dot1.handle_right_type = "VECTOR"

				if dot1.handle_right_type == 'VECTOR' and\
					(dot.handle_left - dot.co).length < distance:
					dot.handle_left_type = "VECTOR"

	delindex = []
	for bezier_point in dellist:
		index = spline_get_point_index(spline, bezier_point)
		if index:
			delindex.append(index)

	spline_bezier_point_remove(spline, delindex)


def collect_splines_divisions(intersections):
	divisions = []
	
	def spline_append(segment, time:float, co):
		""" co is a corraction point from segment intersection detector """
		isNewSpline = True
		for div in divisions:
			if segment.spline == div.spline:
				isNewSegment = True

				for dseg in div.segments:
					if segment.index == dseg.index:
						dseg.times.append(time)
						dseg.cos.append(co)
						isNewSegment = False
						break

				if isNewSegment:
					""" creat a new SegmentDivisions object """
					div.segments.append(SegmentDivisions(segment.index, time, co))

				isNewSpline = False
		
		""" create a new SplineDivisions object """
		if isNewSpline:
			newdiv = SplineDivisions(
				segment.spline,
				SegmentDivisions(segment.index, time, co)
			)

			divisions.append(newdiv)

	for intersection in intersections:
		spline_append(
			intersection.segment1, intersection.time1, intersection.co
		)
		
		spline_append(
			intersection.segment2, intersection.time2, intersection.co
		)

	for division in divisions:
		division.sort(reverse=True)

		for division_segment in division.segments:
			division_segment.sort()

	return divisions


def curve_append(curve, spline):
	if curve.type != 'CURVE' or not spline:
		return
	
	splines = curve.data.splines

	if spline.type == 'BEZIER':
		new_spline = splines.new(type='BEZIER')
		spline_copy(new_spline, spline)

	if spline.type == 'POLY':
		new_spline = splines.new(type='POLY')
		spline_copy(new_spline, spline)
	
	if not new_spline:
		return

	new_spline.tilt_interpolation = spline.tilt_interpolation
	new_spline.radius_interpolation = spline.radius_interpolation
	new_spline.type = spline.type
	new_spline.order_u = spline.order_u
	new_spline.order_v = spline.order_v
	new_spline.resolution_u = spline.resolution_u
	new_spline.resolution_v = spline.resolution_v
	new_spline.use_cyclic_u = spline.use_cyclic_u
	new_spline.use_cyclic_v = spline.use_cyclic_v
	new_spline.use_endpoint_u = spline.use_endpoint_u
	new_spline.use_endpoint_v = spline.use_endpoint_v
	new_spline.use_bezier_u = spline.use_bezier_u
	new_spline.use_bezier_v = spline.use_bezier_v
	new_spline.use_smooth = spline.use_smooth
	new_spline.hide = spline.hide
	new_spline.material_index = spline.material_index


def is_gap(spline1, index1, spline2, index2, distance, selectedonly):
	if selectedonly:
		if not spline1.bezier_points[index1].select_control_point or\
			not spline2.bezier_points[index2].select_control_point:
			return False

	if spline1.use_cyclic_u or spline2.use_cyclic_u:
		return False

	if spline1 == spline2 and index1 == index2:
		return False

	newDistance = get_distance(
		spline1.bezier_points[index1].co,
		spline2.bezier_points[index2].co
	)

	return newDistance <= distance


def spline_bezier_point_remove(spline, index):
	pass


def collaps_splines(curve, spline_a, spline_b):
	spline_a.bezier_points[-1].handle_right_type = "FREE"
	handle_right = spline_b.bezier_points[0].handle_right
	spline_a.bezier_points[-1].handle_right = handle_right

	if spline_a == spline_b:
		spline_a.use_cyclic_u = True
	else:
		spline_join(spline_a, spline_b, trim=1)
		curve.data.splines.remove(spline_b)

	return True

def curve_merge_gaps_by_distance(curve, distance, selectedonly):
	splines = curve.data.splines
	hasgap = True
	while hasgap:
		hasgap = False

		"""self loop"""
		for spline in splines:
			if is_gap(spline, 0, spline, -1, distance, selectedonly):
				hasgap = collaps_splines(curve, spline, spline)

		for spline1, spline2 in product(splines, splines):
			"""end to head"""
			if is_gap(spline1, -1, spline2, 0, distance, selectedonly):
				hasgap = collaps_splines(curve, spline1, spline2)
				break

			"""head to heads"""
			if is_gap(spline1, 0, spline2, 0, distance, selectedonly):
				spline_reverse(spline1)
				hasgap = collaps_splines(curve, spline1, spline2)
				break

			"""end to ends"""
			if is_gap(spline1, -1, spline2, -1, distance, selectedonly):
				spline_reverse(spline2)
				hasgap = collaps_splines(curve, spline1, spline2)
				break

			"""head to end """
			if is_gap(spline1, 0, spline2, -1, distance, selectedonly):
				hasgap = collaps_splines(curve, spline2, spline1)
				break


def curve_break_point(curve, spline, points):
	""" seprate spline from given point indexe
		spline can be Spline class or index
	"""
	if type(spline) == int:
		spline = curve.data.splines[spline]

	points.sort()

	if spline.use_cyclic_u:
		first = points[0]
		spline_make_first(spline, first)
		spline_insert_bezierpoints(
			spline,
			[spline.bezier_points[0]],
			len(spline.bezier_points)
		)
		spline.use_cyclic_u = False
		maximum = len(spline.bezier_points)
		points = [shift_number(i, -first, 0, maximum) for i in points]
		points.sort()

	if not spline.use_cyclic_u and points[0] != 0:
		newspline = Spline(spline)
		newspline.bezier_points = spline.bezier_points[0 : points[0] + 1]
		curve_append(curve, newspline)

	for index in range(len(points)):
		newspline = Spline(spline)
		start = points[index]

		if index < len(points) - 1:
			end = points[index + 1] + 1
			newspline.bezier_points = spline.bezier_points[start:end]

		else:
			newspline.bezier_points = spline.bezier_points[start:]

		curve_append(curve, newspline)

	curve_remove(curve, spline)


def curve_replace_spline(curve, old_spline, new_spline):
	pass


def curve_delete_segments(curve, spline, indexes):
	indexes.sort()
	segments, new = [], []

	splineindex = 0
	for index, sp in enumerate(curve.data.splines):
		if sp == spline:
			splineindex = index
			break

	for index in range(len(spline.bezier_points)):
		if index not in indexes:
			new.append(index)
			continue

		if len(new) > 0:
			segments.append(new.copy())
			new.clear()

	if len(new) > 0:
		segments.append(new.copy())

	splines = []
	for indexes in segments:
		""" clone same spline to have same properties """
		newspline = Spline(spline)
		newspline.use_cyclic_u = False
		count = len(indexes)
		
		for i, index in enumerate(indexes):
			
			newspline.bezier_points.append(spline.bezier_points[index])

			if i >= count-1:
				right = get_next_index_on_spline(spline, index)
				newspline.bezier_points.append(spline.bezier_points[right])
		#TODO need copy a of spline
		splines.append(newspline)

	# """ replace first part with original and append others """
	# curve.data.splines[splineindex] = splines[0]
	# curve_remove(curve.data.splines[splineindex])
	# curve_append(splines[0])
	# old_spline = curve.data.splines[splineindex]
	# new_spline = splines[0]
	# curve_replace_spline(curve, old_spline, new_spline)
	# splines.pop(0)

	for newspline in splines:
		curve_append(curve, newspline)
		# curve.splines.append(newspline)


def curve_swap(curve, index1, index2):
	count = len(curve.data.splines)
	if index1 < count and index2 < count:
		temp = curve.data.splines[index1]
		curve.data.splines[index1] = curve.data.splines[index2]
		curve.data.splines[index2] = temp
		return True

	return False


def spline_clone(curve, spline_index):
	if type(spline_index) == int:
		if spline_index < len(curve.data.splines):
			spline = curve.data.splines[spline_index]
	else:
		spline = spline_index

	if not spline:
		return None

	if spline.type == 'BEZIER':
		new_spline = curve.data.splines.new(type='BEZIER')
		new_spline.bezier_points.add(len(spline.bezier_points) - 1)
		
		for index, point in enumerate(spline.bezier_points):
			bezier_point = new_spline.bezier_points[index]
			bezier_point.co = point.co
			bezier_point.handle_left = point.handle_left
			bezier_point.handle_right = point.handle_right
			bezier_point.tilt = point.tilt
			bezier_point.weight_softbody = point.weight_softbody

	if spline.type == 'POLY':
		new_spline = curve.data.splines.new(type='POLY')
		new_spline.points.add(len(spline.points) - 1)
		
		for index, point in enumerate(spline.points):
			point = new_spline.points[index]
			point.co = point.co
			point.tilt = point.tilt
			point.weight_softbody = point.weight_softbody

	new_spline.use_cyclic_u = spline.use_cyclic_u
	new_spline.use_smooth = spline.use_smooth

	return new_spline


def spline_join(spline_a, spline_b, trim:int=0):
	""" trim ignores the first points of the second spline """
	if not spline_a or not spline_b:
		return
	
	if spline_a.type == spline_b.type =='BEZIER':
		for index in range(trim, len(spline_b.bezier_points)):
			spline_a.bezier_points.add(1)
			copy_bezier_point_to(
				spline_b.bezier_points[index],
				spline_a.bezier_points[-1] 
			)

	if spline_a.type == spline_b.type == 'POLY':
		for index in range(trim, len(spline_b.points)):
			spline_a.points.add(1)
			copy_poly_point_to(
				spline_b.points[index],
				spline_a.points[-1]
			)

def spline_copy(spline_a, spline_b):
	if not spline_a or not spline_b:
		return
	
	if spline_a.type == spline_b.type =='BEZIER':
		count = len(spline_b.bezier_points)
		spline_a.bezier_points.add(count-1)
		for index in range(count):
			copy_bezier_point_to(
				spline_b.bezier_points[index],
				spline_a.bezier_points[index] 
			)

	if spline_a.type == spline_b.type == 'POLY':
		count = len(spline_b.points)
		spline_a.points.add(count-1)
		for index in range(count):
			copy_poly_point_to(
				spline_b.points[index],
				spline_a.points[index]
			)


# def spline_remove(self, index):
# 	if type(index) == int:
# 		self.bezier_points.pop(index)

# 	elif type(index) == list:
# 		index.sort(reverse=True)
# 		for i in index:
# 			self.bezier_points.pop(i)


def spline_remove(curve, spline_index):
	if type(spline_index) == int:
		if spline_index < len(curve.date.splines):
			spline = curve.date.splines[spline_index]
	else:
		spline = spline_index
	
	if not spline:
		return

	curve.data.splines.remove(spline)


def curve_remove(curve, spline):
	if type(spline) == int:
		curve.data.splines.pop(spline)

	if type(spline) == Spline:
		for index, spline in enumerate(curve.splines):
			if spline == spline:
				curve.data.splines.pop(index)
				break


def get_segment_boundbox(segment, start:float, end:float, divid:int):
	""" Get bundbox of part of segment\n
		Segment is a besier curve with a, b, c, d values\n
		start to end by time for get a range 0~1
		divid is number of cuts needed
	"""
	step = (end - start) / divid
	cuts = [
		point_on_cubic_bezier_curve(
			segment.a, segment.b, segment.c, segment.d, start + time*step
		) 
		for time in range(divid + 1)
	]
	return get_boundingbox(cuts)


def segment_get_section_line(segment, start, end):
	point_a = point_on_cubic_bezier_curve(
		segment.a, segment.b, segment.c, segment.d, start
	)
	point_b = point_on_cubic_bezier_curve(
		segment.a, segment.b, segment.c, segment.d, end
	)
	return Line(point_a, point_b)


def segment_divisions_append(self, time, co):
	if 0 < time < 1 and not time in self.times:
		self.times.append(time)
		self.cos.append(co)


def segment_divisions_sort(self, reverse):
	times = self.times.copy()
	cos = self.cos.copy()
	self.cos.clear()
	self.times.sort(reverse=reverse)
	
	""" sort correction point as time sort """
	for time in self.times:
		self.cos.append(cos[times.index(time)])


def spline_divisions_sort(self, reverse):
	indexes = [sd.index for sd in self.segments]
	indexes.sort(reverse=reverse)
	segments = []

	for i in indexes:
		for s in self.segments:
			if i == s.index:
				segments.append(s)
				break

	self.segments = deepcopy(segments)


def get_next_index_on_spline(spline, index:int, riverce:bool=False):
	if riverce:
		if index == 0:
			return len(spline.bezier_points) - 1 if spline.use_cyclic_u else index
		return index - 1

	if index >= len(spline.bezier_points) - 1:
		return 0 if spline.use_cyclic_u else index

	return index + 1


def get_spline_segment(spline, index:int):
	start = index
	end = get_next_index_on_spline(spline, index)
	a = spline.bezier_points[start].co
	b = spline.bezier_points[start].handle_right
	c = spline.bezier_points[end].handle_left
	d = spline.bezier_points[end].co
	return a, b, c, d


def get_spline_segment_length(spline, index:int, steps:int=100):
	if index <= len(spline.bezier_points)-2:
		a, b, c, d = get_spline_segment(spline, index)
		return get_cubic_bezier_curve_length(a, b, c, d, steps=steps)
	return 0


def get_spline_as_segments(spline):
	count = len(spline.bezier_points)\
		if spline.use_cyclic_u else len(spline.bezier_points)-1
	return [Segment(spline, index) for index in range(count)]


def spline_set_free(spline, full=True):
	if not spline.bezier_points:
		return

	if full:
		for point in spline.bezier_points:
			point.handle_left_type = 'FREE'
			point.handle_right_type = 'FREE'

	if not spline.use_cyclic_u:
		ps,pe = spline.bezier_points[0], spline.bezier_points[-1]
		ps.handle_left_type = 'VECTOR'

		if ps.handle_right_type in {'AUTO','ALIGNED'}:
			ps.handle_right_type = 'FREE'

		if ps.handle_left_type in {'AUTO','ALIGNED'}:
			pe.handle_left_type = 'FREE'

		pe.handle_right_type = 'VECTOR'


def spline_make_first(spline, index):
	if spline.use_cyclic_u:
		bezier_points = [BezierPoint(point) for point in spline.bezier_points]
		arranged_bezier_points = bezier_points[index:] + bezier_points[0:index]

		for i, point in enumerate(arranged_bezier_points):
			copy_bezier_point_to(point, spline.bezier_points[i])

	elif index == len(spline.bezier_points) - 1:
		spline_reverse(spline)


def spline_select(spline, state:bool):
	for point in spline.bezier_points:
		point.select_left_handle = state
		point.select_right_handle = state
		point.select_control_point = state


def spline_get_point_index(spline, point):
	for index, bezier_point in enumerate(spline.bezier_points):
		if point == bezier_point:
			return index
	return None


class SegmentDivisions:
	def __init__(self, index, time, co):
		self.index = index
		self.times = [time]
		self.cos = [co]
	
	def append(self, time, co):
		segment_divisions_append(self, time, co)
	
	def sort(self, reverse=False):
		segment_divisions_sort(self, reverse)


class SplineDivisions:
	def __init__(self, spline, segsub):
		self.spline = spline
		self.segments = [segsub]
	
	def sort(self, reverse=False):
		spline_divisions_sort(self, reverse)


class Line:
	def __init__(self, a, b):
		self.a = a
		self.b = b

	def point_on_line(self, t):
		return point_on_line(self.a, self.b, t)

	def get_length(self):
		return get_distance(self.a, self.b)

	def get_angel_2d(self):
		return atan2(self.b.x - self.a.x, self.a.y - self.b.y)

	def get_intersection_with(self, target):
		return get_lines_intersection(self.a, self.b, target.a, target.b)


class BoundingBox:
	def __init__(self, start, end):
		self.start = start
		self.end = end
		self.width = end.x - start.x
		self.length = end.y - start.y
		self.height = end.z - start.z
		self.center = (start + end) / 2
	
	def is_inside_of(self, target):
		return False
	
	def is_cover_the(self, target):
		return False
	
	def is_colide_with(self, target):
		return bounding_box_colide_with(self, target)


class CurveIntersectionPoint:
	def __init__(self, segment1, time1, segment2, time2, co):
		self.segment1 = segment1
		self.time1 = time1
		self.segment2 = segment2
		self.time2 = time2
		self.co = co


class PolyPoint:
	def __init__(self, poly_point):
		self.select = False
		self.hide = False
		self.co = Vector((0, 0, 0))
		self.tilt = 0
		self.weight = 1
		self.weight_softbody = 0.001
		self.radius = 1
		
		if not poly_point:
			return
		
		self.select = poly_point.select
		self.hide = poly_point.hide
		self.co = poly_point.co.copy()
		self.tilt = poly_point.tilt
		self.weight = poly_point.weight
		self.weight_softbody = poly_point.weight_softbody
		self.radius = poly_point.radius


class BezierPoint:
	def __init__(self, bezier_point):
		if bezier_point:
			self.select_left_handle = bezier_point.select_left_handle
			self.select_right_handle = bezier_point.select_right_handle
			self.select_control_point = bezier_point.select_control_point
			self.hide = bezier_point.hide
			self.handle_left_type = bezier_point.handle_left_type
			self.handle_right_type = bezier_point.handle_right_type
			self.handle_left = bezier_point.handle_left.copy()
			self.co = bezier_point.co.copy()
			self.handle_right = bezier_point.handle_right.copy()
			self.tilt = bezier_point.tilt
			self.weight_softbody = bezier_point.weight_softbody
			self.radius = bezier_point.radius
		else:
			self.select_left_handle = False
			self.select_right_handle = False
			self.select_control_point = False
			self.hide = False
			self.handle_left_type = 'VECTOR'
			self.handle_right_type = 'VECTOR'
			self.handle_left = Vector((0, 0, 0))
			self.co = Vector((0, 0, 0))
			self.handle_right = Vector((0, 0, 0))
			self.tilt = 0
			self.weight_softbody = 0.001
			self.radius = 1


class Segment:
	def __init__(self, spline, index):
		start = index
		end = get_next_index_on_spline(spline, index)
		self.spline = spline
		self.index = index
		self.a = spline.bezier_points[start].co
		self.b = spline.bezier_points[start].handle_right
		self.c = spline.bezier_points[end].handle_left
		self.d = spline.bezier_points[end].co
		self.start = BezierPoint(spline.bezier_points[start])
		self.end = BezierPoint(spline.bezier_points[end])
	
	def get_point_on(self, t):
		return point_on_cubic_bezier_curve(
			self.a, self.b, self.c, self.d, t
		)

	def get_section_line(self, start, end):
		segment_get_section_line(self, start, end)
	
	def get_length(self, steps=100):
		return get_cubic_bezier_curve_length(
			self.a, self.b, self.c, self.d, steps=steps
		)

class Spline:
	def __init__(self, spline):
		if spline:
			self.points = [
				PolyPoint(point) for point in spline.points
			]

			self.bezier_points = [
				BezierPoint(bezier_point) for bezier_point in spline.bezier_points
			]

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
			self.points = []
			self.bezier_points = []
			self.tilt_interpolation = 'LINEAR'
			self.radius_interpolation = 'LINEAR'
			self.type = 'LINEAR'
			self.point_count_u = 2
			self.point_count_v = 0
			self.order_u = 0
			self.order_v = 0
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