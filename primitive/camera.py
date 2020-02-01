import bpy
from primitive.primitive import CreatePrimitive
from bsmax.actions import set_create_target, delete_objects

class Camera:
	def __init__(self):
		self.finishon = 2
		self.owner = None
		self.target = None
	def reset(self):
		self.__init__()
	def abort(self):
		delete_objects([self.owner])

class BsMax_OT_CreateCamera(CreatePrimitive):
	bl_idname="bsmax.createcamera"
	bl_label="Camera Free/Target (Create)"
	subclass = Camera()

	def create(self, ctx, clickpoint):
		bpy.ops.object.camera_add(align='WORLD', location=clickpoint.view)
		self.subclass.owner = ctx.active_object
		self.subclass.owner.rotation_euler = clickpoint.orient
	def update(self, ctx, clickcount, dimantion):
		if clickcount == 1:
			if self.drag and self.subclass.target == None:
				self.subclass.target = set_create_target(self.subclass.owner, None)
			self.subclass.target.location = dimantion.view
	def finish(self):
		pass

def camera_cls(register):
	c = BsMax_OT_CreateCamera
	if register: bpy.utils.register_class(c)
	else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	camera_cls(True)

__all__ = ["camera_cls"]