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
from bsmax.state import is_object_mode

class BsMax_MT_Render_Tools(bpy.types.Menu):
	bl_idname = "BSMAX_MT_rendertools"
	bl_label = "Render"
	bl_context = "objectmode"

	@classmethod
	def poll(self, ctx):
		return is_object_mode(ctx)

	def draw(self, ctx):
		layout=self.layout
		layout.operator("render.light_lister",text="Light Lister",icon='LIGHT_SUN')

def render_menu(self, ctx):
	# self.layout.menu("BSMAX_MT_rendertools")
	layout = self.layout
	layout.separator()
	layout.operator("render.light_lister",text="Light Lister",icon='LIGHT_SUN')

def register_menu():
	bpy.utils.register_class(BsMax_MT_Render_Tools)
	bpy.types.TOPBAR_MT_render.append(render_menu)

def unregister_menu():
	bpy.types.TOPBAR_MT_render.remove(render_menu)
	bpy.utils.unregister_class(BsMax_MT_Render_Tools)