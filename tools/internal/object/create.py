############################################################################
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################################################
# 2024/03/03

import bpy
from bpy.types import Operator
from bpy.props import EnumProperty

from primitive.box import Box
from primitive.bolt import Bolt
from primitive.capsule import Capsule
from primitive.cylinder import Cylinder, Cone
from primitive.icosphere import Icosphere
from primitive.monkey import Monkey
from primitive.oiltank import OilTank
from primitive.plane import Plane
from primitive.pyramid import Pyramid
from primitive.quadsphere import QuadSphere
from primitive.sphere import Sphere
from primitive.teapot import Teapot
from primitive.torus import Torus
from primitive.torusknot import TorusKnot
from primitive.tube import Tube
from primitive.arc import Arc
from primitive.circle import Circle
from primitive.donut import Donut
from primitive.ellipse import Ellipse
from primitive.helix import Helix
from primitive.ngon import NGon
from primitive.profilo import Profilo
from primitive.rectangle import Rectangle
from primitive.star import Star


def add_parametric_primitive(type, ctx):
	primitiveClasses = {
		'BOX':Box(),
		'BOLT':Bolt(),
		'CAPSULE':Capsule(),
		'CYLINDER':Cylinder(),
		'CONE':Cone(),
		'ICOSPHERE':Icosphere(),
		'MONKEY':Monkey(),
		'OILTANK':OilTank(),
		'PLANE':Plane(),
		'PYRAMID':Pyramid(),
		'SPHERE':Sphere(),
		'TEAPOT':Teapot(),
		'TORUS':Torus(),
		'TORUSKNOT':TorusKnot(),
		'QUADSPHERE':QuadSphere(),
		'TUBE':Tube(),
		'ARC':Arc(),
		'CIRCLE':Circle(),
		'DONUT':Donut(),
		'ELLIPSE':Ellipse(),
		'HELIX':Helix(),
		'NGON':NGon(),
		'PROFILO': Profilo(),
		'RECTANGLE':Rectangle(),
		'STAR':Star()
	}

	obj = primitiveClasses[type]
	if  type != 'PROFILO':
		obj.create(ctx)

	if type == 'BOX':
		pd = obj.owner.data.primitivedata
		pd.width, pd.length, pd.height = 1, 1, 1
	
	# if type == 'BOLT':
	# 	pd = obj.owner.data.primitivedata

	elif type == 'CAPSULE':
		pd = obj.owner.data.primitivedata
		pd.radius1, pd.height = 1, 1

	elif type == 'CYLINDER':
		pd = obj.owner.data.primitivedata
		pd.radius1, pd.height = 1, 1

	elif type == 'CONE':
		pd = obj.owner.data.primitivedata
		pd.radius1, pd.radius1, pd.height = 1, 0.5, 1

	elif type == 'ICOSPHERE':
		obj.owner.data.primitivedata.radius1 = 1

	elif type == 'MONKEY':
		obj.owner.data.primitivedata.radius1 = 1

	elif type == 'OILTANK':
		pd = obj.owner.data.primitivedata
		pd.radius1, pd.height, pd.thickness = 1, 3, 1

	elif type == 'PLANE':
		pd = obj.owner.data.primitivedata
		pd.width, pd.length = 1, 1

	elif type == 'PYRAMID':
		pd = obj.owner.data.primitivedata
		pd.width, pd.length, pd.height = 1, 1, 1
	
	elif type == 'QUADSPHERE':
		pd = obj.owner.data.primitivedata
		pd.radius1, pd.ssegs, pd.bias_np = 1, 6, 1

	elif type == 'SPHERE':
		obj.owner.data.primitivedata.radius1 = 1

	elif type == 'TEAPOT':
		pd = obj.owner.data.primitivedata.radius1 = 1

	elif type == 'TORUS':
		pd = obj.owner.data.primitivedata
		pd.radius1, pd.radius2 = 1, 0.5
	
	elif type == 'TORUSKNOT':
		pd = obj.owner.data.primitivedata
		pd.radius1, pd.radius2, pd.height = 1, 0.43, 2.2

	elif type == 'TUBE':
		pd = obj.owner.data.primitivedata
		pd.radius1, pd.radius2 ,pd.height = 1, 0.5, 1
	
	elif type == 'ARC':
		pd = obj.owner.data.primitivedata
		pd.radius1, pd.sfrom, pd.sto = 1, 0, 270
		pd.sliceon = True
	
	elif type == 'CIRCLE':
		obj.owner.data.primitivedata.radius1 = 1

	elif type == 'DONUT':
		pd = obj.owner.data.primitivedata
		pd.radius1, pd.radius2 = 1, 0.5

	elif type == 'ELLIPSE':
		pd = obj.owner.data.primitivedata
		pd.width, pd.length = 1, 0.5

	elif type == 'HELIX':
		pd = obj.owner.data.primitivedata
		pd.radius1, pd.radius2, pd.height = 1, 1, 1

	elif type == 'NGON':
		obj.owner.data.primitivedata.radius1 = 1

	elif type == 'PROFILO':
		obj.create(ctx, "Angle")
		pd = obj.owner.data.primitivedata
		pd.width, pd.length, pd.thickness = 1, 1, 0.2

	elif type == 'RECTANGLE':
		pd = obj.owner.data.primitivedata
		pd.width, pd.length = 1, 1

	elif type == 'STAR':
		pd = obj.owner.data.primitivedata
		pd.radius1, pd.radius2 = 1, 0.5

	obj.update()
	ctx.active_object.location = ctx.scene.cursor.location


class Object_OT_Create(Operator):
	bl_idname = "object.create"
	bl_label = "Create (Primitive object)"
	bl_description = "Create Primitive Object"
	bl_options = {'REGISTER', 'UNDO'}

	prims = [
		('BOX','Box',''),
		('BOLT','Bolt',''),
		('CAPSULE','Capsule',''),
		('CYLINDER','Cylinder',''),
		('CONE','Cone',''),
		('ICOSPHERE','Icosphere',''),
		('MONKEY','Monkey',''),
		('OILTANK','OilTank',''),
		('PLANE','Plane',''),
		('PYRAMID','Pyramid',''),
		('QUADSPHERE','QuadSphere',''),
		('SPHERE','Sphere',''),
		('TEAPOT','Teapot',''),
		('TORUS','Torus',''),
		('TORUSKNOT','TorusKnot',''),
		('TUBE','Tube',''),
		('ARC','Arc',''),
		('CIRCLE','Circle',''),
		('DONUT','Donut',''),
		('ELLIPSE','Ellipse',''),
		('HELIX','Helix',''),
		('NGON','NGon',''),
		('PROFILO','Profilo',''),
		('RECTANGLE','Rectangle',''),
		('STAR','Star','')
	]

	type: EnumProperty(name='Object Type', items=prims, default='BOX')

	@classmethod
	def poll(self, ctx):
		return True
	
	def draw(self, ctx):
		self.layout.prop(self,"type", text="Type")

	def execute(self, ctx):
		add_parametric_primitive(self.type, ctx)
		return {'FINISHED'}

	def invoke(self, ctx, event):
		wm = ctx.window_manager
		return wm.invoke_props_dialog(self)


def register_create():
	bpy.utils.register_class(Object_OT_Create)


def unregister_create():
	bpy.utils.unregister_class(Object_OT_Create)


if __name__ == "__main__":
	register_create()