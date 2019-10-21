import bpy
from bpy.types import Operator
from bpy.props import BoolProperty

class BsMax_OT_ScaleIcons(Operator):
	bl_idname = "filebrowser.scaleicons"
	bl_label = "Scale Icons"
	up: BoolProperty(name="scaleup",default=True)
	
	@classmethod
	def poll(self, ctx):
		return ctx.area.ui_type == 'FILE_BROWSER'

	def execute(self, ctx):
		params = ctx.space_data.params
		if self.up:
			if params.display_type == 'THUMBNAIL':
				params.display_type = 'LIST_SHORT'
			elif params.display_type == 'LIST_LONG':
				params.display_type = 'THUMBNAIL'
			elif params.display_type == 'LIST_SHORT':
				params.display_type = 'LIST_LONG'
		else:
			if params.display_type == 'THUMBNAIL':
				params.display_type = 'LIST_LONG'
			elif params.display_type == 'LIST_LONG':
				params.display_type = 'LIST_SHORT'
			elif params.display_type == 'LIST_SHORT':
				params.display_type = 'THUMBNAIL'
		return{"FINISHED"}

def filebrowser_cls(register):
	classes = [BsMax_OT_ScaleIcons]
	for c in classes:
		if register: bpy.utils.register_class(c)
		else: bpy.utils.unregister_class(c)
	return classes

if __name__ == '__main__':
	filebrowser_cls(True)

__all__ = ["filebrowser_cls"]
