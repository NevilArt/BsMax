import bpy
from bpy.types import WorkSpaceTool

class CurveFilletTool(WorkSpaceTool):
	bl_space_type='VIEW_3D'
	bl_context_mode='EDIT_CURVE'

	# The prefix of the idname should be your add-on name.
	bl_idname = "bsmax.curvefillet"
	bl_label = "Fillet (Curve)"
	bl_description = ( "This is a tooltip")
	#bl_icon = "ops.generic.select_circle"
	bl_widget = None

	def draw_settings(ctx, layout, tool):
		#props = tool.operator_properties("view3d.select_circle")
		props = tool.operator_properties("curve.chamfer")
		#layout.prop(props, "mode")
		#layout.prop(props, "radius")
		print("asdfsadf")
	# def execute(self, ctx):
	# 	print("execuite")

	# def modal(self, ctx, event):
	# 	print("Haha")

	# def invoke(self, ctx, event):
	# 	wm = ctx.window_manager
	# 	wm.modal_handler_add(self)
	# 	return {'RUNNING_MODAL'}

class CurveChamferTool(WorkSpaceTool):
	bl_space_type='VIEW_3D'
	bl_context_mode='EDIT_CURVE'

	bl_idname = "bsmax.curvechamfer"
	bl_label = "Chamfer (Curve)"
	bl_description = ("This is a tooltip")
	#bl_icon = "ops.generic.select_lasso"
	bl_widget = None
	def draw_settings(ctx, layout, tool):
		# props = tool.operator_properties("view3d.select_lasso")
		# layout.prop(props, "mode")
		pass

def panel_cls(register):
	if register:
		bpy.utils.register_tool(CurveFilletTool, after={"builtin.randomize"}, separator=True, group=True)
		bpy.utils.register_tool(CurveChamferTool, after={CurveFilletTool.bl_idname})
	else:
		bpy.utils.unregister_tool(CurveFilletTool)
		bpy.utils.unregister_tool(CurveChamferTool)

if __name__ == '__main__':
	panel_cls(True)

__all__ = ["panel_cls"]