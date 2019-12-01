import bpy, math, cmath
from mathutils import Vector, Matrix
from collections import namedtuple
from bpy.types import Operator
from bpy.props import *

param_tollerance = 0.0001

class BsMax_OT_BooleanCurve(Operator):
	bl_idname = "curve.boolean"
	bl_label = "Boolean(test)"

	operation: EnumProperty(name='Type', default='DIFFERENCE',
		items=[('UNION', 'Union', 'Boolean OR', 0),
		('INTERSECTION', 'Intersection', 'Boolean AND', 1),
		('DIFFERENCE', 'Difference', 'Active minus Selected', 2) ])

	def execute(self, ctx):
		splines = ctx.object.data.splines
		spline1 = splines.active
		bpy.ops.curve.spline_type_set(type='BEZIER')
		spline2 = splines[0] if (splines[1] == spline1) else splines[1]
		bezierBooleanGeometry(ctx, spline1, spline2, self.operation)
		return{"FINISHED"}

def bezierBooleanGeometry(ctx, spline1, spline2, operation):
	splines = ctx.object.data.splines
	if not spline1.use_cyclic_u or not spline2.use_cyclic_u:
		return False
	segments1 = bezierSegments([spline1], False)
	segments2 = bezierSegments([spline2], False)

	deletionFlag1 = isPointInSpline(spline1.bezier_points[0].co, spline2)
	deletionFlag2 = isPointInSpline(spline2.bezier_points[0].co, spline1)
	if operation == 'DIFFERENCE':
		deletionFlag2 = not deletionFlag2
	elif operation == 'INTERSECTION':
		deletionFlag1 = not deletionFlag1
		deletionFlag2 = not deletionFlag2
	elif operation != 'UNION':
		return False

	intersections = []
	for segment1 in segments1:
		for segment2 in segments2:
			intersections.extend(segmentIntersection(segment1, segment2))
	if len(intersections) == 0:
		if deletionFlag1:
			splines.remove(spline1)
		if deletionFlag2:
			splines.remove(spline2)
		return True

	prepareSegmentIntersections(segments1)
	prepareSegmentIntersections(segments2)
	subdivideBezierSegmentsOfSameSpline(segments1)
	subdivideBezierSegmentsOfSameSpline(segments2)

	def collectCuts(cuts, segments, deletionFlag):
		for segmentIndex, segment in enumerate(segments):
			if 'extraCut' in segment:
				deletionFlag = not deletionFlag
				segment['extraCut']['index'] = segment['beginIndex']
				segment['extraCut']['deletionFlag'] = deletionFlag
				cuts.append(segment['extraCut'])
			else:
				cuts.append(None)
			cuts.extend(segments[segmentIndex]['cuts'])
			segment['deletionFlag'] = deletionFlag
			for cutIndex, cut in enumerate(segment['cuts']):
				deletionFlag = not deletionFlag
				cut['deletionFlag'] = deletionFlag
	cuts1,cuts2 = [],[]
	collectCuts(cuts1, segments1, deletionFlag1)
	collectCuts(cuts2, segments2, deletionFlag2)

	beginIndex = 0
	for segment in segments1:
		if segment['deletionFlag'] == False:
			beginIndex = segment['beginIndex']
			break
		for cut in segment['cuts']:
			if cut['deletionFlag'] == False:
				beginIndex = cut['index']
				break

	cuts = cuts1
	spline = spline1
	index = beginIndex
	backward = False
	vertices = []
	while True:
		current = spline.bezier_points[index]
		vertices.append([current.handle_left, current.co, current.handle_right])
		if backward:
			current.handle_left, current.handle_right = current.handle_right.copy(), current.handle_left.copy()
		index += len(spline.bezier_points)-1 if backward else 1
		index %= len(spline.bezier_points)
		if spline == spline1 and index == beginIndex:
			break

		cut = cuts[index]
		if cut != None:
			current = spline.bezier_points[index]
			current_handle = current.handle_right if backward else current.handle_left
			spline = spline1 if spline == spline2 else spline2
			cuts = cuts1 if spline == spline1 else cuts2
			index = cut['otherCut']['index']
			backward = cut['otherCut']['deletionFlag']
			next = spline.bezier_points[index]
			if backward:
				next.handle_right = current_handle
			else:
				next.handle_left = current_handle
			if spline == spline1 and index == beginIndex:
				break

	spline = addBezierSpline(ctx.object, True, vertices)
	splines.remove(spline1)
	splines.remove(spline2)
	splines.active = spline
	return True

def isPointInSpline(point, spline):
	return spline.use_cyclic_u and len(xRaySplineIntersectionTest(spline, point))%2 == 1

def bezierSegments(splines, selection_only):
	segments = []
	for spline in splines:
		if spline.type != 'BEZIER':
			continue
		for index, current in enumerate(spline.bezier_points):
			next = spline.bezier_points[(index+1) % len(spline.bezier_points)]
			if next == spline.bezier_points[0] and not spline.use_cyclic_u:
				continue
			if not selection_only or (current.select_right_handle and next.select_left_handle):
				segments.append({
					'spline': spline,
					'beginIndex': index,
					'endIndex': index+1 if index < len(spline.bezier_points)-1 else 0,
					'beginPoint': current,
					'endPoint': next,
					'cuts': []
				})
	return segments

def segmentIntersection(segment1, segment2, tollerance=0.001):
	points1 = bezierSegmentPoints(segment1['beginPoint'], segment1['endPoint'])
	points2 = bezierSegmentPoints(segment2['beginPoint'], segment2['endPoint'])
	result = []
	def addCut(param1, param2):
		cut1 = {'param': param1, 'segment': segment1}
		cut2 = {'param': param2, 'segment': segment2}
		cut1['otherCut'] = cut2
		cut2['otherCut'] = cut1
		segment1['cuts'].append(cut1)
		segment2['cuts'].append(cut2)
		result.append([cut1, cut2])
	if isSegmentLinear(points1) and isSegmentLinear(points2):
		intersection = LineSegmentIntersection(points1[0], points1[3], points2[0], points2[3])
		if intersection != None:
			addCut(intersection[0], intersection[1])
		return result
	solutions = []
	bezierIntersectionBroadPhase(solutions, points1, points2)
	for index in range(0, len(solutions)):
		solutions[index] = bezierIntersectionNarrowPhase(solutions[index], points1, points2)
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
	def areIntersectionsAdjacent(segment1, segment2, param1, param2):
		return segment1['endIndex'] == segment2['beginIndex'] and param1 > 1-param_tollerance and param2 < param_tollerance
	for solution in solutions:
		if (solution[2] > tollerance) or \
		  (segment1['spline'] == segment2['spline'] and \
		  (areIntersectionsAdjacent(segment1, segment2, solution[0], solution[1]) or \
		   areIntersectionsAdjacent(segment2, segment1, solution[1], solution[0]))):
			continue
		addCut(solution[0], solution[1])
	return result

def prepareSegmentIntersections(segments):
	def arecuts1djacent(cut1, cut2):
		return cut1['segment']['beginIndex'] == cut2['segment']['endIndex'] and \
			   cut1['param'] < param_tollerance and cut2['param'] > 1.0-param_tollerance
	for segment in segments:
		segment['cuts'].sort(key=(lambda cut: cut['param']))
		for index in range(len(segment['cuts'])-1, 0, -1):
			prev = segment['cuts'][index-1]
			current = segment['cuts'][index]
			if abs(prev['param']-current['param']) < param_tollerance and \
			   prev['otherCut']['segment']['spline'] == current['otherCut']['segment']['spline'] and \
			   (arecuts1djacent(prev['otherCut'], current['otherCut']) or \
				arecuts1djacent(current['otherCut'], prev['otherCut'])):
				deleteFromArray(prev['otherCut'], prev['otherCut']['segment']['cuts'])
				deleteFromArray(current['otherCut'], current['otherCut']['segment']['cuts'])
				segment['cuts'].pop(index-1 if current['otherCut']['param'] < param_tollerance else index)
				current = segment['cuts'][index-1]['otherCut']
				current['segment']['extraCut'] = current

def subdivideBezierSegmentsOfSameSpline(segments):
	# NOTE: segment['cuts'] must be sorted by param
	indexOffset = 0
	for segment in segments:
		segment['beginIndex'] += indexOffset
		if segment['endIndex'] > 0:
			segment['endIndex'] += indexOffset
		subdivideBezierSegment(segment)
		indexOffset += len(segment['cuts'])
	for segment in segments:
		segment['beginPoint'] = segment['spline'].bezier_points[segment['beginIndex']]
		segment['endPoint'] = segment['spline'].bezier_points[segment['endIndex']]

def addBezierSpline(obj, cyclic, vertices, weights=None, select=False):
	spline = obj.data.splines.new(type='BEZIER')
	spline.use_cyclic_u = cyclic
	spline.bezier_points.add(len(vertices)-1)
	for index, point in enumerate(spline.bezier_points):
		point.handle_left = vertices[index][0]
		point.co = vertices[index][1]
		point.handle_right = vertices[index][2]
		if weights:
			point.weight_softbody = weights[index]
		point.select_left_handle = select
		point.select_control_point = select
		point.select_right_handle = select
		if isSegmentLinear([vertices[index-1][1], vertices[index-1][2], vertices[index][0], vertices[index][1]]):
			spline.bezier_points[index-1].handle_right_type = 'VECTOR'
			point.handle_left_type = 'VECTOR'
	return spline

def xRaySplineIntersectionTest(spline, origin):
	spline_points = spline.bezier_points if spline.type == 'BEZIER' else spline.points
	cyclic_parallel_fix_flag = False
	intersections = []

	def areIntersectionsAdjacent(index):
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

	def appendIntersection(index, root, tangentY, intersectionX):
		beginPoint = spline_points[index-1]
		endPoint = spline_points[index]
		if root == float('inf'): # Segment is parallel to ray
			if index == 0 and spline.use_cyclic_u:
				cyclic_parallel_fix_flag = True
			if len(intersections) > 0 and intersections[-1][1] == beginPoint:
				intersections[-1][1] = endPoint # Skip in adjacency test
		elif intersectionX >= origin[0]:
			intersections.append([beginPoint, endPoint, root, tangentY, intersectionX])
			areIntersectionsAdjacent(len(intersections)-1)

	if spline.type == 'BEZIER':
		for index, endPoint in enumerate(spline.bezier_points):
			if index == 0 and not spline.use_cyclic_u:
				continue
			beginPoint = spline_points[index-1]
			points = (	beginPoint.co,
						beginPoint.handle_right,
						endPoint.handle_left,
						endPoint.co)
			roots = bezierRoots((points[0][1]-origin[1],
								 points[1][1]-origin[1],
								 points[2][1]-origin[1],
								 points[3][1]-origin[1]))
			if roots == float('inf'): # Intersection
				appendIntersection(index, float('inf'), None, None)
			else:
				for root in roots:
					appendIntersection(	index,
										root,
										bezierTangentAt(points, root)[1],
										bezierpoint1t(points, root)[0])

	elif spline.type == 'POLY':
		for index, endPoint in enumerate(spline.points):
			if index == 0 and not spline.use_cyclic_u:
				continue
			beginPoint = spline_points[index-1]
			points = (beginPoint.co, endPoint.co)
			if (points[0][0] < origin[0] and points[1][0] < origin[0]) or \
			   (points[0][1] < origin[1] and points[1][1] < origin[1]) or \
			   (points[0][1] > origin[1] and points[1][1] > origin[1]):
				continue
			diff = points[1]-points[0]
			height = origin[1]-points[0][1]
			if diff[1] == 0: # Parallel
				if height == 0: # Intersection
					appendIntersection(index, float('inf'), None, None)
			else: # Not parallel
				root = height/diff[1]
				appendIntersection(index, root, diff[1], points[0][0]+diff[0]*root)

	if cyclic_parallel_fix_flag:
		appendIntersection(0, float('inf'), None, None)
	areIntersectionsAdjacent(0)
	return intersections

def bezierSegmentPoints(begin, end):
	return [begin.co, begin.handle_right, end.handle_left, end.co]

def isSegmentLinear(points, tollerance=0.0001):
	return 1.0-(points[1]-points[0]).normalized()@(points[3]-points[2]).normalized() < tollerance

def LineSegmentIntersection(begin1, end1, begin2, end2, tollerance=0.001):
	dir1 = end1-begin1
	dir2 = end2-begin2
	param1, param2, point1, point2 = nearestPointOfLines(begin1, dir1, begin2, dir2)
	if math.isnan(param1) or (point1-point2).length > tollerance or \
	   param1 < 0 or param1 > 1 or param2 < 0 or param2 > 1:
		return None
	return (param1, param2, point1, point2)

def aabbIntersectionTest(a, b, tollerance=0.0):
	for i in range(0, 3):
		if abs(a.center[i]-b.center[i]) > a.dimensions[i]+b.dimensions[i]+tollerance:
			return False
	return True

AABB = namedtuple('AxisAlignedBoundingBox', 'center dimensions')

def aabbOfPoints(points):
	min = Vector(points[0])
	max = Vector(points[0])
	for point in points:
		for i in range(0, 3):
			if min[i] > point[i]:
				min[i] = point[i]
			if max[i] < point[i]:
				max[i] = point[i]
	return AABB(center=(max+min)*0.5, dimensions=(max-min)*0.5)

def bezierSliceFromTo(points, minParam, maxParam):
	fromP = bezierpoint1t(points, minParam)
	fromT = bezierTangentAt(points, minParam)
	toP = bezierpoint1t(points, maxParam)
	toT = bezierTangentAt(points, maxParam)
	paramDiff = maxParam-minParam
	return [fromP, fromP+fromT*paramDiff, toP-toT*paramDiff, toP]

def bezierIntersectionBroadPhase(solutions, points1, points2, aMin=0.0, aMax=1.0, bMin=0.0, bMax=1.0, depth=8, tollerance=0.001):
	if aabbIntersectionTest(aabbOfPoints(bezierSliceFromTo(points1, aMin, aMax)), aabbOfPoints(bezierSliceFromTo(points2, bMin, bMax)), tollerance) == False:
		return
	if depth == 0:
		solutions.append([aMin, aMax, bMin, bMax])
		return
	depth -= 1
	aMid = (aMin+aMax)*0.5
	bMid = (bMin+bMax)*0.5
	bezierIntersectionBroadPhase(solutions, points1, points2, aMin, aMid, bMin, bMid, depth, tollerance)
	bezierIntersectionBroadPhase(solutions, points1, points2, aMin, aMid, bMid, bMax, depth, tollerance)
	bezierIntersectionBroadPhase(solutions, points1, points2, aMid, aMax, bMin, bMid, depth, tollerance)
	bezierIntersectionBroadPhase(solutions, points1, points2, aMid, aMax, bMid, bMax, depth, tollerance)

def bezierIntersectionNarrowPhase(broadPhase, points1, points2, tollerance=0.000001):
	aMin = broadPhase[0]
	aMax = broadPhase[1]
	bMin = broadPhase[2]
	bMax = broadPhase[3]
	while (aMax-aMin > tollerance) or (bMax-bMin > tollerance):
		aMid = (aMin+aMax)*0.5
		bMid = (bMin+bMax)*0.5
		a1 = bezierpoint1t(points1, (aMin+aMid)*0.5)
		a2 = bezierpoint1t(points1, (aMid+aMax)*0.5)
		b1 = bezierpoint1t(points2, (bMin+bMid)*0.5)
		b2 = bezierpoint1t(points2, (bMid+bMax)*0.5)
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

def subdivideBezierSegment(segment):
	# Blender only allows uniform subdivision. Use this method to subdivide at arbitrary params.
	# NOTE: segment['cuts'] must be sorted by param
	if len(segment['cuts']) == 0:
		return

	segment['beginPoint'] = segment['spline'].bezier_points[segment['beginIndex']]
	segment['endPoint'] = segment['spline'].bezier_points[segment['endIndex']]
	params = [cut['param'] for cut in segment['cuts']]
	newPoints = bezierSubivideAt(bezierSegmentPoints(segment['beginPoint'], segment['endPoint']), params)
	bpy.ops.curve.select_all(action='DESELECT')
	segment['beginPoint'] = segment['spline'].bezier_points[segment['beginIndex']]
	segment['beginPoint'].select_right_handle = True
	segment['beginPoint'].handle_left_type = 'FREE'
	segment['beginPoint'].handle_right_type = 'FREE'
	segment['endPoint'] = segment['spline'].bezier_points[segment['endIndex']]
	segment['endPoint'].select_left_handle = True
	segment['endPoint'].handle_left_type = 'FREE'
	segment['endPoint'].handle_right_type = 'FREE'

	bpy.ops.curve.subdivide(number_cuts=len(params))
	if segment['endIndex'] > 0:
		segment['endIndex'] += len(params)
	segment['beginPoint'] = segment['spline'].bezier_points[segment['beginIndex']]
	segment['endPoint'] = segment['spline'].bezier_points[segment['endIndex']]
	segment['beginPoint'].select_right_handle = False
	segment['beginPoint'].handle_right = newPoints[0]
	segment['endPoint'].select_left_handle = False
	segment['endPoint'].handle_left = newPoints[-1]

	for index, cut in enumerate(segment['cuts']):
		cut['index'] = segment['beginIndex']+1+index
		newPoint = segment['spline'].bezier_points[cut['index']]
		newPoint.handle_left_type = 'FREE'
		newPoint.handle_right_type = 'FREE'
		newPoint.select_left_handle = False
		newPoint.select_control_point = False
		newPoint.select_right_handle = False
		newPoint.handle_left = newPoints[index*3+1]
		newPoint.co = newPoints[index*3+2]
		newPoint.handle_right = newPoints[index*3+3]

cubic_roots_of_unity = [complex(1, 0), complex(-1, math.sqrt(3))*0.5, complex(-1, -math.sqrt(3))*0.5]
def bezierRoots(dists, tollerance=0.0001):
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

def bezierpoint1t(points, t):
	s = 1-t
	return s*s*s*points[0] + 3*s*s*t*points[1] + 3*s*t*t*points[2] + t*t*t*points[3]

def bezierSubivideAt(points, params):
	if len(params) == 0:
		return []
	newPoints = []
	newPoints.append(points[0]+(points[1]-points[0])*params[0])
	for index, param in enumerate(params):
		paramLeft = param
		if index > 0:
			paramLeft -= params[index-1]
		paramRight = -param
		if index == len(params)-1:
			paramRight += 1.0
		else:
			paramRight += params[index+1]
		point = bezierpoint1t(points, param)
		tangent = bezierTangentAt(points, param)
		newPoints.append(point-tangent*paramLeft)
		newPoints.append(point)
		newPoints.append(point+tangent*paramRight)
	newPoints.append(points[3]-(points[3]-points[2])*(1.0-params[-1]))
	return newPoints

def bezierTangentAt(points, t):
	s = 1-t
	return s*s*(points[1]-points[0])+2*s*t*(points[2]-points[1])+t*t*(points[3]-points[2])
	# return s*s*points[0] + (s*s-2*s*t)*points[1] + (2*s*t-t*t)*points[2] + t*t*points[3]

def boolean_cls(register):
	c = BsMax_OT_BooleanCurve
	if register: bpy.utils.register_class(c)
	else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	boolean_cls(True)

__all__ = ["boolean_cls"]