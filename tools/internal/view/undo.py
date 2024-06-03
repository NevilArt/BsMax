############################################################################
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################################################

import bpy

from bpy.types import Operator
from mathutils import Matrix
from bpy.props import BoolProperty
from bpy.utils import register_class, unregister_class

# TODO undo redo in multi viewprts not works correctly


class ViewCash:
	area = None
	direction = []
	last = None
	index = 0
	changed = False


class VP:
	view = []
	record = True
	count = 100


def get_index(ctx):
	for i, v in enumerate(VP.view):
		if v.area == ctx.area:
			return i
	return None


def is_changed(a, b):
	for i in range(4):
		for j in range(4):
			if a[i][j] != b[i][j]:
				return True
	return False


def is_mouse_over(ctx, event):
	x, y = event.mouse_region_x, event.mouse_region_y
	ex, ey = ctx.area.width, ctx.area.height
	if 0 <= x <= ex and 0 <= y <= ey:
		return True
	return False


def record_navigation(ctx, event):
	index = get_index(ctx)

	if index == None:
		vc = ViewCash()
		vc.area = ctx.area
		vc.last = ctx.area.spaces.active.region_3d.view_matrix.copy()
		VP.view.append(vc)
		index = get_index(ctx)

	if is_mouse_over(ctx, event):
		current = ctx.area.spaces.active.region_3d.view_matrix.copy()
		state = is_changed(current, VP.view[index].last)
		if state:
			extera = (len(VP.view[index].direction) - 1) - VP.view[index].index

			for _ in range(extera):
				VP.view[index].direction.pop()
			VP.view[index].direction.append(current.copy())

			if len(VP.view[index].direction) > VP.count:
				VP.view[index].direction.pop(0)
			VP.view[index].index = len(VP.view[index].direction) - 1

		VP.view[index].last = current.copy()


class BsMax_OT_ViewUndoRedo(Operator):
	bl_idname = 'view.undoredo'
	bl_label = "View Undo/Redo"
	bl_description = ""
	bl_options = {'REGISTER', 'INTERNAL'}

	redo: BoolProperty(name="Redo", default=False) # type: ignore

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		index = get_index(ctx)
		if index:
			if self.redo:
				if VP.view[index].index < len(VP.view[index].direction):
					VP.view[index].index += 1
			else:
				if VP.view[index].index > 0:
					VP.view[index].index -= 1

			if 0 <= VP.view[index].index < len(VP.view[index].direction):
				dindix = VP.view[index].index
				v = Matrix(VP.view[index].direction[dindix])
				ctx.area.spaces.active.region_3d.view_matrix = v.copy()
				VP.view[index].last = v.copy()
				VP.record = False

		return{'FINISHED'}


class View3D_OT_MoveCover(Operator):
	bl_idname = 'view3d.movecover'
	bl_label = "Pan View (Cover)"
	bl_description = ""
	bl_options = {'REGISTER', 'INTERNAL'}

	@classmethod
	def poll(self,ctx):
		return ctx.area.type == 'VIEW_3D'

	def modal(self,ctx,event):
		x, y = event.mouse_region_x, event.mouse_region_y
		if self.x != x or self.y != y:
			record_navigation(ctx, event)
			bpy.ops.view3d.move('INVOKE_DEFAULT')
			self.x,self.y = x,y

		return {'CANCELLED'}

	def invoke(self,ctx,event):
		self.x, self.y = event.mouse_region_x, event.mouse_region_y
		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}


class View3D_OT_RotateCover(Operator):
	bl_idname = 'view3d.rotatecover'
	bl_label = "Rotate View (Cover)"
	bl_description = ""
	bl_options = {'REGISTER', 'INTERNAL'}

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def modal(self, ctx, event):
		x, y = event.mouse_region_x, event.mouse_region_y
		if self.x != x or self.y != y:
			record_navigation(ctx, event)
			bpy.ops.view3d.rotate('INVOKE_DEFAULT')
			self.x,self.y = x,y

		return {'CANCELLED'}

	def invoke(self, ctx, event):
		self.x, self.y = event.mouse_region_x, event.mouse_region_y
		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}


class View3D_OT_ZoomCover(Operator):
	bl_idname = 'view3d.zoomcover'
	bl_label = "Zoom View (Cover)"
	bl_description = ""
	bl_options = {'REGISTER', 'INTERNAL'}

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def modal(self, ctx, event):
		x, y = event.mouse_region_x, event.mouse_region_y
		if self.x != x or self.y != y:
			record_navigation(ctx, event)
			bpy.ops.view3d.zoom('INVOKE_DEFAULT')
			self.x,self.y = x,y

		return {'CANCELLED'}

	def invoke(self, ctx, event):
		self.x, self.y = event.mouse_region_x, event.mouse_region_y
		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}


class View3D_OT_ZoomInCover(Operator):
	bl_idname = 'view3d.zoomincover'
	bl_label = "Zoom In View (Cover)"
	bl_description = ""
	bl_options = {'REGISTER', 'INTERNAL'}

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def modal(self, ctx, event):
		record_navigation(ctx, event)
		bpy.ops.view3d.zoom('INVOKE_DEFAULT', delta=1)
		return {'CANCELLED'}

	def invoke(self, ctx, _):
		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}


class View3D_OT_ZoomOutCover(Operator):
	bl_idname = 'view3d.zoomoutcover'
	bl_label = "Zoom Out View (Cover)"
	bl_description = ""
	bl_options = {'REGISTER', 'INTERNAL'}

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def modal(self, ctx, event):
		record_navigation(ctx, event)
		bpy.ops.view3d.zoom('INVOKE_DEFAULT',delta=-1)
		return {'CANCELLED'}

	def invoke(self, ctx, event):
		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}


class View3D_OT_DollyCover(Operator):
	bl_idname = 'view3d.dollycover'
	bl_label = "Dolly View (Cover)"
	bl_description = ""
	bl_options = {'REGISTER', 'INTERNAL'}

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def modal(self, ctx, event):
		record_navigation(ctx, event)
		bpy.ops.view3d.dolly('INVOKE_DEFAULT')
		return {'CANCELLED'}

	def invoke(self, ctx, _):
		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}


def view_undorido_menu(self, ctx):
	layout = self.layout
	layout.operator('view.undoredo', text="View Undo").redo=False
	layout.operator('view.undoredo', text="View Redo").redo=True
	layout.separator()


classes = {
	BsMax_OT_ViewUndoRedo,
	View3D_OT_MoveCover,
	View3D_OT_RotateCover,
	View3D_OT_ZoomCover,
	View3D_OT_ZoomInCover,
	View3D_OT_ZoomOutCover,
	View3D_OT_DollyCover
}


def register_undo(preferences):
	for cls in classes:
		register_class(cls)

	if preferences.view_undo:
		bpy.types.VIEW3D_MT_view.prepend(view_undorido_menu)


def unregister_undo():
	try: # temprary solution
		if view_undorido_menu in bpy.types.VIEW3D_MT_view:
			bpy.types.VIEW3D_MT_view.remove(view_undorido_menu)
	except:
		pass

	for cls in classes:
		unregister_class(cls)


if __name__ == '__main__':
	pass
	# register_undo()