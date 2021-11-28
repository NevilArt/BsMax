############################################################################
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation,either version 3 of the License,or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not,see <https://www.gnu.org/licenses/>.
############################################################################

import bpy

# Dopesheet Right-Click Menu
# Ozzkar 06-Sep-2013
class BsMax_MT_EditAlignDopesheet(bpy.types.Menu):
	bl_idname = "bsmax.editaligndopesheet"
	bl_label = "Align Special"
	bl_description = "Align selection to specified point"

	def draw(self, ctx):
		layout = self.layout
		layout.operator("action.snap", text = "Selection To Cursor Frame").type='CFRA'
		layout.operator("action.snap", text = "Selection To Nearest Frame").type='NEAREST_FRAME'
		layout.operator("action.snap", text = "Selection To Nearest Second").type='NEAREST_SECOND'
		layout.operator("action.snap", text = "Selection To Nearest Marker").type='NEAREST_MARKER'
		layout.separator()
		layout.operator("action.frame_jump", text = "Cursor To Selection")

class BsMax_MT_ToolMenuDopesheet(bpy.types.Menu):
	bl_idname = "bmax.dopesheetrcmenu"
	bl_label = "BMax Dopesheet Tools"
	bl_description = "BMax right-click menu"

	def draw(self, ctx):
		layout = self.layout
		layout.operator_context = 'INVOKE_REGION_WIN'
		layout.operator("screen.redo_last", text = "Edit Last Action...", icon = "UI")
		layout.separator()
		layout.menu("BsMax_MT_EditAlignDopesheet", icon="ALIGN")
		layout.operator("action.duplicate_move", text = "Clone And Move", icon="MOD_BOOLEAN")
		layout.separator()
		layout.operator("action.handle_type", text = "Handle Type", icon="CURVE_BEZCURVE")
		layout.operator("action.keyframe_type", text = "Keyframe Type", icon="SPACE3")
		layout.operator("action.interpolation_type", text = "Interpolation", icon="IPO_CONSTANT")
		layout.separator()
		operator = layout.operator("wm.context_set_enum", text = "Switch To Graph", icon="IPO")
		operator.data_path = 'area.type'
		operator.value = 'GRAPH_EDITOR'
		layout.separator()
		if ctx.screen.show_fullscreen:
			layout.operator("screen.screen_full_area", text="Restore Viewport", icon="SPLITSCREEN")
		else:
			layout.operator("screen.screen_full_area", text="Maximize Viewport", icon="FULLSCREEN")


classes = [BsMax_MT_EditAlignDopesheet, BsMax_MT_ToolMenuDopesheet]

def dopesheet_register():
	for c in classes:
		bpy.utils.register_class(c)

def dopesheet_unregister():
	for c in classes:
		bpy.utils.unregister_class(c)