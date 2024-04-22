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
	bl_idname = 'BSMAX_MT_view3dtools'
	bl_label = 'Tools'
	
	def draw(self, ctx):
		pass


class BsMax_MT_Compositor_tools(Menu):
	bl_idname = 'BSMAX_MT_compositor_tools'
	bl_label = 'Tools'

	def draw(self, ctx):
		pass


class BsMax_MT_View3D_Create(Menu):
	bl_idname = "BSMAX_MT_create_menu"
	bl_label = "Create"
	bl_context = "objectmode"

	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'OBJECT'

	def draw(self, ctx):
		pass


classes = (
	BsMax_MT_View3D_tools,
	BsMax_MT_Compositor_tools,
	BsMax_MT_View3D_Create
)


def register_prerequisite():
	for c in classes:
		register_class(c)


def unregister_prerequisite():
	for c in classes:
		unregister_class(c)