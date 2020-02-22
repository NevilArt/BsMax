import bpy
from bpy.types import Menu
from bsmax.state import is_object_mode

class BsMax_MT_Animation_Tools(Menu):
	bl_idname = "BSMAX_MT_animationtools"
	bl_label = "Animation"
	bl_context = "objectmode"

	@classmethod
	def poll(self, ctx):
		return is_object_mode(ctx)

	def draw(self, ctx):
		layout=self.layout
		layout.operator("animation.linkconstraint",text="Parent to Active Object",icon="LINKED").linkto = 'OBJECT'
		layout.operator("animation.linkconstraint",text="Parent to World",icon="UNLINKED").linkto = 'WORLD'

def animation_menu(self, ctx):
	self.layout.menu("BSMAX_MT_animationtools")

def menu_cls(register):
	classes = [BsMax_MT_Animation_Tools]
	if register:
		[bpy.utils.register_class(c) for c in classes]
		bpy.types.VIEW3D_MT_editor_menus.append(animation_menu)
	else:
		[bpy.utils.unregister_class(c) for c in classes]
		bpy.types.VIEW3D_MT_editor_menus.remove(animation_menu)

if __name__ == '__main__':
	menu_cls(True)

__all__ = ["menu_cls"]