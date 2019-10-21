import bpy
from bpy.types import Operator
from bsmax.state import is_objects_selected
from bsmax.mouse import ClickPoint, get_click_point_info
from bsmax.math import get_axis_constraint

class BsMax_OT_Drag_Clone_Object(Operator):
	bl_idname = "bsmax.dragclone"
	bl_label = "Drag Clone (Object)"

	point_a = None
	point_b = None

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def modal(self, ctx, event):
		x, y = event.mouse_region_x, event.mouse_region_y
		cp = get_click_point_info(x, y, ctx)
		if event.type == 'LEFTMOUSE':
			if event.value == 'PRESS':
				self.point_a = cp.view
			if event.value =='RELEASE':
				return {'CANCELLED'}
		# get direction
		if event.type == 'MOUSEMOVE':
			if self.point_a != None:
				self.point_b = cp.view
				tr = get_axis_constraint(self.point_a, self.point_b)
				print(tr)
		# get active tool
		# set action
		if event.type in {'RIGHTMOUSE', 'ESC'}:
			return {'CANCELLED'}
		return {'RUNNING_MODAL'}

	def invoke(self, ctx, event):
		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}

def dragclone_cls(register):
	classes = [BsMax_OT_Drag_Clone_Object]
	for c in classes:
		if register: bpy.utils.register_class(c)
		else: bpy.utils.unregister_class(c)
	return classes

if __name__ == '__main__':
	dragclone_cls(True)

__all__ = ["dragclone_cls"]