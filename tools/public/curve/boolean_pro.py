import bpy, cmath
from bpy.types import Operator
from bpy.props import *
from mathutils import Vector
from math import sqrt
from collections import namedtuple
from bsmax.math import point_on_vector,get_segment_length

###############################################################
import numpy as np

def _rect_inter_inner(x1,x2):
	n1=x1.shape[0]-1
	n2=x2.shape[0]-1
	X1=np.c_[x1[:-1],x1[1:]]
	X2=np.c_[x2[:-1],x2[1:]]
	S1=np.tile(X1.min(axis=1),(n2,1)).T
	S2=np.tile(X2.max(axis=1),(n1,1))
	S3=np.tile(X1.max(axis=1),(n2,1)).T
	S4=np.tile(X2.min(axis=1),(n1,1))
	return S1,S2,S3,S4

def _rectangle_intersection_(x1,y1,x2,y2):
	S1,S2,S3,S4=_rect_inter_inner(x1,x2)
	S5,S6,S7,S8=_rect_inter_inner(y1,y2)

	C1=np.less_equal(S1,S2)
	C2=np.greater_equal(S3,S4)
	C3=np.less_equal(S5,S6)
	C4=np.greater_equal(S7,S8)

	ii,jj=np.nonzero(C1 & C2 & C3 & C4)
	return ii,jj

def intersection(x1,y1,x2,y2):
	ii,jj=_rectangle_intersection_(x1,y1,x2,y2)
	n=len(ii)

	dxy1=np.diff(np.c_[x1,y1],axis=0)
	dxy2=np.diff(np.c_[x2,y2],axis=0)

	T=np.zeros((4,n))
	AA=np.zeros((4,4,n))
	AA[0:2,2,:]=-1
	AA[2:4,3,:]=-1
	AA[0::2,0,:]=dxy1[ii,:].T
	AA[1::2,1,:]=dxy2[jj,:].T

	BB=np.zeros((4,n))
	BB[0,:]=-x1[ii].ravel()
	BB[1,:]=-x2[jj].ravel()
	BB[2,:]=-y1[ii].ravel()
	BB[3,:]=-y2[jj].ravel()

	for i in range(n):
		try:
			T[:,i]=np.linalg.solve(AA[:,:,i],BB[:,i])
		except:
			T[:,i]=np.NaN


	in_range= (T[0,:] >=0) & (T[1,:] >=0) & (T[0,:] <=1) & (T[1,:] <=1)

	xy0=T[2:,in_range]
	xy0=xy0.T
	return xy0[:,0],xy0[:,1]
###############################################################

param_tollerance = 0.0001

#https://pomax.github.io/bezierinfo/#introduction

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

def get_bezier_roots(dists, tollerance=0.0001):
	cubic_roots_of_unity = [complex(1,0),complex(-1,sqrt(3))*0.5,complex(-1,-sqrt(3))*0.5]
	# https://en.wikipedia.org/wiki/Cubic_function
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
			if abs(root.imag) < tollerance and root.real > -param_tollerance and root.real < 1.0+param_tollerance:
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

def get_bezier_tangent(points, t):
	s = 1-t
	return s*s*(points[1]-points[0])+2*s*t*(points[2]-points[1])+t*t*(points[3]-points[2])

def get_bezier_point1(points, t):
	s = 1-t
	return s**3*points[0]+3*s*s*t*points[1]+3*s*t*t*points[2]+t**3*points[3]

def xray_spline_intersection(spline, origin):
	spline_points = spline.bezier_points if spline.type == 'BEZIER' else spline.points
	cyclic_parallel_fix_flag = False
	intersections = []

	def are_intersections_adjacent(index):
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

	def append_intersection(index, root, tangentY, intersectionX):
		startpoint = spline_points[index-1]
		endPoint = spline_points[index]
		if root == float('inf'): # Segment is parallel to ray
			if index == 0 and spline.use_cyclic_u:
				cyclic_parallel_fix_flag = True
			if len(intersections) > 0 and intersections[-1][1] == startpoint:
				intersections[-1][1] = endPoint # Skip in adjacency test
		elif intersectionX >= origin.x:
			intersections.append([startpoint, endPoint, root, tangentY, intersectionX])
			are_intersections_adjacent(len(intersections)-1)

	if spline.type == 'BEZIER':
		for index, endPoint in enumerate(spline.bezier_points):
			if index == 0 and not spline.use_cyclic_u:
				continue
			startpoint = spline_points[index-1]
			points = (startpoint.co, 
						startpoint.handle_right,
						endPoint.handle_left,
						endPoint.co)
			roots = get_bezier_roots((points[0].y - origin.y,
								 points[1].y - origin.y,
								 points[2].y - origin.y,
								 points[3].y - origin.y))
			if roots == float('inf'): # Intersection
				append_intersection(index, float('inf'), None, None)
			else:
				for root in roots:
					append_intersection(index, root,
										get_bezier_tangent(points, root)[1],
										get_bezier_point1(points, root)[0])

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
				append_intersection(index, root, diff[1], points[0].x+diff[0]*root)

	if cyclic_parallel_fix_flag:
		append_intersection(0, float('inf'), None, None)
	are_intersections_adjacent(0)
	return intersections

def is_point_in_spline(point, spline):
	return spline.use_cyclic_u and len(xray_spline_intersection(spline, point))%2 == 1

def get_inout_points(spline1, spline2):
	inner, outer, count = [], [], len(spline1.bezier_points)
	for i, point in enumerate(spline1.bezier_points):
		if is_point_in_spline(point.co, spline2):
			inner.append(i)
		else:
			outer.append(i)
	return inner, outer

def get_cross_segments(ins, outs, spline):
	segs, count = [], len(spline.bezier_points)
	for i in range(count):
		sindex = i #if i < count else 0
		eindex = i+1 if i+1 < count else 0
		if (sindex in ins) != (eindex in outs):
			segs.append([sindex,eindex])
	return segs

def is_segment_linear(points, tollerance=0.0001):
	return 1.0-(points[1]-points[0]).normalized()@(points[3]-points[2]).normalized() < tollerance

def line_segment_intersection(begin1, end1, begin2, end2, tollerance=0.001):
	dir1 = end1-begin1
	dir2 = end2-begin2
	param1, param2, point1, point2 = nearestPointOfLines(begin1, dir1, begin2, dir2)
	if math.isnan(param1) or (point1-point2).length > tollerance or \
	   param1 < 0 or param1 > 1 or param2 < 0 or param2 > 1:
		return None
	return (param1, param2, point1, point2)

def aabb_intersection_test(a, b, tollerance=0.0):
	for i in range(0, 3):
		if abs(a.center[i]-b.center[i]) > a.dimensions[i]+b.dimensions[i]+tollerance:
			return False
	return True

def aabb_of_points(points):
	AABB = namedtuple('AxisAlignedBoundingBox', 'center dimensions')
	min = Vector(points[0])
	max = Vector(points[0])
	for point in points:
		for i in range(0, 3):
			if min[i] > point[i]:
				min[i] = point[i]
			if max[i] < point[i]:
				max[i] = point[i]
	return AABB(center=(max+min)*0.5, dimensions=(max-min)*0.5)

def bezier_slice_from_to(points, minParam, maxParam):
	fromP = get_bezier_point1(points, minParam)
	fromT = get_bezier_tangent(points, minParam)
	toP = get_bezier_point1(points, maxParam)
	toT = get_bezier_tangent(points, maxParam)
	paramDiff = maxParam-minParam
	return [fromP, fromP+fromT*paramDiff, toP-toT*paramDiff, toP]

def bezier_intersection_broad_phase(solutions, points1, points2,
									aMin=0, aMax=1, bMin=0, bMax=1,
									depth=8, tollerance=0.001):
	if aabb_intersection_test(aabb_of_points(bezier_slice_from_to(points1, aMin, aMax)),
							  aabb_of_points(bezier_slice_from_to(points2, bMin, bMax)), tollerance) == False:
		return
	if depth == 0:
		solutions.append([aMin, aMax, bMin, bMax])
		return
	depth -= 1
	aMid = (aMin+aMax)*0.5
	bMid = (bMin+bMax)*0.5
	bezier_intersection_broad_phase(solutions, points1, points2, aMin, aMid, bMin, bMid, depth, tollerance)
	bezier_intersection_broad_phase(solutions, points1, points2, aMin, aMid, bMid, bMax, depth, tollerance)
	bezier_intersection_broad_phase(solutions, points1, points2, aMid, aMax, bMin, bMid, depth, tollerance)
	bezier_intersection_broad_phase(solutions, points1, points2, aMid, aMax, bMid, bMax, depth, tollerance)

def bezier_intersection_narrow_phase(broadPhase, points1, points2, tollerance=0.000001):
	aMin = broadPhase[0]
	aMax = broadPhase[1]
	bMin = broadPhase[2]
	bMax = broadPhase[3]
	while (aMax-aMin > tollerance) or (bMax-bMin > tollerance):
		aMid = (aMin+aMax)*0.5
		bMid = (bMin+bMax)*0.5
		a1 = get_bezier_point1(points1, (aMin+aMid)*0.5)
		a2 = get_bezier_point1(points1, (aMid+aMax)*0.5)
		b1 = get_bezier_point1(points2, (bMin+bMid)*0.5)
		b2 = get_bezier_point1(points2, (bMid+bMax)*0.5)
		a1b1Dist = (a1-b1).length
		a2b1Dist = (a2-b1).length
		a1b2Dist = (a1-b2).length
		a2b2Dist = (a2-b2).length
		minDist = min(a1b1Dist, a2b1Dist, a1b2Dist, a2b2Dist)
		if a1b1Dist == minDist:
			aMax = aMid
			bMax = bMid
		elif a2b1Dist == minDist:
			aMin = aMid
			bMax = bMid
		elif a1b2Dist == minDist:
			aMax = aMid
			bMin = bMid
		else:
			aMin = aMid
			bMin = bMid
	return [aMin, bMin, minDist]

def get_boundingbox(points):
	findmin = lambda l: min(l)
	findCenter = lambda l: ( max(l) + min(l) ) / 2
	findmax = lambda l: max(l)
	x,y,z = [[p[i] for p in points] for i in range(3)]
	pmin = [findmin(axis) for axis in [x,y,z]]
	pcenter = [findCenter(axis) for axis in [x,y,z]]
	pmax = [findmax(axis) for axis in [x,y,z]]
	return Vector(pmin), Vector(pcenter), Vector(pmax)

class Segment:
	def __init__(self, spline, indexs):
		self.spline = spline
		self.a = spline.bezier_points[indexs[0]].co
		self.b = spline.bezier_points[indexs[0]].handle_right
		self.c = spline.bezier_points[indexs[1]].handle_left
		self.d = spline.bezier_points[indexs[1]].co
		self.cuts = []
	def split(self, divid):
		s = 1/divid
		self.cuts = [point_on_vector(self.a,self.b,self.c,self.d,t*s) for t in range(divid)]
	def length(self):
		return get_segment_length(self.a,self.b,self.c,self.d,divide)
	def boundingbox(self, start, end, divid):
		step = (end - start) / divid
		cuts = [point_on_vector(self.a,self.b,self.c,self.d,start+t*step) for t in range(divid)]
		pmin, pcen, pmax = get_boundingbox(cuts)
		return [pmin, pmax]


def get_segments_intersection____(segment1, segment2, tollerance=0.001):
	points1 = segment1.segment
	points2 = segment1.segment
	result = []
	def add_cut(param1, param2):
		cut1 = Cut(param1, segment1)
		cut2 = Cut(param2, segment2)
		cut1.target = cut2
		cut2.target = cut1
		segment1.cuts.append(cut1)
		segment2.cuts.append(cut2)
		result.append([cut1, cut2])
	if is_segment_linear(points1) and is_segment_linear(points2):
		intersection = line_segment_intersection(points1[0], points1[3], points2[0], points2[3])
		if intersection != None:
			add_cut(intersection[0], intersection[1])
		return result
	solutions = []
	bezier_intersection_broad_phase(solutions, points1, points2)
	for index in range(0, len(solutions)):
		solutions[index] = bezier_intersection_narrow_phase(solutions[index], points1, points2)
	for index in range(0, len(solutions)):
		for otherIndex in range(0, len(solutions)):
			if solutions[index][2] == float('inf'):
				break
			if index == otherIndex or solutions[otherIndex][2] == float('inf'):
				continue
			diff1 = solutions[index][0]-solutions[otherIndex][0]
			diff2 = solutions[index][1]-solutions[otherIndex][1]
			if diff1*diff1+diff2*diff2 < 0.01:
				if solutions[index][2] < solutions[otherIndex][2]:
					solutions[otherIndex][2] = float('inf')
				else:
					solutions[index][2] = float('inf')
	def are_intersections_adjacent(seg1, seg2, param1, param2):
		return seg1.eindex == seg2.sindex and param1 > 1-param_tollerance and param2 < param_tollerance
	for solution in solutions:
		if (solution[2] > tollerance) or \
		  (segment1.spline == segment2.spline and \
		  (are_intersections_adjacent(segment1, segment2, solution[0], solution[1]) or \
		   are_intersections_adjacent(segment2, segment1, solution[1], solution[0]))):
			continue
		add_cut(solution[0], solution[1])
	return result

# def get_segment_intersections(p0, p1, p2, p3, p4, t):
# 	return (1-t)**4*p0 + 4*t*(1-t)**3*p1 + 6*t**2*(1-t)**2*p2 + 4.t**3*(1-t)*p3 + t**4*p4

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

# def get_linspace(s1, s2, count):
# 	t = np.linspace(0, 1, count)
# 	x1 = point_on_vector(s1.a.x, s1.b.x, s1.c.x, s1.d.x, t)
# 	y1 = point_on_vector(s1.a.y, s1.b.y, s1.c.y, s1.d.y, t)
# 	x2 = point_on_vector(s2.a.x, s2.b.x, s2.c.x, s1.d.x, t)
# 	y2 = point_on_vector(s2.a.y, s2.b.y, s2.c.y, s1.d.y, t)
# 	return x1,y1,x2,y2

# def get_curves_intersection_points(segment1, segment2):
# 	return []

# def get_curves_intersection_points(spline1, segs1, spline2, segs2):
# 	intsecs = []
# 	for a in segs1:
# 		for b in segs2:
# 			segment1 = Segment(spline1, a)
# 			segment2 = Segment(spline2, b)
# 			x1,y1,x2,y2 = get_linspace(segment1, segment2, 100)
# 			x, y = intersection(x1,y1,x2,y2)
# 			for i in range(len(x)):
# 				intsecs.append(Vector((x[i],y[i],0)))
# 	return intsecs

def is_collide_2d(a, b):
	xin, yin = False, False
	if  b[0].x < a[0].x < b[1].x or \
		a[0].x < b[0].x < a[1].x or \
		b[0].x < a[1].x < b[1].x or \
		a[0].x < b[1].x < a[1].x:
		xin = True
	if  b[0].y < a[0].y < b[1].y or \
		a[0].y < b[0].y < a[1].y or \
		b[0].y < a[1].y < b[1].y or \
		a[0].y < b[1].y < a[1].y:
		yin = True
	return (xin and yin)

def get_segments_intersection_points(segment1, segment2):
	points = []
	def scan(boxa,boxb):
		reta,retb = [],[]
		for sa,ea in boxa:
			for sb,eb in boxb:
				box1 = segment1.boundingbox(sa,ea,30)
				box2 = segment2.boundingbox(sb,eb,30)
				if is_collide_2d(box1, box2):
					print("-->",sa,ea,sb,eb)
					m1 = sa+((ea-sa)/2)
					reta += [[sa,m1],[m1,ea]]
					m2 = sb+((eb-sb)/2)
					retb += [[sb,m1],[m1,eb]]
				else:
					print("--<",sa,ea,sb,eb)

		# if len(reta) > 0:
		# 	print("a",reta)
		# if len(retb) > 0:
		# 	print("b",retb)
		return reta, retb
	boxa,boxb = [[0,1]], [[0,1]]
	c, d = scan(boxa,boxb)
	print("cd",c,d)
	f,g = scan(c,d)
	print("fg",f,g)
	scan(f,g)
	return points

def get_curves_intersection_points(spline1, segs1, spline2, segs2):
	intsecs = []
	for a in segs1:
		print("seg1")
		for b in segs2:
			print("seg2")
			segment1 = Segment(spline1, a)
			segment1.split(100)
			segment2 = Segment(spline2, b)
			segment2.split(100)
			intsecs += get_segments_intersection_points(segment1, segment2)
	return intsecs

def boolean(curve, spline1, spline2, mode):
	sp1 = curve.splines[spline1]
	sp2 = curve.splines[spline2]
	sp1in, sp1out = get_inout_points(sp1, sp2)
	sp2in, sp2out = get_inout_points(sp2, sp1)
	sp1crs = get_cross_segments(sp1in, sp1out, sp1)
	sp2crs = get_cross_segments(sp2in, sp2out, sp2)
	intsecs = get_curves_intersection_points(sp1, sp1crs, sp2, sp2crs)
	#print(intsecs)
	print("-------------------")
	

class BsMax_OT_BooleanCurve(Operator):
	bl_idname = "curve.booleanpro"
	bl_label = "Boolean(pro)"

	mode: EnumProperty(name='Type',default='UNION',
		items=[('UNION','Union',''),
		('INTERSECTION','Intersection',''),
		('DIFFERENCE','Difference','') ])

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			if len(ctx.scene.objects) > 0:
				if ctx.object != None:
					if ctx.mode == 'EDIT_CURVE':
						return len(ctx.object.data.splines) > 1
		return False

	def execute(self, ctx):
		curve = ctx.object.data
		splines = curve.splines
		selection = get_curve_selection_index(curve,'close')
		active = get_curve_activespline_index(curve)
		if active != None and len(selection) == 2:
			spline1 = active
			spline2 = selection[0] if selection[0] != active else selection[1]
		#bpy.ops.curve.spline_type_set(type='BEZIER')
		boolean(curve, spline1, spline2, self.mode)
		return{"FINISHED"}

def boolean_cls(register):
	c = BsMax_OT_BooleanCurve
	if register: bpy.utils.register_class(c)
	else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	boolean_cls(True)

__all__ = ["boolean_cls"]