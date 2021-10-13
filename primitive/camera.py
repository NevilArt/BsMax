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
from math import pi
from primitive.primitive import CreatePrimitive
from primitive.gride import Draw_Primitive
from bsmax.actions import delete_objects
from bsmax.math import get_distance

class Camera:
	def __init__(self):
		self.finishon = 2
		self.owner = None
		self.target = None
	def reset(self):
		self.__init__()
	def abort(self):
		delete_objects([self.owner])
		if self.target:
			delete_objects([self.target])



class Create_OT_Camera(Draw_Primitive):
	bl_idname="create.camera"
	bl_label="Camera Free/Target"
	subclass = Camera()
	use_single_click = True

	def create(self, ctx):
		bpy.ops.object.camera_add(align='WORLD', location=self.gride.location)
		self.subclass.owner = ctx.active_object
		self.subclass.owner.rotation_euler = self.gride.rotation
		self.subclass.owner.rotation_euler.x += pi/2

	def update(self, ctx, clickcount, dimantion):
		if clickcount == 1:
			if self.drag and self.subclass.target == None:
				bpy.ops.object.select_all(action = 'DESELECT')
				self.subclass.owner.select_set(state = True)
				ctx.view_layer.objects.active = self.subclass.owner
				bpy.ops.camera.create_target()
				self.subclass.target = self.subclass.owner.constraints["Track To"].target

			self.subclass.target.location = dimantion.location

			size = get_distance(self.subclass.owner.location,self.subclass.target.location)/3
			self.subclass.owner.data.display_size = size
			self.subclass.target.empty_display_size = size / 10

	def finish(self):
		pass

def register_camera():
	bpy.utils.register_class(Create_OT_Camera)

def unregister_camera():
	bpy.utils.unregister_class(Create_OT_Camera)

if __name__ == "__main__":
	register_camera()