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
# 2026/09/10 

import bpy
from bpy.types import Operator, Panel 
from bpy.props import EnumProperty, FloatProperty, BoolProperty, PointerProperty


def _tool_ease(key_x, key_y, neighbor_x, neighbor_y):
	"""Flat handle at 1/3 of the x-distance toward the neighbor key."""
	dist_x = neighbor_x - key_x
	hx = key_x + (1.0 / 3.0) * dist_x
	hy = key_y
	return hx, hy

def _tool_auto_linear(key_x, key_y, neighbor_x, neighbor_y):
    """Zero-length handle collapsed onto the key itself."""
    return key_x, key_y

def _tool_linear(key_x, key_y, neighbor_x, neighbor_y):
	"""Zero-length handle collapsed onto the key itself."""
	dist_x = neighbor_x - key_x
	dist_y = neighbor_y - key_y
	hx = key_x + (1.0 / 3.0) * dist_x
	hy = key_y + (1.0 / 3.0) * dist_y
	return hx, hy

def _tool_reverse_ease(key_x, key_y, neighbor_x, neighbor_y):
    """Handle at 1/3 distance toward neighbor, but sitting at the neighbor's
    y-level instead of the key's own y-level (opposite of a flat ease)."""
    dist_x = neighbor_x - key_x
    hx = key_x + (1.0 / 3.0) * dist_x
    hy = neighbor_y
    return hx, hy


HANDLE_TOOLS = {
	'EASE': _tool_ease,
	'LINEAR': _tool_linear,
	'AUTO_LINEAR': _tool_auto_linear,
	'REVERSE_EASE': _tool_reverse_ease
}


class FCTOOLS_OT_apply_handle_tool(Operator):
	"""Apply a handle-shaping tool to selected keyframes on selected F-Curves"""
	bl_idname = "fctools.apply_handle_tool"
	bl_label = "Apply Handle Tool"
	bl_options = {'REGISTER', 'UNDO'}

	tool: EnumProperty(
		items=[
			('EASE', "Ease", "Flat handle at 1/3 distance toward the neighboring key"),
			('AUTO_LINEAR', "Auto Linear", "Zero-length handle collapsed onto the key itself"),
			('LINEAR', "Linear", "Handle collapsed onto the key point"),
			(
				'REVERSE_EASE', "Reverse Ease",
				"Handle at 1/3 distance toward neighbor, but sitting at the neighbor's y-level"
			)
		],
		name="Tool",
	) # type: ignore

	left : BoolProperty(
		name="Left Handle", description="Set left handle type", default=False
	) # type: ignore

	right : BoolProperty(
		name="Right Handle", description="Set right handle type", default=False
	) # type: ignore

	def execute(self, context):
		func = HANDLE_TOOLS[self.tool]

		for fcurve in context.selected_editable_fcurves:
			kps = fcurve.keyframe_points
			n = len(kps)

			for i, kp in enumerate(kps):
				if not kp.select_control_point:
					continue

				if self.left and i > 0:
					prev = kps[i - 1]
					hx, hy = func(kp.co.x, kp.co.y, prev.co.x, prev.co.y)
					kp.handle_left_type = 'FREE'
					kp.handle_left.x = hx
					kp.handle_left.y = hy

				if self.right and i < n - 1:
					nxt = kps[i + 1]
					hx, hy = func(kp.co.x, kp.co.y, nxt.co.x, nxt.co.y)
					kp.handle_right_type = 'FREE'
					kp.handle_right.x = hx
					kp.handle_right.y = hy

			fcurve.update()

		return {'FINISHED'}


class FCTOOLS_PT_main(Panel):
	bl_label = "FC Tools"
	bl_idname = "FCTOOLS_PT_main"
	bl_space_type = 'GRAPH_EDITOR'
	bl_region_type = 'UI'
	bl_category = "FC Tools"  # this creates the new sidebar tab

	def draw(self, context):
		layout = self.layout

		col = layout.column(align=True)
		col.label(text="Handle Tools:")
		row = col.row(align=True)
		op = row.operator('fctools.apply_handle_tool', text="<", icon='IPO_BEZIER')
		op.tool = 'EASE'
		op.left = True
		op.right = False

		op = row.operator('fctools.apply_handle_tool', text=">", icon='IPO_BEZIER')
		op.tool = 'EASE'
		op.left = False
		op.right = True

		row = col.row(align=True)
		op = row.operator('fctools.apply_handle_tool', text="<", icon='FIXED_SIZE')
		op.tool = 'AUTO_LINEAR'
		op.left = True
		op.right = False

		op = row.operator('fctools.apply_handle_tool', text=">", icon='FIXED_SIZE')
		op.tool = 'AUTO_LINEAR'
		op.left = False
		op.right = True

		row = col.row(align=True)
		op = row.operator('fctools.apply_handle_tool', text="<", icon='HANDLE_VECTOR')
		op.tool = 'LINEAR'
		op.left = True
		op.right = False

		op = row.operator('fctools.apply_handle_tool', text=">", icon='HANDLE_VECTOR')
		op.tool = 'LINEAR'
		op.left = False
		op.right = True

		row = col.row(align=True)
		op = row.operator('fctools.apply_handle_tool', text="<", icon='SHARPCURVE')
		op.tool = 'REVERSE_EASE'
		op.left = True
		op.right = False

		op = row.operator('fctools.apply_handle_tool', text=">", icon='SHARPCURVE')
		op.tool = 'REVERSE_EASE'
		op.left = False
		op.right = True


classes = {
	FCTOOLS_OT_apply_handle_tool,
	FCTOOLS_PT_main
}


def register_fcurve_tools():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister_fcurve_tools():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)


if __name__ == "__main__":
	register_fcurve_tools()
