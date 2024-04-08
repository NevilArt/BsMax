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
from math import pi, sin, cos, radians
from primitive.primitive import Primitive_Geometry_Class, Draw_Primitive

def get_sphere_mesh(
		radius, ssegs, hsegs, hemisphere,
		chop, sliceon, sfrom, sto, base ):

	verts, edges, faces = [], [], []
	sides = []

	ssegs = 3 if ssegs < 3 else ssegs
	hsegs = 3 if hsegs < 3 else hsegs

	arcrange, slicestep, r = pi*2, 0, radius
	if sliceon:
		arcrange, slicestep = radians(sto - sfrom), 1

	# collect segments x y onece
	for i in range(ssegs + slicestep):
		d = (arcrange / ssegs) * i + radians(sfrom)
		sides.append([sin(d), cos(d)])

	# heaight
	heaights = []
	starth, endh = -radius, radius
	startd, endd = 0, pi - hemisphere * pi
	hstep = (endh - starth) / hsegs
	dstep = (endd - startd) / hsegs
	if hemisphere > 0:
		hsegs += 1
	for i in range(1, hsegs):
		h = cos(startd + dstep * i) * radius + radius
		s = sin(startd + dstep * i)
		heaights.append([h, s])

	# add one more step if sclise is on
	ssegs += slicestep

	# Create vertexes data
	# step = (pi*2) / ssegs

	# height offset
	hoffset = 0
	if base:
		if hemisphere == 0:
			hoffset = radius
		else:
			hoffset = radius - heaights[-1][0]

	# first vertex
	verts.append([0,0,radius + hoffset])

	# Body part
	for h, s in heaights:
		for x, y in sides:
			X = r * x * s
			Y = r * y * s
			Z = starth + h + hoffset
			verts.append([X, Y, Z])
	
	# last vertex
	if base:
		verts.append([0,0,0])
	elif hemisphere > 0:
		H = starth + heaights[-1][0] + hoffset
		verts.append([0,0,H])
	else:
		verts.append([0,0,-radius])

	# upper cap
	for i in range(ssegs):
		a = i + 1
		b = a + 1
		if i < ssegs - 1:
			faces.append((0, b, a))
		elif not sliceon:
			a = ssegs
			faces.append((0, 1, a))
	# body
	for i in range(hsegs - 2):
		f = i * ssegs + 1
		for j in range(ssegs):
			a = f + j
			b = a + 1
			c = b + ssegs
			d = c - 1
			if j < ssegs - 1:
				faces.append((a, b, c, d))
			elif not sliceon:
				b = f
				c = b + ssegs
				faces.append((a, b, c, d))

	# lower cap
	f = ssegs * (hsegs - 2) + 1
	l = len(verts) - 1
	for i in range(ssegs):
		a = f + i
		b = a + 1
		if i < ssegs - 1:
			faces.append((a, b, l))
		elif not sliceon:
			faces.append((a, f, l))

	# side plates
	if sliceon:
		cap1, cap2 = [], [0]
		for i in range(hsegs):
			cap1.append(ssegs * i)
			cap2.append(i * ssegs + 1 )
		cap1.append(l)
		cap1.reverse()
		faces.append(cap1)
		faces.append(cap2)

	return verts, edges, faces


class Sphere(Primitive_Geometry_Class):
	def init(self):
		self.classname = "Sphere"
		self.finishon = 2
		self.shading = 'SMOOTH'

	def create(self, ctx):
		mesh = get_sphere_mesh(0, 32, 32, 0, False, False, 0, 360, False)
		self.create_mesh(ctx, mesh, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.ssegs, pd.hsegs, pd.seglock = 32, 30, True

	def update(self):
		pd = self.data.primitivedata
		hsegs = pd.hsegs if not pd.seglock else pd.ssegs - 2
		#radius, ssegs, hsegs, hemisphere, chop, sliceon, sfrom, sto, base
		mesh = get_sphere_mesh(
			pd.radius1, pd.ssegs, hsegs,
			pd.bias, False, #hemisphere, chop
			pd.sliceon, pd.sfrom, pd.sto,
			pd.base
		)
		
		self.update_mesh(mesh)


class Create_OT_Sphere(Draw_Primitive):
	bl_idname = "create.sphere"
	bl_label = "Sphere"
	subclass = Sphere()
	use_gride = True

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


def register_sphere():
	bpy.utils.register_class(Create_OT_Sphere)


def unregister_sphere():	
	bpy.utils.unregister_class(Create_OT_Sphere)


if __name__ == "__main__":
	register_sphere()