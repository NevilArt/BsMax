import bpy
from bpy.types import PropertyGroup
from bpy.app.handlers import persistent
from bpy.props import * # StringProperty,IntProperty,FloatProperty,BoolProperty,EnumProperty
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
from primitive.torus import Torus
from primitive.tube import Tube
from primitive.arc import Arc
from primitive.circle import Circle
from primitive.donut import Donut
from primitive.ellipse import Ellipse
from primitive.extrude import Extrude
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
	elif name == "GeoSphere": return GeoSphere()
	elif name == "Icosphere": return Icosphere()
	elif name == "Mesher": return Mesher()
	elif name == "Monkey": return Monkey()
	elif name == "OilTank": return OilTank()
	elif name == "Plane": return Plane()
	elif name == "Pyramid": return Pyramid()
	elif name == "Sphere": return Sphere()
	elif name == "Torus": return Torus()
	elif name == "Tube": return Tube()
	elif name == "Arc": return Arc()
	elif name == "Circle": return Circle()
	elif name == "Donut": return Donut()
	elif name == "Ellipse": return Ellipse()
	elif name == "Extrude": return Extrude()
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
		subclass.update()

def update(data):
	subclass = get_class(data.primitivedata.classname)
	if subclass != None:
		subclass.data = data
		subclass.update()

@persistent
def primities_update(scene):
	for data in bpy.data.meshes:
		if data.primitivedata.animatable:
			update(data)
	for data in bpy.data.curves:
		if data.primitivedata.animatable:
			update(data)

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

	mode: StringProperty(update=primitive_update)
	target: StringProperty(update=primitive_update)

	profilo_mode: EnumProperty(name='Shape',default='Angle',
		update = primitive_update,
		items =[('Angle','Angle',''),('Bar','Bar',''),
				('Channel','Channel',''),('Cylinder','Cylinder',''),
				('Pipe','Pipe',''),('Tee','Tee',''),('Tube','Tube',''),
				('Width_flange','Width_flange',''),('Elipse','Elipse','')])

def update_cls(register):
	if register:
		bpy.utils.register_class(PrimitiveData)
		bpy.types.Mesh.primitivedata = PointerProperty(type=PrimitiveData)
		bpy.types.Curve.primitivedata = PointerProperty(type=PrimitiveData)
		bpy.app.handlers.frame_change_post.append(primities_update)
	else:
		bpy.utils.unregister_class(PrimitiveData)

if __name__ == '__main__':
	update_cls(True)
	
__all_ = ["update_cls"]