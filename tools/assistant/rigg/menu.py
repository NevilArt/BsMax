import bpy
from bpy.types import Menu
from bsmax.state import is_object_mode

class BsMax_MT_rigg_tools(Menu):
	bl_idname = "BSMAX_MT_riggtools"
	bl_label = "Rigg"
	bl_context = "objectmode"

	@classmethod
	def poll(self, ctx):
		return is_object_mode(ctx)

	def draw(self, ctx):
		layout=self.layout
		layout.operator("bsmax.joystickcreator",icon="EVENT_O")
		layout.operator("bsmax.joystickshapekeyconnector",icon="LINK_BLEND")
		layout.operator("bsmax.eyetargetcreator",icon="HIDE_OFF")

def rigg_menu(self, ctx):
	self.layout.menu("BSMAX_MT_riggtools")

def menu_cls(register):
	classes = [BsMax_MT_rigg_tools]
	if register:
		[bpy.utils.register_class(c) for c in classes]
		bpy.types.VIEW3D_MT_editor_menus.append(rigg_menu)
	else:
		[bpy.utils.unregister_class(c) for c in classes]
		bpy.types.VIEW3D_MT_editor_menus.remove(rigg_menu)  

if __name__ == '__main__':
	menu_cls(True)

__all__ = ["menu_cls"]