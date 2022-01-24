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
from primitive.primitive import Draw_Primitive
from bsmax.actions import delete_objects



class Effector:
	def __init__(self):
		self.finishon = 2
		self.owner = None

	def reset(self):
		self.__init__()

	def update(self):
		pass

	def abort(self):
		delete_objects([self.owner])



class Create_OT_Effector(Draw_Primitive):
	bl_idname="create.effector"
	bl_label="Effector"
	subclass = Effector()
	use_single_click = True

	effector_type: EnumProperty(name='Type',default='FORCE',
		items =[('FORCE','Force',''),('WIND','Wind',''),
				('VORTEX','Vortex',''),('MAGNET','Magnet',''),
				('HARMONIC','Harmonic',''),('CHARGE','Charge',''),
				('LENNARDJ','Lennardj',''),('TEXTURE','Texture',''),
				('GUIDE','Guide',''),('BOID','Boid',''),('TURBULENCE','Turbulence',''),
				('DRAG','Drag',''),('SMOKE','Smoke','')])

	def create(self, ctx):
		bpy.ops.object.effector_add(type=self.effector_type,
			radius=1, location=self.gride.location)
		self.subclass.owner = ctx.active_object
		self.subclass.owner.rotation_euler = self.gride.rotation

	def update(self, ctx, clickcount, dimantion):
		if clickcount == 1:
			self.subclass.owner.empty_display_size = dimantion.radius

	def finish(self):
		pass



def register_effector():
	bpy.utils.register_class(Create_OT_Effector)

def unregister_effector():
	bpy.utils.unregister_class(Create_OT_Effector)

if __name__ == "__main__":
	register_effector()