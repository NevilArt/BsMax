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



class BsMax_MT_View3D_tools(bpy.types.Menu):
	bl_idname = 'BSMAX_MT_view3dtools'
	bl_label = 'Tools'
	bl_context = 'objectmode'

	@classmethod
	def poll(self,ctx):
		return is_object_mode(ctx)

	def draw(self,ctx):
		layout=self.layout
		layout.menu('BSMAX_MT_animationtools',icon='ARMATURE_DATA')
		layout.menu('BSMAX_MT_riggtools',icon='TOOL_SETTINGS')
		layout.menu('BSMAX_MT_particletools',icon='MOD_PARTICLES')



def tools_menu(self,ctx):
	if ctx.mode == 'OBJECT':
		self.layout.menu('BSMAX_MT_view3dtools')
	elif ctx.mode == 'POSE':
		self.layout.menu('BSMAX_MT_animationtools')

def register_menu():
	bpy.utils.register_class(BsMax_MT_View3D_tools)
	bpy.types.VIEW3D_MT_editor_menus.append(tools_menu)

def unregister_menu():
	bpy.utils.unregister_class(BsMax_MT_View3D_tools)
	bpy.types.VIEW3D_MT_editor_menus.remove(tools_menu)

if __name__ == '__main__':
	register_menu()