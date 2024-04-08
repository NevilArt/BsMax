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

from bpy.types import Operator, PropertyGroup
from bpy.app.handlers import persistent
from bpy.utils import register_class, unregister_class

from bpy.props import (
	StringProperty, IntProperty, FloatProperty,
	BoolProperty, EnumProperty, PointerProperty,
	FloatVectorProperty
)

# from .adaptive_plane import Adaptive_Plane
from .box import Box
from .bolt import Bolt
from .capsule import Capsule
from .cylinder import Cylinder, Cone
#frome .geoSphere import GeoSphere
from .icosphere import Icosphere
from .monkey import Monkey
from .oiltank import OilTank
from .plane import Plane
from .pyramid import Pyramid
from .quadsphere import QuadSphere
from .sphere import Sphere
from .teapot import Teapot
from .torus import Torus
from .torusknot import TorusKnot
from .tube import Tube
from .arc import Arc
from .circle import Circle
from .donut import Donut
from .ellipse import Ellipse
from .helix import Helix
from .ngon import NGon
from .profilo import Profilo
from .rectangle import Rectangle
from .star import Star
from .light import Compass


# Classes
def get_class(name):
	# if name == "Adaptive_Plane": return Adaptive_Plane()
	if name == "Box": return Box()
	elif name == "Bolt": return Bolt()
	elif name == "Capsule": return Capsule()
	elif name == "Cone": return Cone()
	elif name == "Cylinder": return Cylinder()
	elif name == "Icosphere": return Icosphere()
	elif name == "Monkey": return Monkey()
	elif name == "OilTank": return OilTank()
	elif name == "Plane": return Plane()
	elif name == "Pyramid": return Pyramid()
	elif name == "QuadSphere": return QuadSphere()
	elif name == "Sphere": return Sphere()
	elif name == "Teapot": return Teapot()
	elif name == "Torus": return Torus()
	elif name == "TorusKnot": return TorusKnot()
	elif name == "Tube": return Tube()
	elif name == "Arc": return Arc()
	elif name == "Circle": return Circle()
	elif name == "Donut": return Donut()
	elif name == "Ellipse": return Ellipse()
	elif name == "Helix": return Helix()
	elif name == "NGon": return NGon()
	elif name == "Profilo": return Profilo()
	elif name == "Rectangle": return Rectangle()
	elif name == "Star": return Star()
	elif name == "Compass": return Compass()
	else: return None


# call if parametrs updated from ui manualy
def primitive_update(_, ctx):
	if not ctx.object:
		return

	subclass = get_class(ctx.object.data.primitivedata.classname)
	if subclass:
		subclass.data = ctx.object.data
		subclass.update()


# call if parameter are animatable and time changed
def update(data):
	subclass = get_class(data.primitivedata.classname)
	if subclass:
		subclass.data = data
		subclass.update()


# Callback function for update primitives if are animatable
@persistent
def primitive_frame_update(_):
	for data in bpy.data.meshes:
		if data.primitivedata.animatable:
			update(data)

	for data in bpy.data.curves:
		if data.primitivedata.animatable:
			update(data)


class Primitive_Option(PropertyGroup):
	draw_mode: EnumProperty(
		name='Draw Mode', default='FLOOR',
		update = primitive_update,
		items =[
			('FLOOR', 'Gride', 'Draw on Floor Gride', 'EVENT_F', 1),
			('VIEW', 'View' ,'Draw on View', 'EVENT_V', 2),
			('SURFACE', 'Surface', 'Draw on Surface', 'EVENT_S', 3)
		]
	)

	#TODO countinu from here
	active_tool: StringProperty()
	next_name: StringProperty()
	next_color: FloatVectorProperty(
		name='Color', subtype='COLOR', default=[0.5, 0.5, 0.5]
	)


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

	# Profile ###############################################

	profilo_mode: EnumProperty(
		name='Shape', default='Angle',
		update = primitive_update,
		items =[
			('Angle', 'Angle', ''),
			('Bar', 'Bar', ''),
			('Channel', 'Channel', ''),
			('Cylinder', 'Cylinder', ''),
			('Pipe', 'Pipe', ''),
			('Tee', 'Tee', ''),
			('Tube', 'Tube', ''),
			('Width_flange', 'Width_flange', ''),
			('Elipse', 'Elipse', '')
		]
	)

	extrude_segmode: EnumProperty(
		name='Segment Type', default='Curve',
		update = primitive_update,
		items =[
			('Curve', 'Curve', ''),
			('Manual', 'Manual', ''),
			('Optimized', 'Optimized', ''),
			('Adaptive', 'Adaptive', '')
		]
	)

	# BoltFactory #############################################

	MAX_INPUT_NUMBER = 50

	Bolt : BoolProperty(
		name="Bolt",
		update = primitive_update,
		default=True,
		description="Bolt"
	)
	
	change : BoolProperty(
		name = "Change",
		update = primitive_update,
		default = False,
		description = "change Bolt"
	)

	# Model Types
	Model_Type_List = [
		('bf_Model_Bolt', 'BOLT', 'Bolt Model'),
		('bf_Model_Nut', 'NUT', 'Nut Model')
	]

	bf_Model_Type: EnumProperty(
		attr='bf_Model_Type',
		name='Model',
		update = primitive_update,
		description='Choose the type off model you would like',
		items=Model_Type_List, default='bf_Model_Bolt'
	)

	# Head Types
	Model_Type_List = [
		('bf_Head_Hex', 'HEX', 'Hex Head'),
		('bf_Head_12Pnt', '12 POINT', '12 Point Head'),
		('bf_Head_Cap', 'CAP', 'Cap Head'),
		('bf_Head_Dome', 'DOME', 'Dome Head'),
		('bf_Head_Pan', 'PAN', 'Pan Head'),
		('bf_Head_CounterSink', 'COUNTER SINK', 'Counter Sink Head')
	]

	bf_Head_Type: EnumProperty(
		attr='bf_Head_Type',
		name='Head',
		update = primitive_update,
		description='Choose the type off Head you would like',
		items=Model_Type_List, default='bf_Head_Hex'
	)

	# Bit Types
	Bit_Type_List = [
		('bf_Bit_None', 'NONE', 'No Bit Type'),
		('bf_Bit_Allen', 'ALLEN', 'Allen Bit Type'),
		('bf_Bit_Torx', 'TORX', 'Torx Bit Type'),
		('bf_Bit_Philips', 'PHILLIPS', 'Phillips Bit Type')
	]

	bf_Bit_Type: EnumProperty(
		attr='bf_Bit_Type',
		name='Bit Type',
		update = primitive_update,
		description='Choose the type of bit to you would like',
		items=Bit_Type_List, default='bf_Bit_None'
	)

	# Nut Types
	Nut_Type_List = [
		('bf_Nut_Hex', 'HEX', 'Hex Nut'),
		('bf_Nut_Lock', 'LOCK', 'Lock Nut'),
		('bf_Nut_12Pnt', '12 POINT', '12 Point Nut')
	]

	bf_Nut_Type: EnumProperty(
		attr='bf_Nut_Type',
		name='Nut Type',
		update = primitive_update,
		description='Choose the type of nut you would like',
		items=Nut_Type_List,
		default='bf_Nut_Hex'
	)

	# Shank Types
	bf_Shank_Length: FloatProperty(
		attr='bf_Shank_Length',
		name='Shank Length', default=0,
		update = primitive_update,
		min=0, soft_min=0, max=MAX_INPUT_NUMBER,
		description='Length of the unthreaded shank',
		unit='LENGTH'
	)

	bf_Shank_Dia: FloatProperty(
		attr='bf_Shank_Dia',
		name='Shank Dia', default=3,
		min=0, soft_min=0,
		max=MAX_INPUT_NUMBER,
		update = primitive_update,
		description='Diameter of the shank',
		unit='LENGTH'
	)

	bf_Phillips_Bit_Depth: FloatProperty(
		attr='bf_Phillips_Bit_Depth',
		name='Bit Depth', default=1.1431535482406616,
		min=0, soft_min=0,
		max=MAX_INPUT_NUMBER,
		update = primitive_update,
		description='Depth of the Phillips Bit',
		unit='LENGTH'
	)

	bf_Allen_Bit_Depth: FloatProperty(
		attr='bf_Allen_Bit_Depth',
		name='Bit Depth', default=1.5,
		min=0, soft_min=0,
		max=MAX_INPUT_NUMBER,
		update = primitive_update,
		description='Depth of the Allen Bit',
		unit='LENGTH'
	)

	bf_Allen_Bit_Flat_Distance: FloatProperty(
		attr='bf_Allen_Bit_Flat_Distance',
		name='Flat Dist', default=2.5,
		min=0, soft_min=0,
		max=MAX_INPUT_NUMBER,
		update = primitive_update,
		description='Flat Distance of the Allen Bit',
		unit='LENGTH'
	)

	# Torx Size Types
	Torx_Size_Type_List = [
		('bf_Torx_T10', 'T10', 'T10'),
		('bf_Torx_T20', 'T20', 'T20'),
		('bf_Torx_T25', 'T25', 'T25'),
		('bf_Torx_T30', 'T30', 'T30'),
		('bf_Torx_T40', 'T40', 'T40'),
		('bf_Torx_T50', 'T50', 'T50'),
		('bf_Torx_T55', 'T55', 'T55')
	]

	bf_Torx_Size_Type: EnumProperty(
		attr='bf_Torx_Size_Type',
		name='Torx Size',
		update = primitive_update,
		description='Size of the Torx Bit',
		items=Torx_Size_Type_List,
		default='bf_Torx_T20'
	)

	bf_Torx_Bit_Depth: FloatProperty(
		attr='bf_Torx_Bit_Depth',
		name='Bit Depth', default=1.5,
		update = primitive_update,
		min=0, soft_min=0,
		max=MAX_INPUT_NUMBER,
		description='Depth of the Torx Bit',
		unit='LENGTH'
	)

	bf_Hex_Head_Height: FloatProperty(
		attr='bf_Hex_Head_Height',
		name='Head Height', default=2,
		update = primitive_update,
		min=0, soft_min=0, max=MAX_INPUT_NUMBER,
		description='Height of the Hex Head',
		unit='LENGTH'
	)

	bf_Hex_Head_Flat_Distance: FloatProperty(
		attr='bf_Hex_Head_Flat_Distance',
		name='Flat Dist', default=5.5,
		update = primitive_update,
		min=0, soft_min=0,
		max=MAX_INPUT_NUMBER,
		description='Flat Distance of the Hex Head',
		unit='LENGTH'
	)

	bf_12_Point_Head_Height: FloatProperty(
		attr='bf_12_Point_Head_Height',
		name='Head Height', default=3.0,
		update = primitive_update,
		min=0, soft_min=0, max=MAX_INPUT_NUMBER,
		description='Height of the 12 Point Head',
		unit='LENGTH'
	)

	bf_12_Point_Head_Flat_Distance: FloatProperty(
		attr='bf_12_Point_Head_Flat_Distance',
		name='Flat Dist', default=3.0,
		update = primitive_update,
		min=0.001, soft_min=0,    #limit to 0.001 to avoid calculation error
		max=MAX_INPUT_NUMBER,
		description='Flat Distance of the 12 Point Head',
		unit='LENGTH'
	)

	bf_12_Point_Head_Flange_Dia: FloatProperty(
		attr='bf_12_Point_Head_Flange_Dia',
		name='12 Point Head Flange Dia', default=5.5,
		update = primitive_update,
		min=0, soft_min=0,
		max=MAX_INPUT_NUMBER,
		description='Flange diameter of the 12 point Head',
		unit='LENGTH'
	)

	bf_CounterSink_Head_Dia: FloatProperty(
		attr='bf_CounterSink_Head_Dia',
		name='Head Dia', default=6.300000190734863,
		update = primitive_update,
		min=0, soft_min=0,
		max=MAX_INPUT_NUMBER,
		description='Diameter of the Counter Sink Head',
		unit='LENGTH'
	)

	bf_Cap_Head_Height: FloatProperty(
		attr='bf_Cap_Head_Height',
		name='Head Height', default=3,
		update = primitive_update,
		min=0, soft_min=0,
		max=MAX_INPUT_NUMBER,
		description='Height of the Cap Head',
		unit='LENGTH'
	)

	bf_Cap_Head_Dia: FloatProperty(
		attr='bf_Cap_Head_Dia',
		name='Head Dia', default=5.5,
		update = primitive_update,
		min=0, soft_min=0,
		max=MAX_INPUT_NUMBER,
		description='Diameter of the Cap Head',
		unit='LENGTH'
	)

	bf_Dome_Head_Dia: FloatProperty(
		attr='bf_Dome_Head_Dia',
		name='Dome Head Dia', default=5.599999904632568,
		update = primitive_update,
		min=0, soft_min=0,
		max=MAX_INPUT_NUMBER,
		description='Length of the unthreaded shank',
		unit='LENGTH'
	)

	bf_Pan_Head_Dia: FloatProperty(
		attr='bf_Pan_Head_Dia',
		name='Pan Head Dia', default=5.599999904632568,
		update = primitive_update,
		min=0, soft_min=0,
		max=MAX_INPUT_NUMBER,
		description='Diameter of the Pan Head',
		unit='LENGTH'
	)

	bf_Philips_Bit_Dia: FloatProperty(
		attr='bf_Philips_Bit_Dia',
		name='Bit Dia', default=1.8199999332427979,
		update = primitive_update,
		min=0, soft_min=0,
		max=MAX_INPUT_NUMBER,
		description='Diameter of the Philips Bit',
		unit='LENGTH'
	)

	bf_Thread_Length: FloatProperty(
		attr='bf_Thread_Length',
		name='Thread Length', default=6,
		update = primitive_update,
		min=0, soft_min=0,
		max=MAX_INPUT_NUMBER,
		description='Length of the Thread',
		unit='LENGTH'
	)

	bf_Major_Dia: FloatProperty(
		attr='bf_Major_Dia',
		name='Major Dia', default=3,
		update = primitive_update,
		min=0, soft_min=0,
		max=MAX_INPUT_NUMBER,
		description='Outside diameter of the Thread',
		unit='LENGTH'
	)

	bf_Pitch: FloatProperty(
		attr='bf_Pitch',
		name='Pitch', default=0.3499999940395355,
		update = primitive_update,
		min=0.1, soft_min=0.1,
		max=7.0,
		description='Pitch if the thread',
		unit='LENGTH'
	)

	bf_Minor_Dia: FloatProperty(
		attr='bf_Minor_Dia',
		name='Minor Dia', default=2.6211137771606445,
		update = primitive_update,
		min=0, soft_min=0,
		max=MAX_INPUT_NUMBER,
		description='Inside diameter of the Thread',
		unit='LENGTH'
	)

	bf_Crest_Percent: IntProperty(
		attr='bf_Crest_Percent',
		name='Crest Percent', default=10,
		update = primitive_update,
		min=1, soft_min=1,
		max=90,
		description='Percent of the pitch that makes up the Crest'
	)

	bf_Root_Percent: IntProperty(
		attr='bf_Root_Percent',
		name='Root Percent', default=10,
		update = primitive_update,
		min=1, soft_min=1,
		max=90,
		description='Percent of the pitch that makes up the Root'
	)

	bf_Div_Count: IntProperty(
		attr='bf_Div_Count',
		name='Div count', default=36,
		update = primitive_update,
		min=4, soft_min=4,
		max=4096,
		description='Div count determine circle resolution'
	)

	bf_Hex_Nut_Height: FloatProperty(
		attr='bf_Hex_Nut_Height',
		name='Hex Nut Height', default=2.4000000953674316,
		update = primitive_update,
		min=0, soft_min=0,
		max=MAX_INPUT_NUMBER,
		description='Height of the Hex Nut',
		unit='LENGTH'
	)

	bf_Hex_Nut_Flat_Distance: FloatProperty(
		attr='bf_Hex_Nut_Flat_Distance',
		name='Hex Nut Flat Dist', default=5.5,
		update = primitive_update,
		min=0, soft_min=0,
		max=MAX_INPUT_NUMBER,
		description='Flat distance of the Hex Nut',
		unit='LENGTH'
	)

	bf_12_Point_Nut_Height: FloatProperty(
		attr='bf_12_Point_Nut_Height',
		name='12 Point Nut Height', default=2.4000000953674316,
		update = primitive_update,
		min=0, soft_min=0,
		max=MAX_INPUT_NUMBER,
		description='Height of the 12 Point Nut',
		unit='LENGTH'
	)

	bf_12_Point_Nut_Flat_Distance: FloatProperty(
		attr='bf_12_Point_Nut_Flat_Distance',
		name='12 Point Nut Flat Dist', default=3.0,
		update = primitive_update,
		min=0.001, soft_min=0, #limit to 0.001 to avoid calculation error
		max=MAX_INPUT_NUMBER,
		description='Flat distance of the 12 point Nut',
		unit='LENGTH'
	)

	bf_12_Point_Nut_Flange_Dia: FloatProperty(
		attr='bf_12_Point_Nut_Flange_Dia',
		name='12 Point Nut Flange Dia', default=5.5,
		update = primitive_update,
		min=0, soft_min=0,
		max=MAX_INPUT_NUMBER,
		description='Flange diameter of the 12 point Nut',
		unit='LENGTH'
	)
	
	# End of Bolt factory ###################################################



class BsMax_OT_Update_Primitive_Geometry(Operator):
	# TODO replace this with a smart convert tool
	bl_idname="primitive.update"
	bl_label="Update Primitive Mesh/Curve"
	def execute(self, ctx):
		for obj in ctx.selected_objects:
			update(obj.data)
			# objClassName = obj.data.primitivedata.classname
			# if not objClassName:
			# 	continue
			
			# subclass = get_class(objClassName)
			# if subclass:
			# 	subclass.data = ctx.object.data
			# 	subclass.update()
		return {"FINISHED"}


classes = (
	PrimitiveData,
	Primitive_Option,
	BsMax_OT_Update_Primitive_Geometry
)


def register_update():
	for c in classes:
		register_class(c)

	bpy.types.Scene.primitive_setting = PointerProperty(
		type=Primitive_Option,
		name='Primitive settings'
	)

	bpy.types.Mesh.primitivedata = PointerProperty(type=PrimitiveData)
	bpy.types.Curve.primitivedata = PointerProperty(type=PrimitiveData)
	bpy.app.handlers.frame_change_post.append(primitive_frame_update)


def unregister_update():
	for c in classes:
		unregister_class(c)

	del bpy.types.Mesh.primitivedata
	del bpy.types.Curve.primitivedata
	del bpy.types.Scene.primitive_setting