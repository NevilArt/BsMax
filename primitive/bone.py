import bpy
from primitive.primitive import CreatePrimitive, PrimitiveGeometryClass
from bsmax.actions import delete_objects
from bsmax.math import get_axis_constraint

class Armature(PrimitiveGeometryClass):
	def __init__(self):
		self.classname = "Armature"
		self.finishon = 0 # infinit
		self.owner = None
		self.data = None
		self.bones = []
	def reset(self):
		self.__init__()
	def create(self, ctx):
		bpy.ops.object.armature_add(enter_editmode=False, location=(0, 0, 0))
		self.owner = ctx.active_object
		self.data = self.owner.data
	def update(self):
		pass
	def abort(self):
		bpy.ops.object.mode_set(mode='EDIT', toggle=False)
		edit_bones = self.data.edit_bones
		if len(edit_bones) > 0:
			edit_bones.remove(edit_bones[-1])
		for i in range(len(edit_bones) - 1):
			# TODO find a better way to replace with this ugly code
			bpy.ops.armature.select_all(action='DESELECT')
			edit_bones.active = edit_bones[i]
			edit_bones[i + 1].select = True
			bpy.ops.armature.parent_set(type='CONNECTED')
			
		bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
		if len(self.data.bones) == 0:
			delete_objects([self.owner])
		self.reset()

class BsMax_OT_CreateBone(CreatePrimitive):
	bl_idname="bsmax.createbone"
	bl_label="Bone (Create)"
	subclass = Armature()
	lastclick = 1
	startpoint = None

	def create(self, ctx, clickpoint):
		self.usedkeys += ['LEFT_SHIFT', 'RIGHT_SHIFT', 'BACK_SPACE']
		self.requestkey = ['BACK_SPACE']
		self.subclass.create(ctx)
		self.startpoint = clickpoint.view
		bpy.ops.object.mode_set(mode='EDIT', toggle=False)
		edit_bones = self.subclass.data.edit_bones 
		for bone in edit_bones:
			edit_bones.remove(bone)

	def update(self, clickcount, dimantion):
		bpy.ops.object.mode_set(mode='EDIT', toggle=False)
		edit_bones = self.subclass.data.edit_bones

		if self.shift:
			if len(edit_bones) > 0:
				dimantion.view = get_axis_constraint(edit_bones[-1].head, dimantion.view)

		if len(edit_bones) > 0:
			edit_bones[-1].tail = dimantion.view
		if clickcount != self.lastclick:
			newbone = edit_bones.new('Bone')
			if len(edit_bones) == 1:
				newbone.head = self.startpoint
			else:
				newbone.head = edit_bones[-2].tail
			newbone.tail = dimantion.view
			self.lastclick = clickcount

	def event(self, event, value):
		if event == 'BACK_SPACE':
			if value == 'RELEASE':
				bpy.ops.object.mode_set(mode='EDIT', toggle=False)
				edit_bones = self.subclass.data.edit_bones
				if len(edit_bones) > 1:
					edit_bones.remove(edit_bones[-1])
	def finish(self):
		pass

def bone_cls(register):
	c = BsMax_OT_CreateBone
	if register: bpy.utils.register_class(c)
	else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	bone_cls(True)

__all__ = ["bone_cls"]