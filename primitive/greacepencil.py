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
from bpy.props import EnumProperty
from primitive.primitive import Draw_Primitive, Primitive_Public_Class
from bsmax.actions import delete_objects



class GreacePencil(Primitive_Public_Class):
	def init(self):
		self.finishon = 2
		self.owner = None

	def create(self, ctx, gpencil_type):
		bpy.ops.object.gpencil_add(location=(0,0,0),type=gpencil_type)
		self.owner = ctx.active_object
		self.data = self.owner.data

	def abort(self):
		delete_objects([self.owner])
	


class Create_OT_GreacePencil(Draw_Primitive):
	bl_idname="create.greacepencil"
	bl_label="GreacePencil"
	subclass = GreacePencil()
	use_gride = True
	use_single_click = True

	gpencil_type: EnumProperty(name='Type',default='EMPTY',
		items =[('EMPTY','Blank',''),('STROKE','Stroke',''),('MONKEY','Monkey','')])

	def create(self, ctx):
		self.subclass.create(ctx, self.gpencil_type)
		owner = self.subclass.owner
		owner.location = self.gride.location
		owner.rotation_euler = self.gride.rotation
		owner.rotation_euler.x -= 1.5708

	def update(self, ctx, clickcount, dimantion):
		if clickcount == 1:
			owner = self.subclass.owner
			owner.location = dimantion.center
			r = dimantion.radius/2
			owner.scale = (r,r,r)



def register_greacepencil():
	bpy.utils.register_class(Create_OT_GreacePencil)

def unregister_greacepencil():
	bpy.utils.unregister_class(Create_OT_GreacePencil)

if __name__ == "__main__":
	register_greacepencil()