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
from bpy.types import PropertyGroup
from bpy.app.handlers import persistent
from bpy.props import StringProperty,IntProperty,FloatProperty,BoolProperty,EnumProperty,PointerProperty
from primitive.box import Box
from primitive.capsule import Capsule
from primitive.cylinder import Cylinder, Cone
#from primitive.geoSphere import GeoSphere
from primitive.icosphere import Icosphere
from primitive.mesher import Mesher
from primitive.monkey import Monkey
from primitive.oiltank import OilTank
from primitive.plane import Plane
from primitive.pyramid import Pyramid
from primitive.sphere import Sphere
from primitive.teapot import Teapot
from primitive.torus import Torus
from primitive.tube import Tube
from primitive.arc import Arc
from primitive.circle import Circle
from primitive.donut import Donut
from primitive.ellipse import Ellipse
from primitive.extrude import Extrude_Curve, Extrude_Mesh
from primitive.helix import Helix
from primitive.ngon import NGon
from primitive.profilo import Profilo
from primitive.rectangle import Rectangle
from primitive.star import Star
from primitive.light import Compass

# Classes
def get_class(name):
	if name == "Box": return Box()
	elif name == "Capsule": return Capsule()
	elif name == "Cone": return Cone()
	elif name == "Cylinder": return Cylinder()
	# elif name == "GeoSphere": return GeoSphere()
	elif name == "Icosphere": return Icosphere()
	elif name == "Mesher": return Mesher()
	elif name == "Monkey": return Monkey()
	elif name == "OilTank": return OilTank()
	elif name == "Plane": return Plane()
	elif name == "Pyramid": return Pyramid()
	elif name == "Sphere": return Sphere()
	elif name == "Teapot": return Teapot()
	elif name == "Torus": return Torus()
	elif name == "Tube": return Tube()
	elif name == "Arc": return Arc()
	elif name == "Circle": return Circle()
	elif name == "Donut": return Donut()
	elif name == "Ellipse": return Ellipse()
	elif name == "Extrude_Curve": return Extrude_Curve()
	elif name == "Extrude_Mesh": return Extrude_Mesh()
	elif name == "Helix": return Helix()
	elif name == "NGon": return NGon()
	elif name == "Profilo": return Profilo()
	elif name == "Rectangle": return Rectangle()
	elif name == "Star": return Star()
	elif name == "Compass": return Compass()
	else: return None

def primitive_update(self, ctx):
	obj = ctx.object
	subclass = get_class(obj.data.primitivedata.classname)
	if subclass != None:
		subclass.data = obj.data
		subclass.update(ctx)

def update(ctx, data):
	subclass = get_class(data.primitivedata.classname)
	if subclass != None:
		subclass.data = data
		subclass.update(ctx)

@persistent
def primities_update(scene):
	for data in bpy.data.meshes:
		if data.primitivedata.animatable:
			update(bpy.context, data)
	for data in bpy.data.curves:
		if data.primitivedata.animatable:
			update(bpy.context, data)

class PrimitiveData(PropertyGroup):
	classname: StringProperty()
	animatable: BoolProperty(update=primitive_update)
	width: FloatProperty(unit='LENGTH', update=primitive_update, min= 0)
	length: FloatProperty(unit='LENGTH', update=primitive_update, min= 0)
	height: FloatProperty(unit='LENGTH', update=primitive_update, min= 0)
	radius1: FloatProperty(unit='LENGTH', update=primitive_update, min= 0)
	radius2: FloatProperty(unit='LENGTH', update=primitive_update, min= 0)
	chamfer1: FloatProperty(unit='LENGTH', update=primitive_update, min= 0)
	chamfer2: FloatProperty(unit='LENGTH', update=primitive_update, min= 0)
	chamfer3: FloatProperty(unit='LENGTH', update=primitive_update, min= 0)
	
	sliceon: BoolProperty(update=primitive_update)
	sfrom: FloatProperty(update=primitive_update)
	sto: FloatProperty(update=primitive_update, default= 360)

	rotation: FloatProperty(update=primitive_update)
	twist: FloatProperty(update=primitive_update)
	turns: FloatProperty(update=primitive_update, min= 0)

	offset_x: FloatProperty(update=primitive_update)
	offset_y: FloatProperty(update=primitive_update)

	bias: FloatProperty(update=primitive_update, min= 0, max= 1, step= 4)
	bias_np: FloatProperty(update=primitive_update, min= -1, max= 1, step= 4)
	thickness: FloatProperty(unit='LENGTH', update=primitive_update)

	seed: IntProperty(update=primitive_update, min= 0, default= 0)
	random: FloatProperty(update=primitive_update)

	wsegs: IntProperty(update=primitive_update, min= 1, max= 1000, default= 1)
	lsegs: IntProperty(update=primitive_update, min= 1, max= 1000, default= 1)
	hsegs: IntProperty(update=primitive_update, min= 1, max= 1000, default= 1)
	csegs: IntProperty(update=primitive_update, min= 1, max= 1000, default= 1)
	ssegs: IntProperty(update=primitive_update, min= 3, max= 1000, default= 3)
	ssegs_b: IntProperty(update=primitive_update, min= 3, max= 1000, default= 3)
	pivotaligne: IntProperty(update=primitive_update, min= 1, max= 9, default= 5)

	center: BoolProperty(update=primitive_update)
	seglock: BoolProperty(update=primitive_update, default=True)
	base: BoolProperty(update=primitive_update)
	outline: BoolProperty(update=primitive_update)
	smooth: BoolProperty(update=primitive_update)
	ccw: BoolProperty(update=primitive_update)
	corner: BoolProperty(update=primitive_update)
	mirror_x: BoolProperty(update=primitive_update)
	mirror_y: BoolProperty(update=primitive_update)

	bool1:BoolProperty(update=primitive_update)
	bool2:BoolProperty(update=primitive_update)
	bool3:BoolProperty(update=primitive_update)
	bool4:BoolProperty(update=primitive_update)

	mode: StringProperty(update=primitive_update)
	target: StringProperty(update=primitive_update)

	profilo_mode: EnumProperty(name='Shape',default='Angle',
		update = primitive_update,
		items =[('Angle','Angle',''),('Bar','Bar',''),
				('Channel','Channel',''),('Cylinder','Cylinder',''),
				('Pipe','Pipe',''),('Tee','Tee',''),('Tube','Tube',''),
				('Width_flange','Width_flange',''),('Elipse','Elipse','')])

	extrude_segmode: EnumProperty(name='Segment Type',default='Curve',
		update = primitive_update,
		items =[('Curve','Curve',''),('Manual','Manual',''),('Optimized','Optimized',''),('Adaptive','Adaptive','')])

def register_update():
	if hasattr(bpy.types.Mesh,'primitivedata') or hasattr(bpy.types.Curve,'primitivedata'):
		unregister_update()
	bpy.utils.register_class(PrimitiveData)
	bpy.types.Mesh.primitivedata = PointerProperty(type=PrimitiveData)
	bpy.types.Curve.primitivedata = PointerProperty(type=PrimitiveData)
	bpy.app.handlers.frame_change_post.append(primities_update)

def unregister_update():
	bpy.utils.unregister_class(PrimitiveData)