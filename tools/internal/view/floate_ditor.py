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
from operator import itemgetter



class Editor_OT_Open_As_Float_Window(Operator):
	bl_idname = 'editor.float'
	bl_label = 'Open As Float Window'
	bl_options = {'REGISTER', 'INTERNAL'}
	
	ui_type: StringProperty(default='VIEW_3D')
	shader_type: StringProperty(default='')

	def execute(self,ctx):
		version = bpy.app.version
		if version[0] == 2 and version[1] <= 92:
			""" Old Method for Blender 2.92 and older """
			original_type = ctx.area.type

			ctx.area.ui_type = self.ui_type
			if self.shader_type != '':
				ctx.space_data.shader_type = self.shader_type

			bpy.ops.screen.area_dupli('INVOKE_DEFAULT')
			ctx.area.type = original_type
		
		else:
			""" New Method for Blender 2.93 and Newer """
			windows = ctx.window_manager.windows
			
			""" Pass if exist """
			for window in windows:
				for area in window.screen.areas:
					if area.ui_type == self.ui_type:
						if self.shader_type != '':
							for space in area.spaces:
								if hasattr(space, 'shader_type'):
									if space.shader_type == self.shader_type:
										return{'FINISHED'}
						else:
							return{'FINISHED'}

			""" Create New Window """
			bpy.ops.wm.window_new()
			area = windows[-1].screen.areas[0]
			area.ui_type = self.ui_type
			if self.shader_type != '':
				ctx.space_data.shader_type = self.shader_type

		return{'FINISHED'}

class Editor_OT_Script_Listener_Open(Operator):
	bl_idname = 'editor.script_listener'
	bl_label = 'Script Listener(Float)'
	bl_options = {'REGISTER', 'INTERNAL'}
	
	def execute(self,ctx):
		version = bpy.app.version
		if version[0] == 2 and version[1] <= 92:
			""" Old Method for Blender 2.92 and older """
			windows = ctx.window_manager.windows
			bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
			area = windows[-1].screen.areas[0]
			area.type = 'CONSOLE'
			bpy.ops.screen.area_split(direction='HORIZONTAL',factor=0.5)
			area = windows[-1].screen.areas[0]
			area.type = 'INFO'
		
		else:
			""" New Method for Blender 2.93 and Newer """
			windows = ctx.window_manager.windows
			
			""" Pass if exist """
			for window in windows:
				if len(window.screen.areas) == 2:
					areas = window.screen.areas
					if areas[0].ui_type == 'INFO' and areas[1].ui_type == 'CONSOLE':
						return{'FINISHED'}

			""" Create New Window """
			bpy.ops.wm.window_new()
			area = windows[-1].screen.areas[0]
			area.ui_type = 'CONSOLE'
			bpy.ops.screen.area_split(direction='HORIZONTAL',factor=0.5)
			area = windows[-1].screen.areas[0]
			area.type = 'INFO'
		
		return{'FINISHED'}

classes = [Editor_OT_Open_As_Float_Window,Editor_OT_Script_Listener_Open]

def register_float_editor():
	[bpy.utils.register_class(c) for c in classes]

def unregister_float_editor():
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_float_editor()