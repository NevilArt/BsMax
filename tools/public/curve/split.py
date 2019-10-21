import bpy, numpy, copy, math
from mathutils import Vector
from bpy.types import Operator
from bsmax.math import *

class Knot:
	in_type = ""
	invec = Vector((0,0,0))
	co = Vector((0,0,0))
	out_type = ""
	outvec = Vector((0,0,0))

def point_on_vector(a, b, c, d, t):
	C1 = d - (3.0 * c) + (3.0 * b) - a
	C2 = (3.0 * c) - (6.0 * b) + (3.0 * a)
	C3 = (3.0 * b) - (3.0 * a)
	C4 = a
	return C1 * t * t * t + C2 * t * t + C3 * t + C4
	
def segment_length1(a, b, c, d):
	x = math.sqrt(a.x**4 + b.x**3 + c.x**2 + d.x)
	y = math.sqrt(a.y**4 + b.y**3 + c.y**2 + d.y)
	z = math.sqrt(a.z**4 + b.z**3 + c.z**2 + d.z)
	return math.sqrt(x**2 + y**2 + z**2)

def distance(a, b):
	x,y,z = a.x - b.x, a.y - b.y, a.z - b.z
	return math.sqrt(x**2 + y**2 + z**2)

def segment_length(a, b, c, d, steps):
	points = [a]
	s = 1 / steps
	for i in range(1, steps + 1):
		t = i * s
		p = point_on_vector(a, b, c, d, t)
		points.append(p)
	lenght = 0
	for i in range(len(points) - 1):
		lenght += distance(points[i], points[i - 1])
	return lenght

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

class BsMax_OT_SplitCurve(Operator):
	bl_idname = "bsmax.splitcurve"
	bl_label = "Split(Curve)"
	def execute(self, ctx):
		# get original data
		obj = ctx.active_object
		splines = obj.data.splines
		points = splines[0].bezier_points
		knots = []
		for point in points:
			newknot = Knot()
			newknot.in_type = point.handle_left_type
			newknot.out_type = point.handle_right_type
			
			newknot.invec = Vector(point.handle_left)
			newknot.co = Vector(point.co)
			newknot.outvec = Vector(point.handle_right)
			knots.append(newknot)
		# calc new date
		p1 = knots[0].co
		p2 = knots[0].outvec
		p3 = knots[1].invec
		p4 = knots[1].co
		t = 0.5
		ns = split_segment(p1, p2, p3, p4, t)
		k1, k2, k3 = Knot(), Knot(), Knot()

		k1.in_type = knots[0].in_type
		k1.invec = knots[0].invec
		k1.co = knots[0].co
		k1.out_type = 'ALIGNED'
		k1.outvec = ns[1]

		k2.in_type = 'ALIGNED'
		k2.invec = ns[2]
		k2.co = ns[3]
		k2.out_type = 'ALIGNED'
		k2.outvec = ns[4]

		k3.in_type = 'ALIGNED'
		k3.invec = ns[5]
		k3.co = knots[1].co
		k3.out_type = knots[1].out_type
		k3.outvec = knots[1].outvec

		# set new data
		# obj.data.splines.clear()
		# newknots = (k1, k2, k3)
		# for spline in newknots:
		# 	spline = obj.data.splines.new('BEZIER')
		# 	spline.bezier_points.add(len(newknots) - 1)
		# 	for i in range(len(newknots)):
		# 		spline.bezier_points[i].handle_left_type = newknots[i].in_type
		# 		spline.bezier_points[i].handle_left = newknots[i].invec
		# 		spline.bezier_points[i].co = newknots[i].co
		# 		spline.bezier_points[i].handle_right_type = newknots[i].out_type
		# 		spline.bezier_points[i].handle_right = newknots[i].outvec

		location = point_on_vector(p1, p2, p3, p4, 0.1)
		bpy.context.scene.objects['Empty'].location = location
		#lenght = segment_length(p1, p2, p3, p4)
		lenght = segment_length(p1, p2, p3, p4, 30)
		print(lenght)
		return{"FINISHED"}

def split_cls(register):
	c = BsMax_OT_SplitCurve
	if register: bpy.utils.register_class(c)
	else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	split_cls(True)

__all__ = ["split_cls"]