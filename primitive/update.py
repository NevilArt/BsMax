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
from bpy.props import (StringProperty, IntProperty, FloatProperty,
	BoolProperty, EnumProperty, PointerProperty)
from primitive.box import Box
from .capsule import Capsule
from .cylinder import Cylinder, Cone
#frome .geoSphere import GeoSphere
from .icosphere import Icosphere
from .mesher import Mesher
from .monkey import Monkey
from .oiltank import OilTank
from .plane import Plane
from .pyramid import Pyramid
from .sphere import Sphere
from .teapot import Teapot
from .torus import Torus
from .tube import Tube
from .arc import Arc
from .circle import Circle
from .donut import Donut
from .ellipse import Ellipse
from .extrude import Extrude_Curve, Extrude_Mesh
from .helix import Helix
from .ngon import NGon
from .profilo import Profilo
from .rectangle import Rectangle
from .star import Star
from .light import Compass

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

def primitive_update(self,ctx):
	if ctx.object:
		subclass = get_class(ctx.object.data.primitivedata.classname)
		if subclass:
			subclass.data = ctx.object.data
			subclass.update()

def update(data):
	subclass = get_class(data.primitivedata.classname)
	if subclass:
		subclass.data = data
		subclass.update()

@persistent
def primitive_frame_update(scene):
	for data in bpy.data.meshes:
		if data.primitivedata.animatable:
			update(data)
	for data in bpy.data.curves:
		if data.primitivedata.animatable:
			update(data)



class Primitive_Option(PropertyGroup):
	draw_mode: EnumProperty(name='Draw Mode (Under Construction)', default='FLOOR',
		update = primitive_update,
		items =[('FLOOR', 'Draw on Floor', ''),
			('VIEW', 'Draw on View', ''),
			('SURFACE', 'Draw on Surface', '')])

	# temprary will remove #
	position: BoolProperty(name='Position', default=False,
		description='Create object on raycasted position aligned to view')
	normal: BoolProperty(name='Normal', default=False,
		description='Create object on raycasted position aligned to face normal')
	
	

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

	profilo_mode: EnumProperty(name='Shape', default='Angle',
		update = primitive_update,
		items =[('Angle', 'Angle', ''),
			('Bar', 'Bar', ''),
			('Channel', 'Channel', ''),
			('Cylinder', 'Cylinder', ''),
			('Pipe', 'Pipe', ''),
			('Tee', 'Tee', ''),
			('Tube', 'Tube', ''),
			('Width_flange', 'Width_flange', ''),
			('Elipse', 'Elipse', '')])

	extrude_segmode: EnumProperty(name='Segment Type', default='Curve',
		update = primitive_update,
		items =[('Curve', 'Curve', ''),
			('Manual', 'Manual', ''),
			('Optimized', 'Optimized', ''),
			('Adaptive', 'Adaptive', '')])

def register_update():
	if hasattr(bpy.types.Mesh, 'primitivedata') or hasattr(bpy.types.Curve, 'primitivedata'):
		unregister_update()
	try:
		bpy.utils.register_class(PrimitiveData)
		bpy.utils.register_class(Primitive_Option)
	except:
		pass
		""" pass if it is allready exist and do not need to add again """

	bpy.types.Scene.primitive_setting = PointerProperty(type=Primitive_Option, name='Primitive settings')
	bpy.types.Mesh.primitivedata = PointerProperty(type=PrimitiveData)
	bpy.types.Curve.primitivedata = PointerProperty(type=PrimitiveData)
	bpy.app.handlers.frame_change_post.append(primitive_frame_update)

def unregister_update():
	del bpy.types.Mesh.primitivedata
	del bpy.types.Curve.primitivedata
	del bpy.types.Scene.primitive_setting
	
	bpy.utils.unregister_class(PrimitiveData)
	bpy.utils.unregister_class(Primitive_Option)