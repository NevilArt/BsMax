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
from math import sin, cos, pi, radians
from primitive.primitive import CreatePrimitive, PrimitiveGeometryClass
from bsmax.actions import delete_objects

def GetTorusMesh( radius1, radius2, rotation, twist, 
				segments, sides, sliceon, sfrom, sto):
	verts,edges,faces,segs = [],[],[],[]
	rotation, twist = radians(rotation), radians(twist)
	sfrom, sto = radians(sfrom), radians(sto)
	arcrange, slicestep = pi*2, 0
	r1,r2 = radius1,radius2
	if sliceon:
		arcrange,slicestep = sto-sfrom, 1
	# collect segments x y onece
	for i in range(segments + slicestep):
		d = ((arcrange/segments)*i)+sfrom
		segs.append([sin(d),cos(d)])

	# add one more step if sclise is on
	segments += slicestep

	# Create vertexes data
	step = (pi*2)/sides
	tw = twist/(segments-slicestep)
	for i in range(len(segs)):
		x, y = segs[i]
		for j in range(sides):
			d = j*step+i*tw+rotation
			X = (r1+r2*cos(d))*x 
			Y = (r1+r2*cos(d))*y
			Z = r2*sin(d)
			verts.append([X,Y,Z])

	# create face data
	for i in range(segments - 1):
		for j in range(sides):
			a = j+i*sides
			if j < sides - 1:
				b = a+1
				c = j+(i+1)*sides+1
				d = c-1
			else:
				b = i*sides
				c = a+1
				d = j+(i+1)*sides
			faces.append((a,b,c,d))

	# apply slice for create cap or conncet end to start
	if sliceon:
		c1,c2 = [],[]
		l = segments*sides-sides
		for i in range(sides):
			c1.append(sides - i - 1)
			c2.append(l+i)
		faces += [c1, c2]	
	else:
		for i in range(sides):
			a = i
			if i < sides - 1:
				b = a+1
				c = i+sides*(segments-1)+1
				d = c-1
			else:
				b = 0
				c = sides*(segments-1)
				d = sides*segments-1
			faces.append((d,c,b,a))
	return verts, edges, faces

class Torus(PrimitiveGeometryClass):
	def __init__(self):
		self.classname = "Torus"
		self.finishon = 3
		self.owner = None
		self.data = None
	def reset(self):
		self.__init__()
	def create(self, ctx):
		mesh = GetTorusMesh(0, 0, 0, 0, 24, 12, False, 0, 360)
		self.create_mesh(ctx, mesh, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.ssegs, pd.ssegs_b = 24, 12
	def update(self):
		pd = self.data.primitivedata
		mesh = GetTorusMesh(pd.radius1, pd.radius2, pd.rotation, pd.twist, 
				pd.ssegs, pd.ssegs_b, pd.sliceon, pd.sfrom, pd.sto)
		self.update_mesh(mesh)
	def abort(self):
		delete_objects([self.owner])

class BsMax_OT_CreateTorus(CreatePrimitive):
	bl_idname = "bsmax.createtorus"
	bl_label = "Torus (Create)"
	subclass = Torus()

	def create(self, ctx, clickpoint):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = clickpoint.view
		self.subclass.owner.rotation_euler = clickpoint.orient
	def update(self, ctx, clickcount, dimantion):
		if clickcount == 1:
			self.params.radius1 = dimantion.radius
			self.params.radius2 = self.params.radius1 / 10
		elif clickcount == 2:
			self.params.radius2 = dimantion.radius
		if clickcount > 0:
			self.subclass.update()
	def finish(self):
		pass

def register_torus():
	bpy.utils.register_class(BsMax_OT_CreateTorus)

def unregister_torus():
	bpy.utils.unregister_class(BsMax_OT_CreateTorus)