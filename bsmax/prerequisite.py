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
# 2024/04/19

from bpy.utils import register_class, unregister_class
from bpy.types import Menu


class BsMax_MT_View3D_tools(Menu):
	bl_idname = 'BSMAX_MT_view3d_tools'
	bl_label = "Tools"

	# @classmethod
	# def poll(self, ctx):
	# 	return ctx.mode == 'OBJECT'
	
	def draw(self, _):
		pass


class BsMax_MT_Compositor_tools(Menu):
	bl_idname = 'BSMAX_MT_compositor_tools'
	bl_label = "Tools"

	# @classmethod
	# def poll(self, ctx):
	# 	return ctx.mode == 'OBJECT'

	def draw(self, _):
		pass


class BsMax_MT_View3D_Create(Menu):
	bl_idname = 'BSMAX_MT_create_menu'
	bl_label = "Create"
	bl_context = "objectmode"

	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'OBJECT'

	def draw(self, _):
		pass

class BsMax_MT_View3D_Copy(Menu):
	bl_idname = 'BSMAX_MT_view3d_copy'
	bl_label = "Copy"
	bl_description = "Copy"

	# @classmethod
	# def poll(self, ctx):
	# 	return ctx.mode == 'OBJECT'

	def draw(self, _):
		self.layout.operator(
			'view3d.copybuffer', text="Object", icon='OBJECT_DATA'
		)


class BsMax_MT_View3D_Paste(Menu):
	bl_idname = 'BSMAX_MT_view3d_paste'
	bl_label = "Paste"
	bl_description = "Paste"

	# @classmethod
	# def poll(self, ctx):
	# 	return ctx.mode == 'OBJECT'

	def draw(self, _):
		self.layout.operator(
			'view3d.pastebuffer', text="Object", icon='OBJECT_DATA'
		)


classes = {
	BsMax_MT_View3D_tools,
	BsMax_MT_Compositor_tools,
	BsMax_MT_View3D_Create,
	BsMax_MT_View3D_Copy,
	BsMax_MT_View3D_Paste
}


def register_prerequisite():
	for cls in classes:
		register_class(cls)


def unregister_prerequisite():
	for cls in classes:
		unregister_class(cls)