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

import bpy
from bpy.types import Operator
from bpy.props import EnumProperty
from primitive.box import Box
from primitive.capsule import Capsule
from primitive.cylinder import Cylinder, Cone
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

class Object_OT_Create(Operator):
	bl_idname = "object.create"
	bl_label = "Create (Primitive object)"
	# bl_description = ""
	bl_options = {'REGISTER', 'UNDO'}

	prims = [('BOX','Box',''), ('CAPSULE','Capsule',''), ('CYLINDER','Cylinder',''),
	('CONE','Cone',''), ('ICOSPHERE','Icosphere',''), ('MESHER','Mesher',''),
	('MONKEY','Monkey',''), ('OILTANK','OilTank',''), ('PLANE','Plane',''),
	('PYRAMID','Pyramid',''), ('SPHERE','Sphere',''), ('TEAPOT','Teapot',''),
	('TORUS','Torus',''), ('TUBE','Tube',''), ('ARC','Arc',''),
	('CIRCLE','Circle',''), ('DONUT','Donut',''), ('ELLIPSE','Ellipse',''),
	('HELIX','Helix',''), ('NGON','NGon',''), ('PROFILO','Profilo',''),
	('RECTANGLE','Rectangle',''), ('STAR','Star','')]

	type: EnumProperty(name='Object Type', items=prims, default='BOX')

	@classmethod
	def poll(self, ctx):
		return True
	
	def draw(self, ctx):
		self.layout.prop(self,"type",text="Type")

	def execute(self,ctx):
		if self.type == 'BOX':
			obj = Box()
			obj.create(ctx)
			pd = obj.owner.data.primitivedata
			pd.width, pd.length, pd.height = 1, 1, 1
			obj.update()
		elif self.type == 'CAPSULE':
			obj = Capsule()
			obj.create(ctx)
			pd = obj.owner.data.primitivedata
			pd.radius1, pd.height = 1, 1
			obj.update()
		elif self.type == 'CYLINDER':
			obj = Cylinder()
			obj.create(ctx)
			pd = obj.owner.data.primitivedata
			pd.radius1, pd.height = 1, 1
			obj.update()
		elif self.type == 'CONE':
			obj = Cone()
			obj.create(ctx)
			pd = obj.owner.data.primitivedata
			pd.radius1, pd.radius1, pd.height = 1, 0.5, 1
			obj.update()
		elif self.type == 'ICOSPHERE':
			obj = Icosphere()
			obj.create(ctx)
			pd = obj.owner.data.primitivedata
			pd.radius1 = 1
			obj.update()
		elif self.type == 'MESHER':
			obj = Mesher()
			obj.create(ctx)
			pd = obj.owner.data.primitivedata
			pd.radius1 = 1
			obj.update()
		elif self.type == 'MONKEY':
			obj = Monkey()
			obj.create(ctx)
			pd = obj.owner.data.primitivedata
			pd.radius1 = 1
			obj.update()
		elif self.type == 'OILTANK':
			obj = OilTank()
			obj.create(ctx)
			pd = obj.owner.data.primitivedata
			pd.radius1, pd.height, pd.thickness = 1, 3, 1
			obj.update()
		elif self.type == 'PLANE':
			obj = Plane()
			obj.create(ctx)
			pd = obj.owner.data.primitivedata
			pd.width, pd.length = 1, 1
			obj.update()
		elif self.type == 'PYRAMID':
			obj = Pyramid()
			obj.create(ctx)
			pd = obj.owner.data.primitivedata
			pd.width, pd.length, pd.height = 1, 1, 1
			obj.update()
		elif self.type == 'SPHERE':
			obj = Sphere()
			obj.create(ctx)
			pd = obj.owner.data.primitivedata
			pd.radius1 = 1
			obj.update()
		elif self.type == 'TEAPOT':
			obj = Teapot()
			obj.create(ctx)
			pd = obj.owner.data.primitivedata
			pd.radius1 = 1
			obj.update()
		elif self.type == 'TORUS':
			obj = Torus()
			obj.create(ctx)
			pd = obj.owner.data.primitivedata
			pd.radius1, pd.radius2 = 1, 0.5
			obj.update()
		elif self.type == 'TUBE':
			obj = Tube()
			obj.create(ctx)
			pd = obj.owner.data.primitivedata
			pd.radius1, pd.radius2 ,pd.height = 1, 0.5, 1
			obj.update()
		elif self.type == 'ARC':
			obj = Arc()
			obj.create(ctx)
			pd = obj.owner.data.primitivedata
			pd.radius1, pd.sfrom, pd.sto = 1, 0, 5
			obj.update()
		elif self.type == 'CIRCLE':
			obj = Circle()
			obj.create(ctx)
			pd = obj.owner.data.primitivedata
			pd.radius1 = 1
			obj.update()
		elif self.type == 'DONUT':
			obj = Donut()
			obj.create(ctx)
			pd = obj.owner.data.primitivedata
			pd.radius1, pd.radius2 = 1, 0.5
			obj.update()
		elif self.type == 'ELLIPSE':
			obj = Ellipse()
			obj.create(ctx)
			pd = obj.owner.data.primitivedata
			pd.width, pd.length = 1, 0.5
			obj.update()
		elif self.type == 'HELIX':
			obj = Helix()
			obj.create(ctx)
			pd = obj.owner.data.primitivedata
			pd.radius1, pd.radius2, pd.height = 1, 1, 1
			obj.update()
		elif self.type == 'NGON':
			obj = NGon()
			obj.create(ctx)
			pd = obj.owner.data.primitivedata
			pd.radius1 = 1
			obj.update()
		elif self.type == 'PROFILO':
			obj = Profilo()
			obj.create(ctx, "Angle")
			pd = obj.owner.data.primitivedata
			pd.width, pd.length, pd.thickness = 1, 1, 0.2
			obj.update()
		elif self.type == 'RECTANGLE':
			obj = Rectangle()
			obj.create(ctx)
			pd = obj.owner.data.primitivedata
			pd.width, pd.length = 1, 1
			obj.update()
		elif self.type == 'STAR':
			obj = Star()
			obj.create(ctx)
			pd = obj.owner.data.primitivedata
			pd.radius1, pd.radius2 = 1, 0.5
			obj.update()
		ctx.active_object.location = ctx.scene.cursor.location
		# bpy.ops.primitive.edit('INVOKE_DEFAULT')
		return {'FINISHED'}

	def invoke(self,ctx,event):
		wm = ctx.window_manager
		return wm.invoke_props_dialog(self)

classes = [Object_OT_Create]

def register_create():
	bpy.utils.register_class(Object_OT_Create)

def unregister_create():
	bpy.utils.unregister_class(Object_OT_Create)

if __name__ == "__main__":
	register_create()