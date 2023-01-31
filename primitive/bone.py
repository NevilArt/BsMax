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

from math import atan2

from primitive.primitive import Primitive_Geometry_Class, Draw_Primitive
from bsmax.math import get_axis_constraint



class Armature(Primitive_Geometry_Class):
	def init(self):
		self.classname = "Armature"
		self.finishon = 0 # infinit
		# self.bones = []

	def create(self, ctx):
		bpy.ops.object.armature_add(enter_editmode=False, location=(0, 0, 0))
		self.owner = ctx.active_object
		self.data = self.owner.data

	def abort(self):
		bpy.ops.object.mode_set(mode='EDIT', toggle=False)
		edit_bones = self.data.edit_bones

		# remove none confirmed bone
		if len(edit_bones) > 0:
			edit_bones.remove(edit_bones[-1])

		for i in range(len(edit_bones) - 1):
			# TODO need to a clear method
			bpy.ops.armature.select_all(action='DESELECT')
			edit_bones.active = edit_bones[i]
			edit_bones[i + 1].select = True
			bpy.ops.armature.parent_set(type='CONNECTED')
			
		bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

		# remove armature if no bone created
		if len(self.data.bones) == 0:
			bpy.ops.object.delete({'selected_objects': [self.owner]})

		self.reset()



def get_roll(bone):
	""" Get edit bone and return corrective roll angle
		args:
			bone: edit bone
		return:
			float roll angle
	"""
	a = bone.head.x - bone.tail.x
	b = bone.head.z - bone.tail.z
	return atan2(a, b)



class Create_OT_Bone(Draw_Primitive):
	bl_idname="create.bone"
	bl_label="Bone"
	subclass = Armature()
	use_gride = False
	lastclick = 1
	startpoint = None

	def create(self, ctx):
		self.used_keys += ['LEFT_SHIFT', 'RIGHT_SHIFT', 'BACK_SPACE']
		self.request_key = ['BACK_SPACE']

		self.subclass.create(ctx)
		self.startpoint = self.gride.location

		bpy.ops.object.mode_set(mode='EDIT', toggle=False)
		edit_bones = self.subclass.data.edit_bones 

		# remove original bone
		for bone in edit_bones:
			edit_bones.remove(bone)

	def update(self, ctx, clickcount, dimension):
		bpy.ops.object.mode_set(mode='EDIT', toggle=False)
		edit_bones = self.subclass.data.edit_bones

		if self.shift:
			if len(edit_bones) > 0:
				dimension.end = get_axis_constraint(edit_bones[-1].head, dimension.end)

		if len(edit_bones) > 0:
			last_bone = edit_bones[-1]
			last_bone.tail = dimension.end
			last_bone.roll = get_roll(last_bone)

		if clickcount != self.lastclick:
			newbone = edit_bones.new('Bone')

			if len(edit_bones) == 1:
				newbone.head = self.startpoint

			else:
				newbone.head = edit_bones[-2].tail
			newbone.tail = dimension.end
			self.lastclick = clickcount

	def event(self, event, value):
		if event == 'BACK_SPACE':
			if value == 'RELEASE':
				bpy.ops.object.mode_set(mode='EDIT', toggle=False)
				edit_bones = self.subclass.data.edit_bones

				if len(edit_bones) > 1:
					edit_bones.remove(edit_bones[-1])



def register_bone():
	bpy.utils.register_class(Create_OT_Bone)

def unregister_bone():
	bpy.utils.unregister_class(Create_OT_Bone)

if __name__ == "__main__":
	register_bone()