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
# 2024/04/20

import bpy

from mathutils import Vector
from math import pi, sin, cos, radians
from bpy.utils import register_class, unregister_class

from primitive.primitive import Primitive_Geometry_Class, Draw_Primitive


def get_cylinder_mesh(
		radius1, radius2, height,hsegs, csegs, ssegs, sliceon, sfrom, sto
	):
	
	verts, edges, faces = [], [], []
	sides, heights = [], []
	sfrom, sto = radians(sfrom), radians(sto)
	arcrange, slicestep, r1, r2 = pi*2, 0, radius1, radius2
	# height
	if sliceon:
		arcrange,slicestep = sto - sfrom, 1

	# collect segments x y onece
	for i in range(ssegs + slicestep):
		d = ((arcrange / ssegs) * i) + sfrom
		sides.append([sin(d), cos(d)])
	# collect cap arc height and scale
	for i in range(1,csegs):
		heights.append(cos(((pi/2)/csegs)*i))
	heights.reverse()

	# add one more step if sclise is on
	ssegs += slicestep
	# Create vertexes data
	# step = (pi*2)/ssegs
	# first vertex
	if csegs > 1 or sliceon:
		verts.append([0,0,0])
	# lover part
	for i in range(csegs):
		s = (r1/csegs)*(i+1)
		for x, y in sides:
			verts.append([s*x,s*y,0])
	# Cylinder part
	h = height/hsegs
	rs = (r2-r1)/hsegs
	for i in range(1, hsegs):
		Z = h*i
		r = r1+rs*i
		for x, y in sides:
			verts.append([r*x, r*y, Z])
		if sliceon:
			for j in range(1, csegs):
				s = (r/csegs)*(csegs - j)
				# X = s*x
				# Y = s*y
			verts.append([0,0,Z]) # the center point
			# for j in range(1, csegs):
			# 	s = (r/csegs)*j
			# 	x, y = sides[0]
			# 	X = s*x
			# 	Y = s*y
	# uppaer part
	for i in range(csegs):
		s = (r2/csegs)*(csegs - i)
		for x, y in sides:
			verts.append([s*x, s*y, height])
	# last vertex
	if csegs > 1 or sliceon:
		verts.append([0,0,height])

	# Create Cap Faces
	if csegs == 1:
		cap = []
		if sliceon:
			for i in range(ssegs + 1):
				cap.append(i)
		else:
			for i in range(ssegs):
				cap.append(i)
		faces.append(cap)
	else:
		# First line
		for i in range(ssegs):
			faces.append([0,i, i + 1])
		if not sliceon:
			faces.append([0, ssegs, 1])

	# fill First cap
	for i in range(csegs - 1):
		s = ssegs * i
		if csegs > 1 or sliceon:
			s += 1
		for j in range(ssegs):
			a = s + j
			b = a + 1
			c = b + ssegs
			d = c - 1
			if j < ssegs - 1:
				faces.append((d, c, b, a))
			elif not sliceon:
				b = a - ssegs + 1
				c = d - ssegs + 1
				faces.append((d, c, b, a))
	# fill body
	f = (csegs - 1) * ssegs
	if csegs > 1 or sliceon:
		f += 1
	for i in range(hsegs):
		s = f + i * ssegs
		if sliceon and i > 0:
			s = f + i * (ssegs + 1) - 1
		for j in range(ssegs):
			a = s + j
			b = a + 1
			c = b + ssegs
			if sliceon and i > 0:
				c += 1
			d = c - 1
			if j < ssegs - 1:
				faces.append((d, c, b, a))
			elif not sliceon:
				b = a - ssegs + 1
				c = d - ssegs + 1
				faces.append((d, c, b, a))
	# fill upper cap
	# find firs vertex of upper cap
	f = hsegs * ssegs
	if csegs > 1:
		f += (csegs - 1) * ssegs + 1
	if sliceon:
		f += hsegs
		if csegs > 1:
			f -= 1
	# Create cap face
	if csegs == 1:
		cap = []
		if sliceon:
			for i in range(ssegs + 1):
				cap.append(f + i)
		else:
			for i in range(ssegs):
				cap.append(f + i)
		cap.reverse()
		faces.append(cap)

	for i in range(csegs - 1):
		s = f + ssegs * i
		for j in range(ssegs):
			a = s + j
			b = a + 1
			c = b + ssegs
			d = c - 1
			if j < ssegs - 1:
				faces.append((d, c, b, a))
			elif not sliceon:
				b = a - ssegs + 1
				c = d - ssegs + 1
				faces.append((d, c, b, a))
				
	# Fill last line
	if csegs > 1:
		l = len(verts) - 1
		f = l - ssegs
		for i in range(ssegs - 1):
			a = f + i
			b = a + 1
			faces.append([l, b, a])
		if not sliceon:
			faces.append([l, f, l - 1])

	# fill sliced face
	if sliceon:
		# Plate one
		cap = [0]
		for i in range(csegs + 1):
			cap.append(i * ssegs + 1)
		s = cap[-1]
		for i in range(1, hsegs):
			cap.append(s + i * (ssegs + 1))
		s = cap[-1]
		for i in range(1, csegs):
			cap.append(s + i * ssegs)
		cap.append(len(verts) - 1)
		s = csegs * ssegs + (hsegs - 1) * (ssegs + 1)
		for i in range(hsegs - 1):
			cap.append(s - i * (ssegs + 1))
		cap.reverse()
		faces.append(cap)
		# Plate two
		cap = [0]
		for i in range(csegs + 1):
			cap.append((i + 1) * ssegs)
		s = cap[-1]
		for i in range(1, hsegs):
			cap.append(s + i * (ssegs + 1))
		s = cap[-1]
		for i in range(1, csegs):
			cap.append(s + i * ssegs)
		cap.append(len(verts) - 1)
		s = csegs * ssegs + (hsegs - 1) * (ssegs + 1)
		for i in range(hsegs - 1):
			cap.append(s - i * (ssegs + 1))
		faces.append(cap)
	return verts, edges, faces


class Cylinder(Primitive_Geometry_Class):
	def init(self):
		self.classname = "Cylinder"
		self.finishon = 3
		self.shading = 'AUTO'
		self.owner = None
		self.data = None

	def create(self, ctx):
		mesh = get_cylinder_mesh(0, 0, 0, 1, 1, 18, False, 0, 360)
		self.create_mesh(ctx, mesh, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.hsegs, pd.csegs, pd.ssegs = 1, 1, 18

	def update(self):
		pd = self.data.primitivedata
		radius = pd.radius1
		mesh = get_cylinder_mesh(
			radius, radius, pd.height, 
			pd.hsegs, pd.csegs, pd.ssegs,
			pd.sliceon, pd.sfrom, pd.sto
		)

		self.update_mesh(mesh)

	def abort(self):
		bpy.ops.object.delete(confirm=False)


class Cone(Primitive_Geometry_Class):
	def init(self):
		self.classname = "Cone"
		self.finishon = 4
		self.shading = 'AUTO'

	def create(self, ctx):
		mesh = get_cylinder_mesh(0, 0, 0, 1, 1, 18, False, 0, 360)
		self.create_mesh(ctx, mesh, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.hsegs, pd.csegs, pd.ssegs = 1, 1, 18

	def update(self):
		pd = self.data.primitivedata
		mesh = get_cylinder_mesh(
			pd.radius1, pd.radius2, pd.height,
			pd.hsegs, pd.csegs, pd.ssegs,
			pd.sliceon, pd.sfrom, pd.sto
		)

		self.update_mesh(mesh)


class Create_OT_Cylinder(Draw_Primitive):
	bl_idname = "create.cylinder"
	bl_label = "Cylinder"
	subclass = Cylinder()
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
				self.params.height = dimension.radius*2
			else:
				self.params.radius1 = dimension.radius

		elif clickcount == 2:
			if self.use_single_draw:
				self.jump_to_end()
				return
			
			self.params.height = dimension.height


class Create_OT_Cone(Draw_Primitive):
	bl_idname = "create.cone"
	bl_label = "Cone"
	subclass = Cone()
	use_gride = True
	gride_updated = False

	def create(self, ctx):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = self.gride.location
		self.subclass.owner.rotation_euler = self.gride.rotation

	def update(self, ctx, clickcount, dimension):
		if clickcount == 1:
			if self.ctrl:
				self.params.radius1 = dimension.radius
				self.params.radius2 = dimension.radius/2
				self.params.height = dimension.radius
			else:
				self.params.radius1 = dimension.radius
				self.params.radius2 = dimension.radius
		
		elif clickcount == 2:
			if self.use_single_draw:
				self.jump_to_end()
				return
			
			self.params.height = dimension.height
			
		elif clickcount == 3:
			if not self.gride_updated:
				center = self.gride.gride_matrix @ Vector((0,0,self.params.height))
				self.gride.location = center
				self.gride.update()
				self.gride_updated = True

			self.params.radius2 = dimension.distance

	def finish(self):
		self.gride_updated = False


classes = (
	Create_OT_Cylinder,
	Create_OT_Cone
)


def register_cylinder():
	for c in classes:
		register_class(c)


def unregister_cylinder():
	for c in classes:
		unregister_class(c)


if __name__ == "__main__":
	register_cylinder()