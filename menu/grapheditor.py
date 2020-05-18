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

# Graph Editor Right-Click Menu
# Ozzkar 2018
class BsMax_EM_EditAlignGraph_MT(bpy.types.Menu):
	bl_label = "Align Special"
	bl_description = "Align selection to specified point"

	def draw(self, ctx):
		layout = self.layout
		layout.operator("graph.snap", text = "Flatten Handles").type='HORIZONTAL'
		layout.separator()
		layout.operator("graph.snap", text = "Selection To Cursor Value").type='VALUE'
		layout.operator("graph.snap", text = "Selection To Cursor Frame").type='CFRA'
		layout.operator("graph.snap", text = "Selection To Nearest Frame").type='NEAREST_FRAME'
		layout.operator("graph.snap", text = "Selection To Nearest Second").type='NEAREST_SECOND'
		layout.operator("graph.snap", text = "Selection To Nearest Marker").type='NEAREST_MARKER'
		layout.separator()
		layout.operator("graph.frame_jump", text = "Cursor To Selection")

class BsMax_MT_ToolMenuGraph(bpy.types.Menu):
	bl_label = "BMax Graph Tools"
	bl_description = "BMax right-click menu"

	def draw(self, ctx):
		layout = self.layout
		layout.operator_context = 'INVOKE_REGION_WIN'

		layout.operator("screen.redo_last", text = "Edit Last Action...", icon = "UI")
		layout.separator()
		layout.menu("BMAX_EM_EditAlignGraph_MT", icon="ALIGN")
		layout.operator("graph.duplicate_move", text = "Clone And Move", icon="MOD_BOOLEAN")
		layout.separator()
		layout.operator("graph.handle_type", text = "Handle Type", icon="CURVE_BEZCURVE")
		layout.operator("graph.easing_type", text = "Easing Type", icon="IPO_EASE_IN_OUT")
		layout.operator("graph.interpolation_type", text = "Interpolation", icon="IPO_CONSTANT")
		layout.separator()
		op = layout.operator("wm.context_set_enum", text = "Switch To Dopesheet", icon="ACTION")
		op.data_path = 'area.type'
		op.value = 'DOPESHEET_EDITOR'
		layout.separator()
		layout.operator("wm.context_menu_enum", text="Rotation/Scale Pivot", icon="ROTATE").data_path='space_data.pivot_point'
		if ctx.screen.show_fullscreen:
			layout.operator("screen.screen_full_area", text="Restore Viewport", icon="SPLITSCREEN")
		else:
			layout.operator("screen.screen_full_area", text="Maximize Viewport", icon="FULLSCREEN")


classes = [BsMax_EM_EditAlignGraph_MT, BsMax_MT_ToolMenuGraph]

def grapheditor_register():
	[bpy.utils.register_class(c) for c in classes]

def grapheditor_unregister():
	[bpy.utils.unregister_class(c) for c in classes]