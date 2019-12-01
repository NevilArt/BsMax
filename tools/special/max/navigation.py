import bpy
from bpy.types import Operator

class BsMax_OT_MaxNavigation(Operator):
	bl_idname = "bsmax.maxnavigation"
	bl_label = "Max Navigation"
	alt = False
	ctrl = False
	mmb = False

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def action(self):
		print(self.mmb, self.alt, self.ctrl)
		if self.mmb and not self.alt and not self.ctrl:
			bpy.ops.view3d.move('INVOKE_DEFAULT')
		if self.mmb and self.alt and not self.ctrl:
			bpy.ops.view3d.rotate('INVOKE_DEFAULT')
		if self.mmb and self.alt and self.ctrl:
			bpy.ops.view3d.zoom('INVOKE_DEFAULT')

	def modal(self,ctx,event):
		if not event.type in ['MIDDLEMOUSE','LEFT_CTRL','LEFT_ALT','RIGHT_CTRL','RIGHT_ALT']: 
			return {'PASS_THROUGH'}
		print(event.type, event.value)

		if event.type == 'MIDDLEMOUSE':
			if event.value in {'PRESS','CLICK_DRAG'}:
				self.mmb = True
			elif event.value == 'RELEASE':
				self.mmb = False

		if event.type in {'LEFT_ALT','RIGHT_ALT'}:
			if event.value in {'PRESS','CLICK_DRAG'}:
				self.alt = True
			elif event.value == 'RELEASE':
				self.alt = False

		if event.type in {'LEFT_CTRL','RIGHT_CTRL'}:
			if event.value in {'PRESS','CLICK_DRAG'}:
				self.ctrl = True
			elif event.value == 'RELEASE':
				self.ctrl = False

		self.action()
		#return {'CANCELLED'}
		return {'RUNNING_MODAL'}
	def invoke(self,ctx,event):
		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}

def navigation_cls(register):
	classes = [BsMax_OT_MaxNavigation]
	for c in classes:
		if register: bpy.utils.register_class(c)
		else: bpy.utils.unregister_class(c)
	return classes

if __name__ == '__main__':
	navigation_cls(True)

__all__ = ["navigation_cls"]