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



class Text(Primitive_Public_Class):
	def init(self):
		self.finishon = 2
		self.owner = None

	def create(self, ctx):
		bpy.ops.object.text_add()
		self.owner = ctx.active_object
	
	def abort(self):
		delete_objects([self.owner])



class Create_OT_Text(Draw_Primitive):
	bl_idname="create.text"
	bl_label="Text (Create)"
	subclass = Text()
	use_gride = True
	use_single_click = True

	fill_mode: EnumProperty( name = 'Fill Mode',  default = 'NONE',
		items =[('NONE', 'None', ''),
				('FRONT', 'Front', ''),
				('BACK', 'Back', ''),
				('BOTH', 'Both', '')])

	def create(self, ctx):
		self.subclass.create(ctx)
		owner = self.subclass.owner
		owner.data.fill_mode = self.fill_mode
		owner.location = self.gride.location
		owner.rotation_euler = self.gride.rotation
	
	def update(self, ctx, clickcount, dimantion):
		if clickcount == 1:
			self.subclass.owner.data.size = dimantion.radius



def register_text():
	bpy.utils.register_class(Create_OT_Text)

def unregister_text():
	bpy.utils.unregister_class(Create_OT_Text)

if __name__ == "__main__":
	register_text()