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

class Editor_OT_Open_As_Float_Window(Operator):
	bl_idname = "editor.float"
	bl_label = "Open As Float Window"
	
	ui_type: StringProperty(default='VIEW_3D')
	shader_type: StringProperty(default='')

	def execute(self,ctx):
		original_type = ctx.area.type

		ctx.area.ui_type = self.ui_type
		if self.shader_type != '':
			ctx.space_data.shader_type = self.shader_type

		bpy.ops.screen.area_dupli('INVOKE_DEFAULT')
		ctx.area.type = original_type

		self.report({'OPERATOR'},'bpy.ops.editor.float()')
		return{"FINISHED"}

class Editor_OT_ScriptListenerOpen(Operator):
	bl_idname = "editor.script_listener"
	bl_label = "Script Listener(Float)"
	def execute(self,ctx):
		bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
		area = ctx.window_manager.windows[-1].screen.areas[0]
		area.type = 'CONSOLE'
		bpy.ops.screen.area_split(direction='HORIZONTAL',factor=0.5)
		area = ctx.window_manager.windows[-1].screen.areas[0]
		area.type = 'INFO'
		self.report({'OPERATOR'},'bpy.ops.editor.script_listener()')
		return{"FINISHED"}

classes = [Editor_OT_Open_As_Float_Window,Editor_OT_ScriptListenerOpen]

def register_floateditor():
	[bpy.utils.register_class(c) for c in classes]

def unregister_floateditor():
	[bpy.utils.unregister_class(c) for c in classes]