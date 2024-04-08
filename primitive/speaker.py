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
from primitive.primitive import Draw_Primitive, Primitive_Public_Class


class Speaker(Primitive_Public_Class):
	def init(self):
		self.finishon = 2
		self.owner = None


class Create_OT_Speaker(Draw_Primitive):
	bl_idname="create.speaker"
	bl_label="Speaker"
	subclass = Speaker()
	use_single_click = True

	def create(self, ctx):
		bpy.ops.object.speaker_add(location=self.gride.location)
		self.subclass.owner = ctx.active_object
		self.subclass.owner.rotation_euler = self.gride.rotation

	def update(self, ctx, clickcount, dimension):
		if self.drag:
			self.subclass.owner.location = dimension.end


def register_speaker():
	bpy.utils.register_class(Create_OT_Speaker)


def unregister_speaker():	
	bpy.utils.unregister_class(Create_OT_Speaker)


if __name__ == "__main__":
	register_speaker()