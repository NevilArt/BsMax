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

from primitive.primitive import Primitive_Geometry_Class, Draw_Primitive


def get_pyramid_mesh(width, depth, height, wsegs, dsegs, hsegs):
	verts, edges, faces = [], [], []
	w, d, h = width / 2.0, depth / 2.0, height
	ws, ds, hs = width / wsegs, depth / dsegs, height / hsegs
	wc, dc, hc = w / hsegs, d / hsegs, h / hsegs
	# get floor vertexes
	for i in range(wsegs + 1):
		for j in range(dsegs + 1):
			x = -w + i * ws
			y = -d + j * ds
			verts.append((x, y, 0))

	# get side vertexes x
	for i in range(1, hsegs):
		s = (((hsegs - i) * hc) / h)
		for j in range(dsegs):
			x = (-w + i * wc)
			y = (-d + j * ds) * s
			z = i * hs
			verts.append((x, y, z))

		for j in range(wsegs):
			x = (-w + j * ws) * s
			y = (-d + i * dc) * -1
			z = i * hs
			verts.append((x, y, z))

		for j in range(dsegs):
			x = (-w + i * wc) * -1
			y = (-d + (dsegs - j) * ds) * s
			z = i * hs
			verts.append((x, y, z))

		for j in range(wsegs):
			x = (-w + (wsegs - j) * ws) * s
			y = (-d + i * dc)
			z = i * hs
			verts.append((x, y, z))
	# add top vertex
	verts.append((0, 0, h))

	# get floor faces
	for i in range(wsegs):
		for j in range(dsegs):
			r = i * (dsegs + 1)
			a = r + j
			b = a + 1
			c = b + dsegs + 1
			d = c - 1
			faces.append((a, b, c, d))

	f = (wsegs + 1) * (dsegs + 1)
	l = (wsegs + dsegs) * 2
	for i in range(hsegs - 2):
		for j in range(l):
			a = f + i * l + j
			if j < l - 1:
				b = a + 1
				c = b + l
				d = c - 1
			else:
				b = f + i * l
				c = f + (i + 1) * l
				d = a + l
			faces.append((d, c, b, a))

	v = len(verts) - 1 # last vertex index
	f2 = f + l * (hsegs - 2) # last line first vertext

	if hsegs > 1:
		# top
		for i in range(l):
			a = f2 + i
			if i < l - 1:
				b = a + 1
			else:
				b = f2
			c = v
			faces.append((c, b, a))

		# silde lowr line 1
		for i in range(dsegs):
			a = i
			b = a + 1
			c = f + i + 1
			d = f + i
			faces.append((d, c, b, a))

		# silde lowr line 2
		fl, fu = dsegs, f + dsegs
		for i in range(wsegs):
			a = fl + i * (dsegs + 1)
			b = a + dsegs + 1
			c = fu + i + 1
			d = fu + i
			faces.append((d, c, b, a))

		fl = (wsegs + 1) * (dsegs + 1) - 1
		fu = f + wsegs + dsegs
		for i in range(dsegs):
			a = fl - i
			b = a - 1
			c = fu + i + 1
			d = fu + i
			faces.append((d, c, b, a))

		fl = (dsegs + 1) * wsegs
		fu = (wsegs + 3) * (dsegs + 1) + (wsegs - 2)
		for i in range(wsegs):
			a = fl - i * (dsegs + 1)
			b = a - (dsegs + 1)
			if i < wsegs - 1:
				c = fu + i + 1
			else:
				c = f
			d = fu + i
			faces.append((d, c, b, a))

	else:
		for i in range(dsegs):
			a, b = i, i + 1
			faces.append((v, b, a))
		l = (dsegs + 1)

		for i in range(wsegs):
			a = (i + 1) * l - 1
			b = a + l
			faces.append((v, b, a))

		for i in range(dsegs):
			a = f - i - 1
			b = a - 1
			faces.append((v, b, a))

		f = l * wsegs
		for i in range(wsegs):
			a = f - l * i
			b = f - l * (i + 1)
			faces.append((v, b, a))

	return verts, edges, faces


class Pyramid(Primitive_Geometry_Class):
	def init(self):
		self.classname = "Pyramid"
		self.finishon = 3
		self.shading = 'FLAT'

	def create(self, ctx):
		mesh = get_pyramid_mesh(0, 0, 0, 1, 1, 1)
		self.create_mesh(ctx, mesh, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.wsegs, pd.lsegs, pd.hsegs = 1, 1, 1

	def update(self):
		pd = self.data.primitivedata
		mesh = get_pyramid_mesh(
			pd.width, pd.length, pd.height,
			pd.wsegs, pd.lsegs, pd.hsegs
		)

		self.update_mesh(mesh)


class Create_OT_Pyramid(Draw_Primitive):
	bl_idname = "create.pyramid"
	bl_label = "Pyramid (Create)"
	subclass = Pyramid()
	use_gride = True

	def create(self, ctx):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = self.gride.location
		self.subclass.owner.rotation_euler = self.gride.rotation

	def update(self, ctx, clickcount, dimension):
		if clickcount == 1:
			if self.ctrl:
				self.params.width = dimension.radius
				self.params.length = dimension.radius
				self.params.height = dimension.radius*0.6

			else:
				self.params.width = abs(dimension.width)
				self.params.length = abs(dimension.length)
				self.subclass.owner.location = dimension.center
		
		elif clickcount == 2:
			if self.use_single_draw:
				self.jump_to_end()
				return

			self.params.height = dimension.height


def register_pyramid():
	bpy.utils.register_class(Create_OT_Pyramid)


def unregister_pyramid():
	bpy.utils.unregister_class(Create_OT_Pyramid)


if __name__ == '__main__':
	register_pyramid()