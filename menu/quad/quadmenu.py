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
from bpy.props import StringProperty
from .q_refrence import QuadMenuRef
from .q_menu import QuadMenu
from .menu_standard import * # all functions started with "get_" came frome here

class BsMax_OT_View3D_QuadMenu(Operator):
	bl_idname = "bsmax.view3dquadmenue"
	bl_label = "Viewport QuadMenu"
	x, y = 0, 0
	handler = None
	controllers = []
	menu: StringProperty(name = 'default')
	space: StringProperty(name = 'View3D')
	#TODO remove space just make it auto
	#'View3D', 'UVEditor', 'GraphEditor', 'DopeSheetEditor', 'NodeEditor'
	#ClipEditor, ImageEditor, NLA, NodeEditorPath, Outliner3D

	def modal(self, ctx, event):
		if ctx.area:
			ctx.area.tag_redraw()
		if event.type == 'MOUSEMOVE':
			self.update(event.mouse_region_x, event.mouse_region_y)
		if event.type == 'LEFTMOUSE':
			if event.value == 'RELEASE':
				self.click(event.mouse_region_x, event.mouse_region_y)
		if event.type == 'RIGHTMOUSE':
			if event.value == 'PRESS':
				if self.handler != None:
					QuadMenuRef.finish = True

		# resize the quad menu
		# if event.type == 'NUMPAD_MINUS':
		# 	if event.value == 'PRESS':
		# 		if QuadMenuRef.size > 15:
		# 			QuadMenuRef.size -= 1
		# if event.type == 'NUMPAD_PLUS':
		# 	if event.value == 'PRESS':
		# 		if QuadMenuRef.size < 60:
		# 			QuadMenuRef.size += 1

		if event.type in {'ESC'} or QuadMenuRef.finish:
			self.unregister_handler()
			return {'CANCELLED'}
		return {'RUNNING_MODAL'}

	def update(self, x, y):
		for c in self.controllers:
			c.mousehover(x, y, False)

	def click(self, x, y):
		for c in self.controllers:
			c.mousehover(x, y, True)
		QuadMenuRef.execute()

	def draw(self, ctx):
		for c in self.controllers:
			c.update()
		for c in self.controllers:
			c.update_lbl()

	def SpaceFromName(self, name):
		if name == 'View3D':
			return bpy.types.SpaceView3D
		elif name == 'UVEditor':
		    return bpy.types.SpaceUVEditor
		elif name == 'GraphEditor':
			return bpy.types.SpaceGraphEditor
		elif name == 'DopeSheetEditor':
			return bpy.types.SpaceDopeSheetEditor
		elif name == 'NodeEditor':
			return bpy.types.SpaceNodeEditor
		return None

	def register_handler(self, ctx):
		space = self.SpaceFromName(self.space)
		if space != None:
			self.handler = space.draw_handler_add(self.draw,tuple([ctx]),
												'WINDOW','POST_PIXEL')    

	def unregister_handler(self):
		space = self.SpaceFromName(self.space)
		if space != None:
			space.draw_handler_remove(self.handler, "WINDOW")
				
	def create(self, ctx):
		self.controllers.clear()
		QuadMenuRef.finish = False
		Menus = []
		########################################
		# all this function are "from .menu_standard import *"
		if self.menu == 'default': # RMB
			Menus.append(get_view3d_transform(ctx))
			Menus.append(get_view3d_display(ctx))
			Menus.append(get_view3d_tool1(ctx))
			Menus.append(get_view3d_tool2(ctx))
		elif self.menu == 'create': # Ctrl + RMB
			Menus.append(get_view3d_transform(ctx))
			Menus.append(get_view3D_create(ctx))
			Menus.append(get_view3d_tool1(ctx))
			Menus.append(get_view3d_tool2(ctx))
		elif self.menu == 'viewport': # V
			Menus.append(get_view3D_viewport(ctx))
			Menus.append(get_view3d_camera(ctx))
		elif self.menu == 'coordinate': # Alt + RMB
			Menus.append(get_view3d_set(ctx))
			Menus.append(get_view3d_coordinates(ctx))
			Menus.append(get_view3d_transform2(ctx))
			Menus.append(get_view3d_pose(ctx))
		elif self.menu == 'snap': # Shift + RMB
			Menus.append(get_view3d_snap_toggles(ctx))
			Menus.append(get_view3d_snap_override(ctx))
			Menus.append(get_view3d_snap_options(ctx))
		elif self.menu == 'render': # Alt + Ctrl + RMB
			Menus.append(get_view3d_rendering_properties(ctx))
			Menus.append(get_view3d_render(ctx))
			Menus.append(get_view3d_rendering_tools(ctx))
		elif self.menu == 'Selection': # Ctrl + Shift + RMB
			Menus.append(get_view3d_selection1(ctx))
			Menus.append(get_view3d_selection2(ctx))
			Menus.append(get_view3d_selection3(ctx))
			Menus.append(get_view3d_selection4(ctx))
		elif self.menu == 'fx': # Alt + Shift + RMB
			Menus.append(get_view3d_fx_tools(ctx))
			Menus.append(get_view3d_fx_objects(ctx))
			Menus.append(get_view3d_fx_simulation(ctx))
			Menus.append(get_view3d_fx_constraints(ctx))
		elif self.menu == 'custom': # Alt + Ctrl + Shift + RMB
			Menus = []
		elif self.menu == 'UV': # RMB
			Menus.append(get_uv_editor_transform(ctx))
			Menus.append(get_uv_editor_display(ctx))
			Menus.append(get_uv_editor_tools1(ctx))
			Menus.append(get_uv_editor_tools2(ctx))
		elif self.menu == 'TrackView': # RMB
			Menus.append(get_grapheditor_trackview(ctx))
		##############################################
		for M in Menus:
			lbl, items, index = M
			if len(items) > 0:
				NewQuad = QuadMenu(self.x, self.y, lbl, items, index)
				self.controllers.append(NewQuad)

	def invoke(self, ctx, event):
		QuadMenuRef.size = qmd.get_scale() * 15
		self.x = event.mouse_region_x - int(QuadMenuRef.size / 2)
		self.y = event.mouse_region_y + int(QuadMenuRef.size / 2)
		self.create(ctx)
		self.register_handler(ctx)
		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}

class Quad_Menu_Data:
	preferences = None
	def get_scale(self):
		if self.preferences == None:
			return 1
		else:
			return self.preferences.menu_scale

qmd = Quad_Menu_Data()

def register_quadmenu(preferences):
	qmd.preferences = preferences
	bpy.utils.register_class(BsMax_OT_View3D_QuadMenu)

def unregister_quadmenu():
	bpy.utils.unregister_class(BsMax_OT_View3D_QuadMenu)