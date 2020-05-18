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

class Editor_OT_NodeEditorFloat(Operator):
	bl_idname = "editor.open_node_ditor"
	bl_label = "Node Editor(Float)"
	mode: bpy.props.StringProperty()

	def execute(self,ctx):
		area = ctx.area
		original_type = ctx.area.type
		if self.mode == 'Material':
			ctx.area.ui_type = 'ShaderNodeTree'
			ctx.space_data.shader_type = 'OBJECT'
		elif self.mode == 'Environment':
			ctx.area.ui_type = 'ShaderNodeTree'
			ctx.space_data.shader_type = 'WORLD'
		elif self.mode == 'Composit':
			area.ui_type = 'CompositorNodeTree'

		bpy.ops.screen.area_dupli('INVOKE_DEFAULT')
		area.type = original_type
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
		return{"FINISHED"}

classes = [Editor_OT_NodeEditorFloat,Editor_OT_ScriptListenerOpen]

def register_floateditor():
	[bpy.utils.register_class(c) for c in classes]

def unregister_floateditor():
	[bpy.utils.unregister_class(c) for c in classes]