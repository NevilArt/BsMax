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



def get_tube_mesh(radius1, radius2, height, hsegs, csegs, ssegs, sliceon, sfrom, sto):
	Sides = []
	r1, r2 = radius1, radius2
	sfrom, sto = radians(sfrom), radians(sto)
	if radius1 > radius2:
		r2, r1 = radius1, radius2
	Range, slicestep = pi*2, 0

	if sliceon:
		Range = sto - sfrom
		slicestep = 1

	for i in range(ssegs + slicestep):
		d = ((Range/ssegs)*i)+sfrom
		Sides.append([sin(d), cos(d)])
	ssegs += slicestep

	verts,edges,faces = [],[],[]
	# Create inner and outer vertex
	for r in (r1, r2):
		for i in range(hsegs+1):
			for x, y in Sides:
				verts.append((r*x,r*y,i*(height/hsegs)))

	# Create cap vertexes
	for h in (0, height):
		for i in range(1, csegs):
			r = r1+(((r2-r1)/csegs)*i)
			for x ,y in Sides:
				verts.append((r*x, r*y, h))

	# create side vertexes
	if sliceon:
		for x, y in (Sides[0], Sides[-1]):
			for i in range(1, csegs):
				r = r1 + (((r2 - r1) / csegs) * i)
				for i in range(1, hsegs):
					verts.append((r*x, r*y, i*(height/hsegs)))

	c1,c1e = 0, ssegs*(hsegs+1) - 1 # Cylinder 1 (inner) start and end
	c2,c2e = c1e+1, c1e+ssegs*(hsegs+1) # Cylinder 2 (outter)
	p1,p1e = c2e+1, c2e+ssegs*(csegs - 1) # cap segments upper
	p2,p2e = p1e+1, p1e+ssegs*(csegs - 1) # cap segments lower
	f1,f1e = p2e+1, p2e+(hsegs - 1)*(csegs - 1) # slice face 1
	f2 = f1e+1 # slice face 2

	# inner and our cylinders
	for o, p in ((0,0),((ssegs*hsegs),1)):
		for i in range(hsegs):
			for j in range(ssegs - 1):
				a = j+((i+p)*ssegs)+o
				b = a+1
				c = a+ssegs+1
				d = c - 1
				if o == 0:
					faces.append((a,b,c,d)) # inner faces
				else:
					faces.append((d,c,b,a)) # outer faces
	# lower cap
	for i in range(csegs):
		for j in range(ssegs - 1):
			if i == 0:
				a = j + c1
			else:
				a = j + p1 + (i - 1) * ssegs
			b = a + 1
			if i < csegs - 1:
				c = j + p1 + i * ssegs + 1
			else:
				c = j + c2 + 1
			d = c - 1
			faces.append((d, c, b, a))
	# upper cap
	for i in range(csegs):
		for j in range(ssegs - 1):
			if i == 0:
				a = j + c1e - ssegs + 1
			else:
				a = j + p2 + (i - 1) * ssegs
			b = a + 1
			if i < csegs - 1:
				c = j + p2 + i * ssegs + 1
			else:
				c = j + c2e - ssegs + 2
			d = c - 1
			faces.append((a, b, c, d))

	if sliceon:
		# Cap faces 2
		for o, f in ((0, f1), (ssegs - 1, f2)):
			for i in range(hsegs):
				for j in range(csegs):
					# Get A
					if i == 0:
						if j == 0:
							a = c1 + o
						else:
							a = p1 + o + (j - 1) * ssegs
					else:
						if j == 0:
							a = c1 + o + i * ssegs
						else:
							a = f + (i - 1) + (j - 1) * (hsegs - 1)
					# Get B
					if i == 0:
						if j < csegs - 1:
							b = p1 + o + j * ssegs
						else:
							b = c2 + o
					else:
						if j < csegs - 1:
							b = f + (i - 1) + j * (hsegs - 1)
						else:
							b = c2 + o + i * ssegs
					# Get C
					if i < hsegs - 1:
						if j < csegs - 1:
							c = f + i + j * (hsegs - 1)
						else:
							c = c2 + o + (i + 1) * ssegs
					else:
						if j < csegs - 1:
							c = p2 + o + j * ssegs
						else:
							c = c2 + o + (i + 1) * ssegs
					# Get D
					if i < hsegs - 1:
						if j == 0:
							d = c1 + o + (i + 1) * ssegs
						else:
							d = f + i + (j - 1) * (hsegs - 1)
					else:
						if j == 0:
							d = c1 + o + (i + 1) * ssegs
						else:
							d = p2 + o + (j - 1) * ssegs
					if o == 0:
						faces.append((d, c, b, a))
					else:
						faces.append((a, b, c, d))
	else:
		#Close gap
		for cx in [c1, c2]:
			for i in range(hsegs):
				a = cx + i * ssegs
				b = a + ssegs
				c = cx + (i + 2) * ssegs - 1
				d = b - 1
				if cx == 0:
					faces.append((a, b, c, d))
				else:
					faces.append((d, c, b, a))

		for i in range(csegs):
			# TODO refne this part like lower one
			# combine if possble
			if i == 0:
				a = c1
			else:
				a = p1 + (i - 1) * ssegs
			if i < csegs - 1:
				b = p1 + i * ssegs
			else:
				b = c2
			c = b + ssegs - 1
			d = a + ssegs - 1
			faces.append((d, c, b, a))

		for i in range(csegs):
			if i == 0:
				a = c1 + hsegs * ssegs
			else:
				a = p2 + (i - 1) * ssegs
			b = a + ssegs - 1
			if i < csegs - 1:
				c = p2 + ssegs - 1 + i * ssegs
			else:
				c = c2 + hsegs * ssegs + ssegs - 1
			d = c - ssegs + 1
			faces.append((d, c, b, a))

	return verts, edges, faces



class Tube(Primitive_Geometry_Class):
	def init(self):
		self.classname = "Tube"
		self.finishon = 4

	def create(self, ctx):
		mesh = get_tube_mesh(0, 0, 0, 1, 1, 18, False, 0, 360)
		self.create_mesh(ctx, mesh, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.ssegs = 18

	def update(self):
		pd = self.data.primitivedata
		mesh = get_tube_mesh(pd.radius1, pd.radius2, pd.height,
			pd.hsegs, pd.csegs, pd.ssegs,
			pd.sliceon, pd.sfrom, pd.sto)
		self.update_mesh(mesh)

	def abort(self):
		bpy.ops.object.delete({'selected_objects': [self.owner]})



class Create_OT_Tube(Draw_Primitive):
	bl_idname = "create.tube"
	bl_label = "Tube"
	subclass = Tube()
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



def register_tube():
	bpy.utils.register_class(Create_OT_Tube)

def unregister_tube():
	bpy.utils.unregister_class(Create_OT_Tube)

if __name__ == "__main__":
	register_tube()