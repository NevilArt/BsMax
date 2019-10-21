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

def floateditor_cls(register):
	classes = [BsMax_OT_MaterialEditorOpen, BsMax_OT_ScriptListenerOpen]
	for c in classes:
		if register: bpy.utils.register_class(c)
		else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	floateditor_cls(True)

__all__ = ["floateditor_cls"]