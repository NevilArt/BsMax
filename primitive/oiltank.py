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
from bpy.types import Operator
from math import pi, sin, cos, radians
from primitive.primitive import PrimitiveGeometryClass, CreatePrimitive
from bsmax.actions import delete_objects

def get_oiltank_mesh(radius,height,capheight,blend,ssegs,csegs,hsegs,sliceon,sfrom,sto):
	verts,edges,faces = [],[],[]
	sides,heights = [],[]
	arcrange,slicestep,r = pi*2,0,radius

	# get zscale of arc
	zscale = (capheight/radius) if radius > 0 else 0

	# fix height value
	height -= capheight * 2 if capheight > 0 else 0

	# height
	if sliceon:
		arcrange,slicestep = radians(sto-sfrom),1

	# collect segments x y onece
	for i in range(ssegs+slicestep):
		d = (arcrange/ssegs)*i+radians(sfrom)
		sides.append([sin(d),cos(d)])

	# get offsets
	zoffset1 = 0 if zscale > 0 else -radius*zscale
	zoffset2 = radius*zscale if zscale > 0 else 0
	zoffset3 = height+(zscale*radius)*2 if zscale > 0 else height+(zscale*radius)

	# collect cap arc height and scale
	for i in range(csegs):
		d = ((pi/2)/csegs)*i
		s = cos(d)
		h = sin(d)*zscale
		heights.append([h,s])
	heights.reverse()

	# add one more step if sclise is on
	ssegs += slicestep
	# Create vertexes data
	step = (pi*2)/ssegs

	# first vertex
	verts.append([0,0,zoffset1])
	# lower part
	for h, s in heights:
		for x, y in sides:
			X = r*x*s
			Y = r*y*s
			Z = radius*zscale-r*h+zoffset1
			verts.append([X,Y,Z])
		if sliceon:
			verts.append([0,0,Z])

	# Cylinder part
	h = height/hsegs
	for i in range(1,hsegs):
		for x,y in sides:
			X = r*x
			Y = r*y
			#Z = radius + h * i
			Z = zoffset2 + h * i
			verts.append([X,Y,Z])
		if sliceon:
				verts.append([0,0,Z])

	# uppaer part
	heights.reverse()
	for h,s in heights:
		for x,y in sides:
			X = r*x*s
			Y = r*y*s
			Z = zoffset2+r*h+height
			verts.append([X,Y,Z])
		if sliceon:
			verts.append([0,0,Z])
	# add last vertex
	verts.append([0,0,zoffset3])

	# uper triangles faces
	if sliceon:
		ssegs += 1
	for i in range(ssegs):
		a = i+1
		b = i+2
		c = 0
		if i < ssegs - 1:
			faces.append((a,b,c))
		else:
			faces.append((a,1,c))

	# body faces
	for i in range(csegs*2+hsegs-2):
		for j in range(ssegs):
			a = i*ssegs+j+1
			if j < ssegs-1:
				b = a+1
				c = a+ssegs+1
				d = c-1
			else:
				b = a-(ssegs-1)
				c = a+1
				d = a+ssegs
			faces.append((d,c,b,a))

	# lover triangels
	f = ssegs*(((csegs-1)*2)+hsegs)+1
	c = len(verts)-1
	for i in range(ssegs):
		a = i+f
		b = a+1 
		if i < ssegs-1:
			faces.append((c,b,a))
		else:
			faces.append((c,f,a))
	return verts,edges,faces

class OilTank(PrimitiveGeometryClass):
	def __init__(self):
		self.classname = "OilTank"
		self.finishon = 4
		self.owner = None
		self.data = None
	def reset(self):
		self.__init__()
	def create(self, ctx):
		mesh = get_oiltank_mesh(0,0,0,0,18,8,6,False,0,360)
		self.create_mesh(ctx, mesh, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.ssegs, pd.csegs, pd.hsegs = 18,8,3
		pd.center = True
	def update(self):
		pd = self.data.primitivedata
		csegs = pd.csegs if not pd.seglock else pd.ssegs-2
		if pd.center:
			height = pd.height
		else:
			diameter = pd.radius1*2
			if pd.height < diameter:
				pd.height = diameter
			height = pd.height-pd.radius1*2
		""" limit the cao height with heaight """
		if pd.thickness*2 > height:
			pd.thickness = height/2
		if pd.thickness*2 < -height:
			pd.thickness = -height/2
		mesh = get_oiltank_mesh(pd.radius1, height,
			pd.thickness, pd.chamfer1, # capheight, blend
			pd.ssegs, csegs, pd.hsegs,
			pd.sliceon, pd.sfrom, pd.sto)
		self.update_mesh(mesh)
	def abort(self):
		delete_objects([self.owner])

class Create_OT_OilTank(CreatePrimitive):
	bl_idname = "create.oiltank"
	bl_label = "OilTank"
	subclass = OilTank()

	def create(self, ctx, clickpoint):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = clickpoint.view
		self.subclass.owner.rotation_euler = clickpoint.orient
	def update(self, ctx, clickcount, dimantion):
		if clickcount == 1:
			self.params.radius1 = dimantion.radius
		elif clickcount == 2:
			self.params.height = dimantion.height
		elif clickcount == 3:
			self.params.thickness = dimantion.height
		if clickcount > 0:
			self.subclass.update()
	def finish(self):
		pass

def register_oiltank():
	bpy.utils.register_class(Create_OT_OilTank)
	
def unregister_oiltank():
	bpy.utils.unregister_class(Create_OT_OilTank)