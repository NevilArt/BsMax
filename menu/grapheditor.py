import bpy
from bpy.types import Menu

# Graph Editor Right-Click Menu
# Ozzkar 2018
class BsMax_EM_EditAlignGraph_MT(Menu):
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

class BsMax_MT_ToolMenuGraph(Menu):
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
	
def grapheditor_menu(register):
	classes = [BsMax_EM_EditAlignGraph_MT, BsMax_MT_ToolMenuGraph]
	for c in classes:
		if register: bpy.utils.register_class(c)
		else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	grapheditor_menu(True)

__all__ = ["grapheditor_menu"]
