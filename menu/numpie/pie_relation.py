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
# 2025/10/16

import bpy

from bpy.types import Menu

from .numpadpie import get_menu, get_menu_pie

class VIEW3D_MT_PIE_View3D_Object_Relation(Menu):
	bl_idname = "BSMAX_MT_pie_view3d_object_Relation"
	bl_label = "Parent"

	def draw(self, context):
		pie = self.layout.menu_pie()
		# pie.label(text="Left")
		# pie.label(text="Right")
		# pie.label(text="Bottom")
		# pie.label(text="Top")
		# pie.label(text="LT")
		# pie.label(text="RT")
		# pie.label(text="LD")
		# pie.label(text="RD")