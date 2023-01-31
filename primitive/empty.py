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
from bpy.props import EnumProperty
from primitive.primitive import Draw_Primitive, Primitive_Public_Class



class Empty(Primitive_Public_Class):
	def init(self):
		self.finishon = 2
		self.owner = None

	def abort(self):
		bpy.ops.object.delete({'selected_objects': [self.owner]})



class Create_OT_Empty(Draw_Primitive):
	bl_idname="create.empty"
	bl_label="Empty"
	subclass = Empty()
	use_gride = True
	use_single_click = True

	empty_type: EnumProperty(name='Type',default='PLAIN_AXES',
		items =[('PLAIN_AXES','Point axis',''),('ARROWS','Arrows',''),
				('SINGLE_ARROW','Single Arrow',''),('CIRCLE','Circle',''),
				('CUBE','Cube',''),('SPHERE','Sphere',''),
				('CONE','Cone',''),('IMAGE','Image','')])
	depth: EnumProperty(name='Depth',default='DEFAULT',
		items =[('DEFAULT','Default',''),('FRONT','Front',''),('BACK','Back','')])

	def create(self, ctx):
		bpy.ops.object.empty_add(type=self.empty_type,location=self.gride.location)
		self.subclass.owner = ctx.active_object
		self.subclass.owner.rotation_euler = self.gride.rotation
		if self.empty_type == "IMAGE":
			self.subclass.owner.empty_image_depth = self.depth

	def update(self, ctx, clickcount, dimension):
		if clickcount == 1:
			self.subclass.owner.empty_display_size = dimension.radius



class Create_OT_Image(Operator):
	bl_idname="create.image"
	bl_label="Image"
	bl_options={"UNDO"}
	image_type: EnumProperty(name='Type',default='REFERENCE',
		items =[('REFERENCE','Reference',''),('BACKGROUND','Background','')])

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		if self.image_type == "REFERENCE":
			bpy.ops.create.empty('INVOKE_DEFAULT',empty_type="IMAGE",depth="DEFAULT")
		else:
			bpy.ops.create.empty('INVOKE_DEFAULT',empty_type="IMAGE",depth="BACK")
		return {'FINISHED'}



classes = [Create_OT_Empty, Create_OT_Image]

def register_empty():
	for c in classes:
		bpy.utils.register_class(c)

def unregister_empty():
	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == "__main__":
	register_empty()