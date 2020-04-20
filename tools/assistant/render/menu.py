import bpy
from bpy.types import Menu
from bsmax.state import is_object_mode

class BsMax_MT_Render_Tools(Menu):
	bl_idname = "BSMAX_MT_rendertools"
	bl_label = "Render"
	bl_context = "objectmode"

	@classmethod
	def poll(self, ctx):
		return is_object_mode(ctx)

	def draw(self, ctx):
		layout=self.layout
		layout.operator("render.lightlister",text="Light Lister",icon='LIGHT_SUN')

def animation_menu(self, ctx):
	self.layout.menu("BSMAX_MT_rendertools")

def menu_cls(register):
	classes = [BsMax_MT_Render_Tools]
	if register:
		[bpy.utils.register_class(c) for c in classes]
		bpy.types.VIEW3D_MT_editor_menus.append(animation_menu)
	else:
		[bpy.utils.unregister_class(c) for c in classes]
		bpy.types.VIEW3D_MT_editor_menus.remove(animation_menu)

if __name__ == '__main__':
	menu_cls(True)

__all__ = ["menu_cls"]