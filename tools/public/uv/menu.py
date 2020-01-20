import bpy
from bpy.types import Menu

class BsMax_MT_UV_Edit(Menu):
	bl_idname = "BSMAX_MT_uvedit"
	bl_label = "Edit"

	def draw(self, ctx):
		layout=self.layout
		if ctx.space_data.show_uvedit:
			layout.operator("uv.turn",text="-90",icon="LOOP_BACK").ccw = False
			layout.operator("uv.turn",text="+90",icon="LOOP_FORWARDS").ccw = True
			#layout.separator()
		# elif ctx.space_data.show_uvedit:# image editor
		# 	layout.operator("image.turn",text="-90",icon="LOOP_BACK").ccw = False
		# 	layout.operator("image.turn",text="+90",icon="LOOP_FORWARDS").ccw = True

def uv_edit_menu(self, ctx):
	self.layout.menu("BSMAX_MT_uvedit")

def menu_cls(register):
	c = BsMax_MT_UV_Edit
	if register:
		bpy.utils.register_class(c)
		bpy.types.MASK_MT_editor_menus.append(uv_edit_menu)
	else:
		bpy.types.MASK_MT_editor_menus.remove(uv_edit_menu)
		bpy.utils.unregister_class(c)

if __name__ == '__main__':
	menu_cls(True)

__all__ = ["menu_cls"]