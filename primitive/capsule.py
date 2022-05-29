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

import bpy
from math import pi, sin, cos, radians
from primitive.primitive import Primitive_Geometry_Class, Draw_Primitive
from bsmax.actions import delete_objects



def get_capsule_mesh(radius, height, ssegs, csegs, hsegs, sliceon, sfrom, sto):
	verts, edges, faces = [], [], []
	sides, heights = [], []
	arcrange, slicestep, r = pi*2, 0, radius
	# height
	if sliceon:
		arcrange, slicestep = radians(sto - sfrom), 1

	# collect segments x y onece
	for i in range(ssegs + slicestep):
		d = (arcrange / ssegs) * i + radians(sfrom)
		sides.append([sin(d), cos(d)])

	# collect cap arc height and scale
	for i in range(csegs):
		d = ((pi/2) / csegs) * i
		s = cos(d)
		h = sin(d)
		heights.append([h, s])
	heights.reverse()

	# add one more step if sclise is on
	ssegs += slicestep
	# Create vertexes data
	step = (pi*2) / ssegs

	# first vertex
	verts.append([0,0,0])
	# lower part
	for h, s in heights:
		for x, y in sides:
			X = r * x * s
			Y = r * y * s
			Z = radius - r * h
			verts.append([X, Y, Z])
		if sliceon:
			verts.append([0, 0, Z])

	# Cylinder part
	h = height / hsegs
	for i in range(1, hsegs):
		for x, y in sides:
			X = r * x
			Y = r * y
			Z = radius + h * i
			verts.append([X, Y, Z])
		if sliceon:
				verts.append([0, 0, Z])

	# uppaer part
	heights.reverse()
	for h, s in heights:
		for x, y in sides:
			X = r * x * s
			Y = r * y * s
			Z = radius + r * h + height
			verts.append([X, Y, Z])
		if sliceon:
			verts.append([0, 0, Z])
	# add last vertex
	verts.append([0,0,radius * 2 + height])

	# uper triangles faces
	if sliceon:
		ssegs += 1
	for i in range(ssegs):
		a = i + 1
		b = i + 2
		c = 0
		if i < ssegs - 1:
			faces.append((a, b, c))
		else:
			faces.append((a, 1, c))

	# body faces
	for i in range(csegs * 2 + hsegs - 2):
		for j in range(ssegs):
			a = i * ssegs + j + 1
			if j < ssegs - 1:
				b = a + 1
				c = a + ssegs + 1
				d = c - 1
			else:
				b = a - (ssegs - 1)
				c = a + 1
				d = a + ssegs
			faces.append((d, c, b, a))

	# lover triangels
	f = ssegs * (((csegs - 1) * 2) + hsegs) + 1
	c = len(verts) - 1
	for i in range(ssegs):
		a = i + f
		b = a + 1 
		if i < ssegs - 1:
			faces.append((c, b, a))
		else:
			faces.append((c, f, a))
	return verts, edges, faces



class Capsule(Primitive_Geometry_Class):
	def init(self):
		self.classname = "Capsule"
		self.finishon = 3

	def create(self, ctx):
		mesh = get_capsule_mesh(0, 0, 18, 8, 6, False, 0, 360)
		self.create_mesh(ctx, mesh, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.ssegs, pd.csegs, pd.hsegs = 18, 8, 3
		pd.center = True

	def update(self):
		pd = self.data.primitivedata
		csegs = pd.csegs if not pd.seglock else pd.ssegs - 2
		if pd.center:
			height = pd.height
		else:
			diameter = pd.radius1 * 2
			if pd.height < diameter:
				pd.height = diameter
			height = pd.height - pd.radius1 * 2
		mesh = get_capsule_mesh(pd.radius1, height,
			pd.ssegs, csegs, pd.hsegs,
			pd.sliceon, pd.sfrom, pd.sto)
		self.update_mesh(mesh)

	def abort(self):
		delete_objects([self.owner])



class Create_OT_Capsule(Draw_Primitive):
	bl_idname = "create.capsule"
	bl_label = "Capsule"
	subclass = Capsule()
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
				self.params.height = dimension.radius
			else:
				self.params.radius1 = dimension.radius

		elif clickcount == 2:
			if self.use_single_draw:
				self.jump_to_end()
				return
			self.params.height = dimension.height



def register_capsule():
	bpy.utils.register_class(Create_OT_Capsule)
	
def unregister_capsule():
	bpy.utils.unregister_class(Create_OT_Capsule)

if __name__ == "__main__":
	register_capsule()