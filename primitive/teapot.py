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
# 2024/04/04

import bpy

from mathutils import Vector
from math import sin, cos, pi

from bsmax.curve import Spline, Bezier_point
from bsmax.math import point_on_cubic_bezier_curve
from primitive.primitive import Primitive_Geometry_Class, Draw_Primitive


def get_path(part):
	body_path = Spline(None)
	points = []
	if part == 'body':
		points = (
			((0, 0, 0), (0, 0, 0), (0.358946, 0, 0.00480962)),
			((0.774773, 0, -0.000830472), (0.75, 0, 0.075), (0.791808, 0, 0.150003)),
			((0.978876, 0, 0.20208), (1, 0, 0.45), (1.02112, 0, 0.69792)),
			((0.805268, 0, 1.06392), (0.750701, 0, 1.2012), (0.695276, 0, 1.29381)),
			((0.676157, 0, 1.2304), (0.7, 0, 1.2), (0.7, 0, 1.2))
		)

	elif part == 'lid':
		points = (
			((0, 0, 1.575), (0, 0, 1.575), (0.400656, 0, 1.56443)),
			((0.00236605, 0, 1.43537), (0.1 ,0 ,1.35), (0.211611, 0, 1.27556)),
			((0.657876, 0, 1.26831), (0.65, 0, 1.2), (0.65, 0, 1.2))
		)

	elif part == 'spout_a':
		points = (
			((0.85, 0, 0.7125), (0.85, 0, 0.7125), (1.30583, 0, 0.724497)),
			((1.15645, 0, 1.0605), (1.35, 0, 1.2), (1.39425, 0, 1.23295)),
			((1.45212, 0, 1.24122), (1.4, 0, 1.2), (1.4, 0, 1.2))
		)

	elif part == 'spout_b':
		points = (
			((0.848828, 0, 0.3), (0.848828, 0, 0.3), (1.5298, 0, 0.39321)),
			((1.22074, 0, 1.03193), (1.65, 0, 1.2), (1.70914, 0, 1.22046)),
			((1.78246, 0, 1.27581), (1.6, 0, 1.2), (1.6, 0, 1.2))
		)

	elif part == 'spout_s':
		points = (
			((0, 0.2475, 0), (0, 0.2475, 0), (0, 0.24786, 0)),
			((0, 0.0876482, 0), (0, 0.09375, 0), (0, 0.0926101, 0)),
			((0, 0.0610992, 0), (0, 0.05625, 0), (0, 0.05625, 0))
		)

	elif part == 'handle_a':
		points = (
			((-0.75, 0, 1.125), (-0.75, 0, 1.125), (-0.999939, 0, 1.12514)),
			((-1.51932, 0, 1.16786), (-1.5, 0, 0.9), (-1.47991, 0, 0.621563)),
			((-1.2955, 0, 0.456572), (-0.95, 0, 0.3), (-0.95, 0, 0.3))
		)

	elif part == 'handle_b':
		points = (
			((-0.8, 0, 1.0125), (-0.8, 0, 1.0125), (-1.01763, 0, 0.999294)),
			((-1.34732, 0, 1.04424), (-1.35, 0, 0.9), (-1.35272, 0, 0.753523)),
			((-1.19108, 0, 0.528823), (-1, 0, 0.45), (-1, 0, 0.45))
		)

	elif part == 'handle_s':
		points = (
			((0, 0.112449, 0), (0, 0.112449, 0), (0, 0.112449, 0)),
			((0, 0.112449, 0), (0, 0.112449, 0), (0, 0.112449, 0)),
			((0, 0.112449, 0), (0, 0.112449, 0), (0, 0.112449, 0))
		)

	for p in points:
		newbp = Bezier_point(None)
		newbp.handle_left = Vector((p[0]))
		newbp.co = Vector((p[1]))
		newbp.handle_right = Vector((p[2]))
		body_path.bezier_points.append(newbp)

	return body_path


def get_ring(point1, point2, scale):
	ring = Spline(None)
	d = Vector((0,scale*1.25,0))
	p1 = Bezier_point(None)
	p2 = Bezier_point(None)
	p1.handle_left = point1+d
	p1.co = point1
	p1.handle_right = point1-d
	ring.bezier_points.append(p1)
	p2.handle_left = point2-d
	p2.co = point2
	p2.handle_right = point2+d
	ring.bezier_points.append(p2)
	ring.use_cyclic_u = True

	return ring


def get_verts_body(spline, ssegs, scale):
	verts = []
	for index in range(len(spline.bezier_points)):
		a, b, c, d = spline.get_segment(index)
		for j in range(ssegs):
			t = (1/ssegs)*j
			newvert = point_on_cubic_bezier_curve(a, b, c, d, t)
			verts.append(newvert*scale)

	return verts


def get_verts_pipe(spline, ssegs, scale):
	verts = []
	if spline.use_cyclic_u:
		for index in range(len(spline.bezier_points)):
			a, b, c, d = spline.get_segment(index)
			for j in range(ssegs):
				t = (1/ssegs)*j
				newvert = point_on_cubic_bezier_curve(a,b,c,d,t)
				verts.append(newvert*scale)

	else:
		for index in range(len(spline.bezier_points)-1):
			a, b, c, d = spline.get_segment(index)
			for j in range(ssegs):
				t = (1/ssegs)*j
				newvert = point_on_cubic_bezier_curve(a,b,c,d,t)
				verts.append(newvert*scale)

			if index == len(spline.bezier_points)-2:
				verts.append(d*scale)

	return verts


def get_teapot_mesh(radius, csegs, body, handle, spout, lid):
	verts, edges, faces = [], [], []
	cs = csegs*4
	step = (pi*2)/cs

	def create_body(line, flip):
		f = len(verts) # First vertex of element

		""" Create vertexes """
		path = get_path(line)
		sides = get_verts_body(path, csegs, radius)
		l = len(sides)-1
		verts.append(sides[0])

		for i in range(1,l):
			x = sides[i].x
			for j in range(cs):
				d = j*step
				X = sin(d)*x 
				Y = cos(d)*x
				Z = sides[i].z
				verts.append([X,Y,Z])

		""" first triangle faces """
		for i in range(cs):
			newface = (f,f+i,f+i+1) if flip else (f+i+1,f+i,f)
			faces.append(newface)

		newface = (f,f+cs,f+1) if flip else (f+1,f+cs,f)
		faces.append(newface)
				
		faces.append((0,cs,1))
		""" faces """
		f += 1 # First vertex of element
		for i in range(l-2):
			for j in range(cs):
				a = f+j+(i*cs)
				if j < cs-1:
					b = a+1
					c = a+cs+1
					d = c-1

				else: 
					b = f+i*cs
					c = a+1
					d = a+cs

				newface = (d,c,b,a) if flip else (a,b,c,d)
				faces.append(newface)

	def create_pipe(line1, line2, line3,flip):
		f = len(verts)
		""" create vertexes """
		spline1 = get_path(line1)
		spline2 = get_path(line2)
		spline3 = get_path(line3)

		v1 = get_verts_pipe(spline1, csegs, radius)
		v2 = get_verts_pipe(spline2, csegs, radius)
		v3 = get_verts_pipe(spline3, csegs, radius)

		for p1,p2,p3 in zip(v1,v2,v3):
			ring = get_ring(p1,p2,p3.y)
			vert = get_verts_pipe(ring,csegs,1)
			for v in vert:
				verts.append(v)

		""" faces """
		ssegs = csegs*2
		for i in range(len(v1)-1):
			for j in range(ssegs):
				a = f+i*ssegs+j
				if j < ssegs-1:
					b = a+1
					c = a+ssegs+1
					d = c-1

				else:
					b = f+i*ssegs
					c = b+ssegs
					d = a+ssegs

				newface = (d, c, b, a) if flip else (a, b, c, d)
				faces.append(newface)

	if body:
		create_body('body', True)

	if lid:
		create_body('lid', False)

	if handle:
		create_pipe("handle_a", "handle_b", "handle_s", True)

	if spout:
		create_pipe("spout_a", "spout_b", "spout_s", False)

	return verts, edges, faces


class Teapot(Primitive_Geometry_Class):
	def init(self):
		self.classname = "Teapot"
		self.finishon = 2
		self.shading = 'SMOOTH'

	def create(self, ctx):
		mesh = get_teapot_mesh(0, 4, True, True, True, True)
		self.create_mesh(ctx, mesh, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.csegs = 4
		pd.bool1, pd.bool2, pd.bool3, pd.bool4 = True, True, True, True

	def update(self):
		pd = self.data.primitivedata
		mesh = get_teapot_mesh(pd.radius1, pd.csegs, 
			pd.bool1, pd.bool2, pd.bool3, pd.bool4)
		self.update_mesh(mesh)


class Create_OT_Teapot(Draw_Primitive):
	bl_idname = "create.teapot"
	bl_label = "Teapot"
	subclass = Teapot()

	def create(self, ctx):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = self.gride.location
		self.subclass.owner.rotation_euler = self.gride.rotation

	def update(self, ctx, clickcount, dimension):
		if clickcount == 1:
			self.params.radius1 = dimension.radius

		if clickcount > 0:
			self.subclass.update()


def register_teapot():
	bpy.utils.register_class(Create_OT_Teapot)


def unregister_teapot():
	bpy.utils.unregister_class(Create_OT_Teapot)


if __name__ == "__main__":
	register_teapot()