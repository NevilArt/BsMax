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

# Open a Material editor
class BsMax_OT_MaterialEditorOpen(Operator):
	bl_idname = "bsmax.openmaterialeditor"
	bl_label = "Material Editor(Open)"
	def execute(self, contecxt):
		Area = bpy.context.area
		Editor = Area.type
		Area.type = 'NODE_EDITOR' #'ShaderNodeTree'
		bpy.ops.screen.area_dupli('INVOKE_DEFAULT')
		Area.type = Editor
		return{"FINISHED"}

# Open a Script listener
class BsMax_OT_ScriptListenerOpen(Operator):
	bl_idname = "bsmax.scriptlistener"
	bl_label = "Script Listener(Open)"
	def execute(self, contecxt):
		bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
		area = bpy.context.window_manager.windows[-1].screen.areas[0]
		area.type = 'CONSOLE'
		bpy.ops.screen.area_split(direction='HORIZONTAL', factor=0.5)
		area = bpy.context.window_manager.windows[-1].screen.areas[0]
		area.type = 'INFO'
		return{"FINISHED"}

classes = [BsMax_OT_MaterialEditorOpen, BsMax_OT_ScriptListenerOpen]

def register_floateditor():
	[bpy.utils.register_class(c) for c in classes]

def unregister_floateditor():
	[bpy.utils.unregister_class(c) for c in classes]