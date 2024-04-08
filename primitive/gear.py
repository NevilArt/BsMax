############################################################################
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation,either version 3 of the License,or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not,see <https://www.gnu.org/licenses/>.
############################################################################

# The original author is "Vojtech Cada" that was create this amazing plugin
# for 3DsMax by max script.

import bpy

from math import tan, atan, sin, cos, sqrt, pi, degrees, isclose, radians
from numpy import cross
from mathutils import Vector

from bsmax.math import dot, get_distance, BitArray
from bsmax.bsmatrix import matrix_from_elements
from primitive.primitive import Primitive_Geometry_Class, Draw_Primitive

def getMmPerUnit (unitssystemType):
	# {'inches':25.4, 'feet':304.8, }
	if unitssystemType == 'inches':
		return 25.4
	if unitssystemType == 'feet':
		return 304.8
	if unitssystemType == 'miles':
		return 1609344.
	if unitssystemType == 'centimeters':
		return 10.0
	if unitssystemType == 'meters':
		return 1e3
	if unitssystemType == 'kilometers':
		return 1e6
	return 1.0

# parameters main rollout:params
# (
# 	toothCount default:20 type:#integer ui:spnToothCount
# 	pitchRadius default:20 type:#worldUnits ui:spnPitchRadius
# 	holeRadius default:4 type:#worldUnits ui:spnHoleRadius
# 	faceWidth default:4 type:#worldUnits ui:spnFaceWidth
# 	toothSegs default:5 type:#integer ui:spnSegs
# 	innerSegs default:2 type:#integer ui:spnInnerSegs
# 	heightSegs default:1 type:#integer ui:spnHeightSegs
# 	smooth default:true type:#boolean ui:chxSmooth

# 	pressureAngle default:20 type:#angle ui:spnPressureAngle
# 	profileShift default:0 type:#float ui:spnProfileShift
# 	clearance default:0.25 type:#float ui:spnclearance
# 	precision default:0.01 type:#float animatable:false ui:spnPrecision
# 	mmPerUnit default:0 type:#float animatable:false ui:spnMmPerUnit

# 	on toothCount set count do (toothAngle = 180 / (halfN = count / 2d0); this.params.spnModule.value = this.params.getModule (mmPerUnit != 0))
# 	on pitchRadius set val do this.params.spnModule.value = this.params.getModule (mmPerUnit != 0)
# )
class Gear_Data():
	def __init__(self):
		self.involutePoints = []
		self.trochoidPoints = []
		self.toothAngle = radians(18) #pi/10 #18
		self.halfN = 1.5

		self.toothCount = 3
		self.pitchRadius = 2
		self.holeRadius = 8
		self.faceWidth = 20
		self.toothSegs = 3
		self.innerSegs = 2
		self.heightSegs = 1
		self.smooth = True

		self.pressureAngle = radians(20) #<--
		self.profileShift = 0
		self.clearance = 0.1
		self.precision = 0.01
		self.mmPerUnit = 0

		self.spnModule = 0

		self.toothCount_set(self.toothCount)
	
	def getModule(self, conversionSet):
		# 2 * pitchRadius / toothCount * (if conversionSet then mmPerUnit else getMmPerUnit())
		return	2 * self.pitchRadius / self.toothCount * (self.mmPerUnit if conversionSet else getMmPerUnit(""))

	def toothCount_set(self, count):
		# toothAngle = 180 / (halfN = count / 2d0);
		# this.params.spnModule.value = this.params.getModule (mmPerUnit != 0)
		self.halfN = count / 2
		self.toothAngle = pi / self.halfN
		self.spnModule = self.getModule(self.mmPerUnit != 0)
		self.pitchRadius_set()
	
	def pitchRadius_set(self):
		# self.params.spnModule.value = self.params.getModule (mmPerUnit != 0)
		self.spnModule = self.getModule(self.mmPerUnit != 0)

gear = Gear_Data()


# UI
# rollout params "Parameters"
# (
# 	group "Basic"
# 	(
# 		spinner spnToothCount "Tooth Count: " type:#integer fieldWidth:50 range:[3, 1e6, 20]
# 		spinner spnModule "Module [mm]: " type:#float fieldWidth:50 range:[0.1, 1e6, 2] tooltip:"The length of the pitch circle diameter per tooth.\nIf the units are generic units, they are treated as millimeters."
# 		spinner spnPitchRadius "Pitch Radius: " type:#worldUnits fieldWidth:50 range:[1e-6, 1e9, 20] tooltip:"The diameter of a circle which by pure rolling action would produce the same motion as toothed gear."
# 		spinner spnHoleRadius "Hole Radius: " type:#worldUnits fieldWidth:50 range:[1e-9, 1e9, 4]
# 		spinner spnFaceWidth "Face Width: " type:#worldUnits fieldWidth:50 range:[-1e9, 1e9, 4]
# 		spinner spnSegs "Tooth Segs: " type:#integer fieldWidth:50 offset:[0,10] range:[3, 1e6, 5]
# 		spinner spnInnerSegs "Inner Segs: " type:#integer fieldWidth:50 range:[2, 1e6, 1]
# 		spinner spnHeightSegs "Height Segs: " type:#integer fieldWidth:50 range:[1, 1e6, 1]
# 		checkBox chxSmooth "Smooth" align:#right
# 	)

# 	group "Advanced"
# 	(
# 		spinner spnPressureAngle "Pressure Angle: " fieldWidth:50 range:[1, 90, 20] tooltip:"Common values are 14.5, 20 and 25 degrees.\nFor 14.51° pressure angle the usual clearance is equal to pi / 20.\nFor 20° pressure angle it is to 0.225 - 0.25"
# 		spinner spnProfileShift "Profile Shift: " fieldWidth:50 range:[-0.5, 0.6, 0] tooltip:"Used most often to prevent undercut.\nIndicates what portion of gear one's addendum height should be shifted to gear two."
# 		spinner spnclearance "Clearance Coeff. " fieldWidth:50 range:[0.1, 0.3, pi/20d0]
# 		spinner spnPrecision "Precision: " fieldWidth:50 scale:1e-3 range:[1e-3, 0.1, 0.01]
# 		spinner spnMmPerUnit "mm per Unit: " fieldWidth:50 indeterminate:true range:[0, 1e9, 0]
# 	)

# 	fn getModule conversionSet =
# 		2 * pitchRadius / toothCount * (if conversionSet then mmPerUnit else getMmPerUnit())

# 	on params open do
# 	(
# 		local conversionSet = mmPerUnit != 0
# 		spnMmPerUnit.indeterminate = NOT conversionSet
# 		spnModule.value = getModule conversionSet
# 	)

# 	on spnModule changed val do
# 	(
# 		pitchRadius = toothCount / 2d0 * val / (if mmPerUnit != 0 then mmPerUnit else getMmPerUnit())
# 		redrawViews()
# 	)
# )

def on_open():
	conversionSet = gear.mmPerUnit != 0
	# spnMmPerUnit.indeterminate = not conversionSet
	gear.spnModule = gear.getModule(conversionSet)

def spnModule_update(val):
	gear.pitchRadius = gear.toothCount / 2 * val / (gear.mmPerUnit if gear.mmPerUnit != 0 else getMmPerUnit(""))

# local flipMeshNormals = meshOp.flipNormals
# flipMeshNormals = True #meshOp.flipNormals

# struct segment (index = 0, box, elements)
class segment():
	def __init__(self, index, box, element):
		self.index = index
		self.box = box
		self.elements = element

# struct rect
# (
# 	p1, p2,
# 	x = amin p1.x p2.x,
# 	y = amin p1.y p2.y,
# 	w = abs (p1.x - p2.x),
# 	h = abs (p1.y - p2.y),
# 	left = x,
# 	right = x + w,
# 	bottom = y,
# 	top = y + h
# )

class rect():
	def __init__(self, p1, p2):
		self.p1 = p1 #type = Vector())
		self.p2 = p2 #type = Vector())
		self.x = min(p1.x, p2.x)
		self.y = min(p1.y, p2.y)
		self.w = abs(p1.x - p2.x)
		self.h = abs(p1.y - p2.y)
		self.left = self.x
		self.right = self.x + self.w
		self.bottom = self.y
		self.top = self.y + self.h

# fn isOdd nr =
# 	bit.and 1L nr != 0
def isOdd(num):
	return not (num % 2) == 0

# fn getUnitRoot rad =
# 	(rad^2 + 1)^.5
def getUnitRoot (rad):
	return (rad**2 + 1)**0.5

# fn getTangent outer inner =
# 	(((outer / inner)^2 - 1)^.5)
def getTangent(outer, inner):
	return ((outer / inner)**2 - 1)**0.5

# fn getUnwindAngle ang =
# 	radToDeg ang - atan ang
def getUnwindAngle(ang):
	# return (degrees(ang) - atan(ang))
	return ang - atan(ang)

# fn getNthVal n nMax valMin valMax mult:1d0 =
# 	(valMin * (nMax - n * mult) + valMax * n * mult) / nMax
def getNthVal(n, nMax, valMin, valMax, mult=1):
	return (valMin * (nMax - n * mult) + valMax * n * mult) / nMax

# fn wrapIndex nr lower upper =
# 	int(mod (nr - lower) (upper - lower + 1)) + lower
def wrapIndex(nr, lower, upper):
	return int((nr - lower) % (upper - lower + 1)) + lower

# fn doBoxesIntersect b1 b2 =
# 	abs(b1.x - b2.x) < (b1.w + b2.w) AND abs(b1.y - b2.y) < (b1.h + b2.h)
def doBoxesIntersect(b1, b2):
	return abs(b1.x - b2.x) < (b1.w + b2.w) and abs(b1.y - b2.y) < (b1.h + b2.h)

# fn isPointInSegment p1 p2 pos =
# (
# 	local proj = (dot (normalize (p2 - p1)) (pos - p1))
# 	proj >= 0 AND proj <= length (p2 - p1) AND close_enough ((dot (normalize (p2 - p1)) (normalize (pos - p1)))) 1 10
# )

def length(vec):
    return sqrt(vec.x**2 + vec.y**2 + vec.z**2)

def isPointInSegment(p1, p2, pos):
	proj = dot((p2-p1).normalized(), (pos-p1))
	return 0 <= proj <= length(p2-p1) and \
		isclose(dot((p2-p1).normalized(), (pos-p1).normalized()), 1, rel_tol=10)

# fn doSegmentsContainPt s1 s2 pt =
# 	isPointInSegment s1.p1 s1.p2 pt AND isPointInSegment s2.p1 s2.p2 pt
def doSegmentsContainPt(s1, s2, pt):
	return isPointInSegment(s1.p1, s1.p2, pt) and isPointInSegment(s2.p1, s2.p2, pt)

# fn getLineIntersection p1 p2 p3 p4 =
# (
# 	local cross1 = cross (normalize (p2 - p1)) (normalize (p4 - p3))
# 	local cross2 = cross (p3 - p1) (normalize (p4 - p3))
# 	p1 + normalize (p2 - p1) * dot cross2 cross1 / dot cross1 cross1
# )
def getLineIntersection(p1, p2, p3, p4):
	cross1 = Vector(cross(((p2-p1).normalized()), ((p4-p3).normalized())))
	cross2 = Vector(cross((p3-p1), ((p4-p3).normalized())))
	return (p1+(p2-p1).normalized() * dot(cross2, cross1) / dot(cross1, cross1))

# fn getBoxForBoxes b1 b2 =
# 	rect p1:[amin b1.left b2.left, amax b1.top b2.top] \
# 			p2:[amax b1.right b2.right, amin b1.bottom b2.bottom]
def getBoxForBoxes(b1, b2):
	return rect(
			p1=Vector((min(b1.left, b2.left), max(b1.top, b2.top), 0)),
			p2=Vector((max(b1.right, b2.right), min(b1.bottom, b2.bottom), 0))
			)

# fn getSegments points =
# 	for i = 2 to points.count collect
# 		segment index:i box:(rect p1:points[i-1] p2:points[i]) elements:#(points[i-1], points[i])
def getSegments(points):
	return [
			segment(i,
					rect(points[i-1], points[i]),
					[points[i-1], points[i]]
			)
					for i in range(2, len(points))
	]
		
# fn getSegmentTree segments =
# 	if segments.count > 2 then
# 	(
# 		local newSegments = for i = 2 to segments.count by 2 collect
# 			segment box:(getBoxForBoxes segments[i-1].box segments[i].box) elements:#(segments[i-1], segments[i])
# 		if isOdd segments.count do append newSegments segments[segments.count]
# 		getSegmentTree newSegments
# 	)
# 	else if segments.count == 2 then
# 		segment box:(getBoxForBoxes segments[1].box segments[2].box) elements:#(segments[1], segments[2])
# 	else segments[1]
def getSegmentTree(segments):
	if len(segments) > 2:
		newSegments =[
			segment(0,
					getBoxForBoxes(segments[i-1].box, segments[i].box),
					[segments[i-1], segments[i]]
			)
			for i in range(1, len(segments)-1, 2)
		]
		
		if isOdd(len(segments)):
			# newSegments.append(segments[len(segments)])
			newSegments.append(segments[-1])

		return getSegmentTree(newSegments)

	elif len(segments) == 2:
		return segment(0,
						(getBoxForBoxes(segments[0].box, segments[1].box)),
						[segments[0], segments[1]]
				)
	else:
		return segments[0]

# fn findIntersections seg1 seg2 intersections:#() =
# (
# 	if doBoxesIntersect seg1.box seg2.box then
# 	(
# 		if seg1.index > 0 AND seg2.index > 0 then
# 		(
# 			local intersection = getLineIntersection seg1.box.p1 seg1.box.p2 seg2.box.p1 seg2.box.p2
# 			if doSegmentsContainPt seg1.box seg2.box intersection do
# 			(
# 				append intersections intersection
# 				append intersections seg1.index
# 				append intersections seg2.index
# 			)
# 		)
# 		else if seg1.index > 0 then
# 		(
# 			findIntersections seg1 seg2.elements[1] intersections:intersections
# 			findIntersections seg1 seg2.elements[2] intersections:intersections
# 		)
# 		else if seg2.index > 0 then
# 		(
# 			findIntersections seg1.elements[1] seg2 intersections:intersections
# 			findIntersections seg1.elements[2] seg2 intersections:intersections
# 		)
# 		else
# 		(
# 			findIntersections seg1.elements[1] seg2.elements[1] intersections:intersections
# 			findIntersections seg1.elements[1] seg2.elements[2] intersections:intersections
# 			findIntersections seg1.elements[2] seg2.elements[1] intersections:intersections
# 			findIntersections seg1.elements[2] seg2.elements[2] intersections:intersections
# 		)
# 	)
# 	intersections
# )
def findIntersections(seg1, seg2, intersections=[]):
	if doBoxesIntersect(seg1.box, seg2.box):
		if seg1.index > 0 and seg2.index > 0:
			intersection = getLineIntersection(seg1.box.p1, seg1.box.p2,
												seg2.box.p1, seg2.box.p2)
			if doSegmentsContainPt(seg1.box, seg2.box, intersection):
				intersections.append(intersection)
				intersections.append(seg1.index)
				intersections.append(seg2.index)
		elif seg1.index > 0:
			findIntersections(seg1, seg2.elements[0], intersections=intersections)
			findIntersections(seg1, seg2.elements[1], intersections=intersections)
		elif seg2.index > 0:
			findIntersections(seg1.elements[0], seg2, intersections=intersections)
			findIntersections(seg1.elements[1], seg2, intersections=intersections)
		else:
			findIntersections(	seg1.elements[0],
								seg2.elements[0],
								intersections=intersections
			)
			findIntersections(	seg1.elements[0],
								seg2.elements[1],
								intersections=intersections
			)
			findIntersections(	seg1.elements[1],
								seg2.elements[0],
								intersections=intersections
			)
			findIntersections(	seg1.elements[1],
								seg2.elements[1],
								intersections=intersections
			)
	return intersections

# fn intersectToothCurves involutePoints trochoidPoints =
# (
# 	local involuteCurve = getSegmentTree (getSegments involutePoints)
# 	local trochoidCurve = getSegmentTree (getSegments trochoidPoints)

# 	local intersections = findIntersections involuteCurve trochoidCurve

# 	if intersections.count < 1 then
# 	(
# 		local intersection = trochoidPoints[1]
# 		this.involutePoints = for p in involutePoints where p.y > intersection.y collect p
# 	)
# 	else
# 	(
# 		this.involutePoints = for i = 1 to intersections[2] - 1 collect involutePoints[i]
# 		this.trochoidPoints = for i = intersections[3] to trochoidPoints.count collect trochoidPoints[i]
# 		append involutePoints intersections[1]
# 		insertItem intersections[1] this.trochoidPoints 1
# 	)
# )

def intersectToothCurves(involutePoints, trochoidPoints):
	involuteCurve = getSegmentTree(getSegments(involutePoints))
	trochoidCurve = getSegmentTree(getSegments(trochoidPoints))

	intersections = findIntersections(involuteCurve, trochoidCurve)

	if len(intersections) < 1:
		# intersection = trochoidPoints[1]
		intersection = trochoidPoints[0]
		involutePoints = [p for p in involutePoints if p.y > intersection.y]
	else:
		involutePoints = [involutePoints[i]
								for i in range(0, intersections[1] - 1)
		]

		trochoidPoints = [trochoidPoints[i]
								for i in range(intersections[2],
												len(trochoidPoints))
		]

		involutePoints.append(intersections[0])
		# intersections[0].insert(trochoidPoints, 1)
		trochoidPoints.insert(1, intersections[0])

# fn getInterpolatedPts points count =
# (
# 	local total = 0d0
# 	local lengths = for i = 2 to points.count collect (d = distance points[i-1] points[i]; total += d; d)
# 	local step = total / count * (1 - precision / 100)

# 	local pts = #()
# 	local accum = 0d0
# 	for i = 2 to points.count do
# 	(
# 		accum += lengths[i-1]
# 		while accum >= step do
# 			append pts (points[i] + (accum -= step) * normalize (points[i-1] - points[i]))
# 	)
# 	pts
# )
def getInterpolatedPts(points, count):
	total = 0
	lengths = []
	for i in range(1, len(points)):
		d = get_distance(points[i-1], points[i])
		total += d
		lengths.append(d)
	step = total / count * (1 - gear.precision / 100)

	pts, accum = [], 0
	for i in range(1, len(points)):
		accum += lengths[i-1]
		while accum >= step:
			accum -= step
			pts.append(points[i] + accum * (points[i-1] - points[i]).normalized())
	return pts

# fn getUnitToothPoints segIters =
# (
# 	free involutePoints
# 	free trochoidPoints

# 	local addendum = 1 + profileShift
# 	local dedendum = (1 - profileShift) + clearance

# 	local V = (profileShift - 1) / tan pressureAngle
# 	local U = V * (tan pressureAngle)^2 - clearance * (getUnitRoot (tan pressureAngle)) - pi / 4

# 	local offsetAngle = toothAngle / 4 + getUnwindAngle (tan pressureAngle)
# 	local involuteMax = getTangent (1 + addendum / halfN) (cos pressureAngle)

# 	local angleMin = radToDeg ((U + V) / halfN)
# 	local angleMax = radToDeg (U / halfN)

# 	for seg = 0 to segIters do
# 	(
# 		local trochoidAngle = getNthVal seg segIters angleMin angleMax mult:0.99d0
# 		local involuteAngle = getUnwindAngle (getNthVal seg segIters involuteMax 0) - offsetAngle

# 		if involuteAngle < 0 do append involutePoints \
# 			(cos pressureAngle * getUnitRoot (getNthVal seg segIters involuteMax 0) * [sin involuteAngle, cos involuteAngle, 0])

# 		local stepV = getNthVal seg segIters -V 0 mult:0.99d0

# 		local M = V * tan pressureAngle / stepV
# 		local N = clearance / getUnitRoot M
# 		local P = N * M + V * tan pressureAngle + halfN

# 		local x = P * sin trochoidAngle + (N + stepV) * cos trochoidAngle
# 		local y = P * cos trochoidAngle - (N + stepV) * sin trochoidAngle

# 		append trochoidPoints ([x, y, 0] / halfN)
# 	)
# 	append trochoidPoints ((1 - dedendum / halfN) * [-sin (toothAngle / 2), cos (toothAngle / 2), 0])

# 	intersectToothCurves involutePoints trochoidPoints

# 	local toothPoints = #(involutePoints[1])
# 	for p in (getInterpolatedPts involutePoints toothSegs) do append toothPoints p
# 	for p in (getInterpolatedPts trochoidPoints toothSegs) do append toothPoints p
# 	toothPoints
# )
def getUnitToothPoints(segIters):
	global gear
	gear.involutePoints.clear()
	gear.trochoidPoints.clear()

	addendum = 1 + gear.profileShift
	dedendum = 1 - gear.profileShift + gear.clearance

	# tanPressureAngle = tan(gear.pressureAngle)
	V = (gear.profileShift - 1) / tan(gear.pressureAngle)
	U = V * (tan(gear.pressureAngle))**2 - gear.clearance * (getUnitRoot(tan(gear.pressureAngle))) - pi / 4

	offsetAngle = gear.toothAngle / 4 + getUnwindAngle(tan(gear.pressureAngle))
	involuteMax = getTangent((1 + addendum / gear.halfN), (cos(gear.pressureAngle)))

	# angleMin = degrees((U + V) / gear.halfN)
	# angleMax = degrees(U / gear.halfN)
	angleMin = (U + V) / gear.halfN
	angleMax = U / gear.halfN

	for seg in range(0, segIters):
		trochoidAngle = getNthVal(seg, segIters, angleMin, angleMax, mult=0.99)
		involuteAngle = getUnwindAngle(
							(getNthVal(seg, segIters, involuteMax, 0)) - offsetAngle
						)

		if involuteAngle < 0:
			# involutePoints.append (cos(gear.pressureAngle) * \
			# 	getUnitRoot(getNthVal(seg, segIters, involuteMax, 0)) * \
			# 		[sin(involuteAngle), cos(involuteAngle), 0])
			s = cos(gear.pressureAngle) * getUnitRoot(getNthVal(seg, segIters, involuteMax, 0))
			gear.involutePoints.append(Vector((s*sin(involuteAngle), s*cos(involuteAngle), 0)))

		stepV = getNthVal(seg, segIters, -V, 0, mult=0.99)

		M = V * tan(gear.pressureAngle) / stepV
		N = gear.clearance / getUnitRoot(M)
		P = N * M + V * tan(gear.pressureAngle) + gear.halfN

		x = P * sin(trochoidAngle + (N + stepV)) * cos(trochoidAngle)
		y = P * cos(trochoidAngle - (N + stepV)) * sin(trochoidAngle)

		# trochoidPoints.append([x, y, 0] / halfN)
		gear.trochoidPoints.append(Vector((x/gear.halfN, y/gear.halfN, 0)))

	# trochoidPoints.append((1 - dedendum / halfN) * [-sin(toothAngle / 2), cos(toothAngle / 2), 0])
	s = (1 - dedendum / gear.halfN)
	gear.trochoidPoints.append(Vector((-sin(gear.toothAngle/2)*s, cos(gear.toothAngle/2)*s, 0)))

	intersectToothCurves(gear.involutePoints, gear.trochoidPoints)

	# toothPoints = [gear.involutePoints[1]]
	toothPoints = [gear.involutePoints[0]]
	for p in (getInterpolatedPts(gear.involutePoints, gear.toothSegs)):
		toothPoints.append(p)
	for p in (getInterpolatedPts(gear.trochoidPoints, gear.toothSegs)):
		toothPoints.append(p)
	return toothPoints



# fn getReversedFace face =
# 	[face.z, face.y, face.x]
def getReversedFace(face, offset):
	return[face[2]+offset, face[1]+offset, face[0]+offset]

# fn addQuad pt1 pt2 pt3 pt4 &faces =
# (
# 	append faces [pt1, pt4, pt3]
# 	append faces [pt3, pt2, pt1]
# )
def addQuad(pt1, pt2, pt3, pt4, faces):
	faces.append([pt1, pt4, pt3])
	faces.append([pt3, pt2, pt1])

# fn addRow pts1 pts2 row rows count &vertList new:true =
# 	if row == 0 then pts1 else if row == rows then pts2
# 	else if NOT new then for i = vertList.count - count + 1 to vertList.count collect i
# 	else
# 	(
# 		local lastVert = vertList.count
# 		join vertList (for i = 1 to count collect getNthVal row rows vertList[pts1[i]] vertList[pts2[i]])
# 		for i = lastVert + 1 to lastVert + count collect i
# 	)
def addRow(pts1, pts2, row, rows, count, vertList, new=True):
	if row == 0:
		return pts1
	elif row == rows:
		return pts2
	elif not new:
		return [i for i in range(len(vertList) - count + 1, len(vertList))]
	else:
		lastVert = len(vertList)
		vertList.join([getNthVal(row, rows, vertList[pts1[i]], vertList[pts2[i]]) for i in range(1, count)])
		return[i for i in range(lastVert + 1, lastVert + count)]

# fn makeQuadStrip pts1 pts2 count &faceList closed:false =
# (
# 	if closed do count -= 1
# 	for offset = 1 to count do
# 		addQuad pts1[offset] pts1[offset + 1] pts2[offset + 1] pts2[offset] &faceList

# 	if closed do addQuad pts1[count + 1] pts1[1] pts2[1] pts2[count + 1] &faceList
# )
def makeQuadStrip(pts1, pts2, count, faceList, closed=False):
	if closed:
		count -= 1
	#TODO TEMPRARY
	mincount = min(len(pts1), len(pts2))
	count = mincount if count > mincount else count
	for offset in range(0, count-1):
		addQuad(pts1[offset], pts1[offset + 1], pts2[offset + 1], pts2[offset], faceList)

	if closed:
		addQuad(pts1[count + 1], pts1[1], pts2[1], pts2[count + 1], faceList)

# fn makeMultiStrip pts1 pts2 count loops &faceList &vertList closed:false =
# 	for row = 1 to loops do
# 		makeQuadStrip (addRow pts1 pts2 (row - 1) loops pts1.count &vertList new:false) \
# 						(addRow pts1 pts2 row loops pts1.count &vertList) \
# 						count &faceList closed:closed
def makeMultiStrip(pts1, pts2, count, loops, faceList, vertList, closed=False):
	for row in range(0, loops-1):
		makeQuadStrip(	addRow(pts1, pts2, (row-1), loops, len(pts1), vertList, new=False),
						addRow(pts1, pts2, row, loops, len(pts1), vertList), 
						count,
						faceList,
						closed=closed
		)

# fn getOuterPoints toothCount toothPtCount midCount offset:1 pts:#{} =
# (
# 	for i = 0 to toothCount-1 do
# 		pts += #{offset + i * toothPtCount .. offset + 2 * toothSegs + i * toothPtCount, \
# 					offset + 2 * toothSegs + midCount + i * toothPtCount .. offset + (i + 1) * toothPtCount - 1}

# 	pts = pts as array
# 	for i = pts.count to 1 by -1 collect pts[i]
# )
def getOuterPoints(toothCount, toothPtCount, midCount, offset=1, pts=[]):
	bitarray = BitArray()

	for i in range(0, toothCount-1):
		# bstr = str(offset + i * toothPtCount) + '-'
		# bstr += str(offset + 2 * gear.toothSegs + i * toothPtCount) + ','
		# bstr += str(offset + 2 * gear.toothSegs + midCount + i * toothPtCount) + '-'
		# bstr += str(offset + (i + 1) * toothPtCount - 1)
		bstr = str(offset + i * toothPtCount - 1) + '-'
		bstr += str(offset + 2 * gear.toothSegs + i * toothPtCount - 1) + ','
		bstr += str(offset + 2 * gear.toothSegs + midCount + i * toothPtCount - 1) + '-'
		bstr += str(offset + (i + 1) * toothPtCount - 2)
		
		bitarray.set(bstr)
		pts += bitarray.get()
	
	pts = pts.reverse()

	# for i in range(len(pts), 1, -1):
	# 	pts[i]

# fn addSingleNGonPoints n radius &vertList segments:1 clockwise:false =
# (
# 	local angle = 360d0/n * (if clockwise then 1 else -1)
# 	local prevPos = [0, radius, 0]
# 	local dist = 2 * radius * sin angle / segments

# 	for i = 1 to n do
# 	(
# 		local pos = radius * [sin (i*angle), cos (i*angle), 0]
# 		local step = (pos - prevPos) / segments

# 		for i = 0 to segments-1 do append vertList (prevPos + i * step)
# 		prevPos = pos
# 	)
# )
def addSingleNGonPoints(n, radius, vertList, segments=1, clockwise=False):
	angle = 360/n * (1 if clockwise else -1)
	prevPos = Vector((0, radius, 0))
	# dist = 2 * radius * sin(angle) / segments

	for i in range(1, n):
		pos = radius * Vector((sin(i*angle), cos(i*angle), 0))
		step = (pos - prevPos) / segments

		for i in range(0,segments-1):
			vertList.append(prevPos + i * step)
		prevPos = pos

# fn addNGonsPoints holeRadius rootRadius loops innerDiv &vertList =
# 	for i = 1 to loops do
# 	(
# 		local mult = getNthVal i innerSegs 1d0 0d0
# 		addSingleNGonPoints toothCount (((1 - mult) * holeRadius + mult * rootRadius) / cos (toothAngle/2)) &vertList segments:innerDiv
# 	)
def addNGonsPoints(holeRadius, rootRadius, loops, innerDiv, vertList):
	global gear
	for i in range(1, loops):
		mult = getNthVal(i, gear.innerSegs, 1, 0)
		addSingleNGonPoints(gear.toothCount,
							(((1 - mult) * holeRadius + mult * rootRadius) / cos(gear.toothAngle/2)),
							vertList,
							segments=innerDiv)

# fn addTeethPoints pitchRadius toothCount toothPoints innerCount &vertList =
# 	for tooth = 0 to toothCount-1 do
# 	(
# 		local angle = tooth * toothAngle

# 		for i = toothPoints.count-1 to 1 by - 1 do
# 			append vertList (pitchRadius * toothPoints[i] * [-1,1,0] * rotateZMatrix angle)

# 		for i = 1 to toothPoints.count-innerCount do
# 			append vertList (pitchRadius * toothPoints[i] * [0,1,0] * rotateZMatrix angle)

# 		for p in toothPoints do
# 			append vertList (pitchRadius * p * rotateZMatrix angle)
# 	)
def rotateZMatrix(angle):
	return matrix_from_elements((0, 0, 0), (0, 0, angle), (1, 1, 1))

def addTeethPoints(pitchRadius, toothCount, toothPoints, innerCount, vertList):
	global gear
	for tooth in range(0, toothCount):
		angle = tooth * gear.toothAngle #toothAngle alredy is radian

		# for i in range(len(toothPoints)-1, 1, -1):
		for i in range(len(toothPoints)-1, 0, -1):
			vertList.append((pitchRadius * toothPoints[i] * Vector((-1,1,0)) @ rotateZMatrix(angle)))

		# for i in range(1, len(toothPoints)-innerCount):
		for i in range(0, len(toothPoints)-innerCount):
			vertList.append(pitchRadius * toothPoints[i] * Vector((0,1,0)) @ rotateZMatrix(angle))

		for p in toothPoints:
			vertList.append(pitchRadius * p @ rotateZMatrix(angle))

# fn getCurvedLoop offset baseCount midCount =
# 	for i = offset + midCount to (offset + midCount + 4 * toothSegs) collect wrapIndex i 1 baseCount
def getCurvedLoop(offset, baseCount, midCount):
	return [wrapIndex(i, 1, baseCount)
			for i in range (offset + midCount, (offset + midCount + 4 * gear.toothSegs))]

# fn getStraightLoop offset baseCount loopCount midCount toothPtCount innerDiv =
# 	join (for i = offset to offset + midCount - 1 collect wrapIndex i 1 baseCount) \
# 			(for i = baseCount + innerDiv * (offset / toothPtCount) + 1 to baseCount + innerDiv * (1 + offset / toothPtCount) + 1 collect wrapIndex i (baseCount + 1) (baseCount + loopCount)) + \
# 			(for i = offset + toothPtCount + midCount - 1 to offset + toothPtCount by - 1 collect wrapIndex i 1 baseCount)
def getStraightLoop(offset, baseCount, loopCount, midCount, toothPtCount, innerDiv):
	retarray =[wrapIndex(i, 1, baseCount) for i in range(offset, offset + midCount - 1)]

	retarray +=[wrapIndex(i, (baseCount + 1), (baseCount + loopCount))
				for i in range(
								int(baseCount + innerDiv * (offset / toothPtCount) + 1),
								int(baseCount + innerDiv * (1 + offset / toothPtCount) + 1)
						)
	]

	retarray +=[wrapIndex(i, 1, baseCount)
				for i in range(offset + toothPtCount + midCount - 1, offset + toothPtCount, - 1)]

	return retarray

# fn makeOuterFlatFaces baseCount loopCount midCount toothPtCount innerDiv &faceList =
# 	for offset = 2 * toothSegs + 1 to baseCount by toothPtCount do
# 		makeQuadStrip (getCurvedLoop offset baseCount midCount) \
# 						(getStraightLoop offset baseCount loopCount midCount toothPtCount innerDiv) \
# 						(4 * toothSegs) &faceList
def makeOuterFlatFaces(baseCount, loopCount, midCount, toothPtCount, innerDiv, faceList):

	# for offset in range(2 * gear.toothSegs, baseCount-1, toothPtCount):
	print(">>-->>", 2*gear.toothSegs+1, baseCount, toothPtCount)
	for offset in range(2 * gear.toothSegs+1, baseCount, toothPtCount):
		makeQuadStrip(	(getCurvedLoop(offset, baseCount, midCount)),
						(getStraightLoop(offset, baseCount, loopCount, midCount,
										toothPtCount, innerDiv)),
						(4 * gear.toothSegs),
						faceList
		)

# fn makeInnerFlatFaces loops baseCount loopCount stripCount &faceList =
# 	for i = 0 to loops do
# 		makeQuadStrip (#{baseCount + i * loopCount + 1 .. baseCount + (i+1) * loopCount} as array) \
# 						(#{baseCount + (i+1) * loopCount + 1 .. baseCount + (i+2) * loopCount} as array) \
# 						stripCount &faceList closed:true
def makeInnerFlatFaces(loops, baseCount, loopCount, stripCount, faceList):
	bitarray = BitArray()
	
	for i in range(0, loops):
		# bstr1 = str(baseCount + i * loopCount + 1) + '-' + str(baseCount + (i+1) * loopCount)
		# bstr2 = str(baseCount + (i+1) * loopCount + 1) + '-' + str(baseCount + (i+2) * loopCount)
		bstr1 = str(baseCount + i * loopCount) + '-' + str(baseCount + (i+1) * loopCount - 1)
		bstr2 = str(baseCount + (i+1) * loopCount) + '-' + str(baseCount + (i+2) * loopCount - 1)
		bitarray.set(bstr1)
		array1 = bitarray.get()
		bitarray.set(bstr2)
		array2 = bitarray.get()
		makeQuadStrip( array1 , array2, stripCount, faceList, closed=True)

# fn makeOuterLoopFaces toothCount toothPtCount midCount basePointCount &faceList &vertList =
# 	makeMultiStrip (getOuterPoints toothCount toothPtCount midCount) \
# 					(getOuterPoints toothCount toothPtCount midCount offset:(basePointCount + 1)) \
# 					(toothCount * (toothPtCount - midCount + 1)) heightSegs &faceList &vertList closed:true
def makeOuterLoopFaces(toothCount, toothPtCount, midCount, basePointCount, faceList, vertList):
	makeMultiStrip( (getOuterPoints(toothCount, toothPtCount, midCount)),
					(getOuterPoints(toothCount, toothPtCount, midCount, offset=(basePointCount + 1))),
					(toothCount * (toothPtCount - midCount + 1)),
					gear.heightSegs,
					faceList,
					vertList,
					closed=True
	)

# fn makeInnerLoopFaces basePointCount loopCount &faceList &vertList =
# 	makeMultiStrip (#{basePointCount - loopCount + 1 .. basePointCount} as array) \
# 					(#{2 * basePointCount - loopCount + 1 .. 2 * basePointCount} as array) \
# 					loopCount heightSegs &faceList &vertList closed:true
def makeInnerLoopFaces(basePointCount, loopCount, faceList, vertList):
	bitarray = BitArray()
	# bitarray.set(str(basePointCount - loopCount + 1) + '-' + str(basePointCount))
	# pts1 = bitarray.get()
	# bitarray.set(str(2 * basePointCount - loopCount + 1) + '-' + str(2 * basePointCount))
	# pts2 = bitarray.get()
	bitarray.set(str(basePointCount - loopCount) + '-' + str(basePointCount - 1))
	pts1 = bitarray.get()
	bitarray.set(str(2 * basePointCount - loopCount) + '-' + str(2 * basePointCount - 1))
	pts2 = bitarray.get()
	makeMultiStrip( pts1, pts2, loopCount, gear.heightSegs, faceList, vertList, closed=True)

# fn smoothFaces obj flatFaceCount faceCount facetCount =
# (
# 	for face = 1 to flatFaceCount do setFaceSmoothGroup obj face 1
# 	for face = flatFaceCount + 1 to faceCount do setFaceSmoothGroup obj face 2
# 	for i = 0 to facetCount do
# 	(
# 		local f = flatFaceCount + 1 + (2 * i + 1) * toothSegs * 4 + i * 4
# 		for face = f to f+3 do setFaceSmoothGroup obj face 4
# 	)
# )
def smoothFaces(obj, flatFaceCount, faceCount, facetCount):
	pass
	# for face in range(1, flatFaceCount):
	# 	setFaceSmoothGroup(obj, face, 1)

	# for face in range(flatFaceCount + 1, faceCount):
	# 	setFaceSmoothGroup(obj, face, 2)

	# for i in range(0, facetCount):
	# 	f = flatFaceCount + 1 + (2 * i + 1) * toothSegs * 4 + i * 4
	# 	for face in range(f, f+3):
	# 		setFaceSmoothGroup(obj, face, 4)

# fn clampHoleRadius rootRadius =
# (
# 	disableRefMsgs()
# 	holeRadius = amin holeRadius (0.9 * rootRadius)
# 	enableRefMsgs()
# )
def clampHoleRadius(rootRadius):
	gear.holeRadius = min(gear.holeRadius, (0.9 * rootRadius))

# on clone original do
# (
# 	toothAngle = original.toothAngle
# 	halfN = original.halfN
# )
def clone_original():
	# gear.toothAngle = original.toothAngle
	# gear.halfN = original.halfN
	pass

# on buildMesh do
# (
# 	local vertList = #()
# 	local faceList = #()

# 	local innerCount = int((toothSegs + 1) / 2)
# 	local innerDiv = 2 * (innerCount-1)
# 	local midCount = 2 * toothSegs - (innerCount - 1)
# 	local toothPtCount = 1 + 4 * toothSegs + midCount
# 	local baseCount = toothCount * toothPtCount
# 	local loopCount = toothCount * innerDiv

# 	local toothPoints = this.getUnitToothPoints (int(1 / precision))
# 	local rootRadius = pitchRadius * length toothPoints[toothPoints.count]

# 	clampHoleRadius rootRadius

# 	addTeethPoints pitchRadius toothCount toothPoints innerCount &vertList
# 	addNGonsPoints holeRadius rootRadius (innerSegs-1) innerDiv &vertList
# 	addSingleNGonPoints loopCount holeRadius &vertList

# 	makeOuterFlatFaces baseCount loopCount midCount toothPtCount innerDiv &faceList
# 	makeInnerFlatFaces (innerSegs - 2) baseCount loopCount (toothCount * innerDiv) &faceList

# 	local basePointCount = vertList.count
# 	join vertList (for vert in vertList collect Point3 vert.x vert.y faceWidth)
# 	join faceList (for face in faceList collect basePointCount + getReversedFace face)
# 	local flatFaceCount = faceList.count

# 	makeOuterLoopFaces toothCount toothPtCount midCount basePointCount &faceList &vertList
# 	makeInnerLoopFaces basePointCount loopCount &faceList &vertList

# 	setMesh mesh vertices:vertList faces:faceList

# 	for face in mesh.faces do
# 		setEdgeVis mesh face.index 3 false

# 	if faceWidth < 0 do
# 		flipMeshNormals mesh #all

# 	if NOT smooth then
# 		for face = 1 to faceList.count do
# 			setFaceSmoothGroup mesh face 0
# 	else
# 		smoothFaces mesh flatFaceCount faceList.count (heightSegs * toothCount - 1)
# )
def buildMesh():
	vertList, faceList = [], []
	_faceList = []

	innerCount = int((gear.toothSegs + 1) / 2)
	innerDiv = 2 * (innerCount-1)
	midCount = 2 * gear.toothSegs - (innerCount - 1)
	toothPtCount = 1 + 4 * gear.toothSegs + midCount
	baseCount = gear.toothCount * toothPtCount
	loopCount = gear.toothCount * innerDiv

	toothPoints = getUnitToothPoints(int(1 / gear.precision))
	# rootRadius = gear.pitchRadius * get_distance(toothPoints[len(toothPoints)-1])
	rootRadius = gear.pitchRadius * length(toothPoints[-1])

	clampHoleRadius(rootRadius)

	###################################################
	# print(">>-->>", gear.pitchRadius, gear.toothCount, toothPoints, innerCount, vertList)
	addTeethPoints(gear.pitchRadius, gear.toothCount, toothPoints, innerCount, vertList)
	addNGonsPoints(gear.holeRadius, rootRadius, (gear.innerSegs-1), innerDiv, vertList)
	addSingleNGonPoints(loopCount, gear.holeRadius, vertList)
	
	makeOuterFlatFaces(baseCount, loopCount, midCount, toothPtCount, innerDiv, faceList)
	makeInnerFlatFaces((gear.innerSegs-2), baseCount, loopCount, (gear.toothCount * innerDiv), faceList)

	basePointCount = len(vertList)
	vertList += [Vector((vert.x, vert.y, gear.faceWidth)) for vert in vertList]
	faceList += [getReversedFace(face, basePointCount) for face in faceList]
	flatFaceCount = len(faceList)

	makeOuterLoopFaces(gear.toothCount, toothPtCount, midCount, basePointCount, faceList, vertList)
	makeInnerLoopFaces(basePointCount, loopCount, faceList, vertList)
	###################################################

	print(">V>",len(vertList))
	# print(">F>",faceList)
	print("-------------------------------------------------------------")
	return vertList, []#faceList

def create():
	faceWidth = 0
	# nodeTM.translation = gridPoint
	# holeRadius = gear.pitchRadius = ((gridDist.x^2 + gridDist.y^2)^.5) / 5
	# faceWidth = gridDist.z
	buildMesh()

def get_gear_mesh(width, length, WSegs, LSegs):
	verts, edges, faces = [], [], []
	# verts.append((0, 0, 0))
	# faces.append((d, c, b, a))
	verts, faces = buildMesh()
	return verts, edges, faces

class Gear(Primitive_Geometry_Class):
	def __init__(self):
		self.classname = "Gear"
		self.finishon = 2

	def create(self, ctx):
		mesh = get_gear_mesh(0, 0, 1, 1)
		self.create_mesh(ctx, mesh, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname

	def update(self):
		pd = self.data.primitivedata
		mesh = get_gear_mesh(pd.width, pd.length, pd.wsegs, pd.lsegs)
		self.update_mesh(mesh)

	def abort(self):
		bpy.ops.object.delete(confirm=False)


class Create_OT_Gear(Draw_Primitive):
	bl_idname = "create.gear"
	bl_label = "Gear"
	subclass = Gear()
	use_gride = True

	def create(self, ctx):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = self.gride.location
		self.subclass.owner.rotation_euler = self.gride.rotation

	def update(self, ctx, clickcount, dimension):
		if clickcount == 1:
			if self.ctrl:
				self.params.radius1 = dimension.radius
				self.params.radius2 = dimension.radius * 0.6
				self.params.height = dimension.radius*2
			else:
				self.params.radius1 = dimension.radius
				self.params.radius2 = self.params.radius1 * 0.9
		
		elif clickcount == 2:
			if self.use_single_draw:
				self.jump_to_end()
				return
			self.params.radius2 = dimension.distance
		
		elif clickcount == 3:
			self.params.height = dimension.height

def register_gear():
	bpy.utils.register_class(Create_OT_Gear)

def unregister_gear():
	bpy.utils.unregister_class(Create_OT_Gear)

if __name__ == "__main__":
	register_gear()
	obj = Gear()
	
	on_open()
	spnModule_update(1)

	obj.create(bpy.context)
	bpy.ops.primitive.cleardata()