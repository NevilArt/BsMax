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

from math import sin, cos, pi, radians
from primitive.primitive import Primitive_Geometry_Class, Draw_Primitive


def get_torus_mesh(
		radius1, radius2, rotation, twist, 
		segments, sides, sliceon, sfrom, sto ):

	verts,edges,faces,segs = [],[],[],[]
	rotation, twist = radians(rotation), radians(twist)
	sfrom, sto = radians(sfrom), radians(sto)
	arcrange, slicestep = pi*2, 0
	r1, r2 = radius1, radius2
	
	if sliceon:
		arcrange, slicestep = sto-sfrom, 1
	# collect segments x y onece
	for i in range(segments + slicestep):
		d = ((arcrange / segments) * i) + sfrom
		segs.append([sin(d), cos(d)])

	# add one more step if sclise is on
	segments += slicestep

	# Create vertexes data
	step = (pi * 2) / sides
	tw = twist / (segments - slicestep)
	for i in range(len(segs)):
		x, y = segs[i]
		for j in range(sides):
			d = j * step + i * tw + rotation
			X = (r1 + r2 * cos(d)) * x 
			Y = (r1 + r2 * cos(d)) * y
			Z = r2 * sin(d)
			verts.append([X, Y, Z])

	# create face data
	for i in range(segments - 1):
		for j in range(sides):
			a = j + i * sides
			if j < sides - 1:
				b = a + 1
				c = j + (i + 1) * sides + 1
				d = c - 1
			else:
				b = i * sides
				c = a + 1
				d = j + (i + 1) * sides
			faces.append((a, b, c, d))

	# apply slice for create cap or conncet end to start
	if sliceon:
		c1, c2 = [], []
		l = segments * sides - sides
		for i in range(sides):
			c1.append(sides - i - 1)
			c2.append(l + i)

		faces += [c1, c2]	

	else:
		for i in range(sides):
			a = i
			if i < sides - 1:
				b = a + 1
				c = i + sides * (segments - 1) + 1
				d = c - 1
			else:
				b = 0
				c = sides * (segments - 1)
				d = sides * segments - 1

			faces.append((d, c, b, a))

	return verts, edges, faces


class Torus(Primitive_Geometry_Class):
	def init(self):
		self.classname = "Torus"
		self.finishon = 3
		self.shading = 'SMOOTH'

	def create(self, ctx):
		mesh = get_torus_mesh(0, 0, 0, 0, 24, 12, False, 0, 360)
		self.create_mesh(ctx, mesh, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.ssegs, pd.ssegs_b = 24, 12

	def update(self):
		pd = self.data.primitivedata
		mesh = get_torus_mesh(
			pd.radius1, pd.radius2, pd.rotation, pd.twist, 
			pd.ssegs, pd.ssegs_b, pd.sliceon, pd.sfrom, pd.sto
		)

		self.update_mesh(mesh)


class Create_OT_Torus(Draw_Primitive):
	bl_idname = "create.torus"
	bl_label = "Torus"
	subclass = Torus()

	def create(self, ctx):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = self.gride.location
		self.subclass.owner.rotation_euler = self.gride.rotation

	def update(self, ctx, clickcount, dimension):
		if clickcount == 1:
			if self.ctrl:
				self.params.radius1 = dimension.radius
				self.params.radius2 = dimension.radius * 0.3
			else:
				self.params.radius1 = dimension.radius
				self.params.radius2 = dimension.radius * 0.1

		elif clickcount == 2:
			if self.use_single_draw:
				self.jump_to_end()
				return

			self.params.radius2 = dimension.radius


def register_torus():
	bpy.utils.register_class(Create_OT_Torus)


def unregister_torus():
	bpy.utils.unregister_class(Create_OT_Torus)


if __name__ == "__main__":
	register_torus()