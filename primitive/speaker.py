import bpy
from primitive.primitive import CreatePrimitive
from bsmax.actions import delete_objects

class Speaker:
	def __init__(self):
		self.finishon = 2
		self.owner = None
	def reset(self):
		self.__init__()
	def abort(self):
		delete_objects([self.owner])

class BsMax_OT_CreateSpeaker(CreatePrimitive):
	bl_idname="bsmax.createspeaker"
	bl_label="Speaker (Create)"
	subclass = Speaker()

	def create(self, ctx, clickpoint):
		bpy.ops.object.speaker_add(location=clickpoint.view)
		self.subclass.owner = ctx.active_object
		self.subclass.owner.rotation_euler = clickpoint.orient
	def update(self, clickcount, dimantion):
		if self.drag:
			self.subclass.owner.location = dimantion.view
	def finish(self):
		pass

def speaker_cls(register):
	c = BsMax_OT_CreateSpeaker
	if register: bpy.utils.register_class(c)
	else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	speaker_cls(True)

__all__ = ["speaker_cls"]