import bpy
from bpy.props import EnumProperty
from primitive.primitive import CreatePrimitive
from bsmax.actions import delete_objects

class Text:
	def __init__(self):
		self.finishon = 2
		self.owner = None
	def reset(self):
		self.__init__()
	def create(self, ctx):
		bpy.ops.object.text_add()
		self.owner = ctx.active_object
	def abort(self):
		delete_objects([self.owner])

class BsMax_OT_CreateText(CreatePrimitive):
	bl_idname="bsmax.createtext"
	bl_label="Text (Create)"
	subclass = Text()

	fill_mode: EnumProperty( name = 'Fill Mode',  default = 'NONE',
		items =[('NONE', 'None', ''),
				('FRONT', 'Front', ''),
				('BACK', 'Back', ''),
				('BOTH', 'Both', '')])

	def create(self, ctx, clickpoint):
		self.subclass.create(ctx)
		owner = self.subclass.owner
		owner.location = clickpoint.view
		owner.data.fill_mode = self.fill_mode
		owner.rotation_euler = clickpoint.orient
	def update(self, clickcount, dimantion):
		if clickcount == 1:
			self.subclass.owner.data.size = dimantion.radius
	def finish(self):
		pass

def text_cls(register):
	c = BsMax_OT_CreateText
	if register: bpy.utils.register_class(c)
	else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	text_cls(True)

__all__ = ["text_cls"]