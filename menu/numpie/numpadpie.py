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
# 2025/10/15

import bpy

from bpy.types import Menu

# Piemenu Order by Index
#			4
#		5		6
#	1				2
#		7		8
#			3


def get_menu(pie, text:str, icon:str, name:str) -> None:
	if icon:
		pie.operator("wm.call_menu", text=text, icon=icon).name=name
		return
	pie.operator("wm.call_menu", text=text).name=name


def get_menu_pie(pie, text:str, icon:str, name:str, mode) -> None:
	if icon:
		pie.operator("wm.call_menu_pie", text=text, icon=icon).name=name
		return
	pie.operator("wm.call_menu_pie", text=text).name=name


class VIEW3D_MT_PIE_Template(Menu):
	bl_idname = "BSMAX_MT_pie_template"
	bl_label = "Template"

	def draw(self, context):
		pass


def register_numpadpie():
	bpy.utils.register_class(VIEW3D_MT_PIE_Template)

def unregister_numpadpie():
	bpy.utils.unregister_class(VIEW3D_MT_PIE_Template)

if __name__ == '__main__':
	register_numpadpie()
