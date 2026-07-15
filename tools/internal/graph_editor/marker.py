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
# 2025/10/03
# 2026/08/02 Marker set ranege added
# 2026/08/13 Marker setrange menu added

import bpy

from bpy.types import Operator, Menu
from bpy.props import BoolProperty, EnumProperty
from bpy.utils import register_class, unregister_class
from bpy.app import version


def is_digits(string:str) -> bool:
	for char in string:
		if not char in '0123456789':
			return False
	return True


def fix_marker_name(marker) -> None:
	parts = marker.name.split('_')
	if len(parts) != 2:
		return
	if parts[0] == 'F' and is_digits(parts[1]):
		marker.name = "F_" + str(marker.frame)


def copy_markers_to_clipboard(
	context:bpy.types.Context,
	copy_all:bool
) -> None:

	markers =[
		marker for marker in context.scene.timeline_markers
		if marker.select or copy_all
	]
	text = "BSMAXCOPYMARKERKEYWORD\n"
	for marker in markers:
		text += marker.name + ','
		text += str(marker.frame) + '\n'

	context.window_manager.clipboard = text


def paste_markers_from_clipboard(context:bpy.types.Context) -> None:
	keys = context.window_manager.clipboard.split('\n')

	if not keys:
		return

	if keys[0] != "BSMAXCOPYMARKERKEYWORD":
		return

	for key in keys[1:]:
		parts = key.split(',')
		if len(parts) < 2:
			continue
		name = parts[0]
		frame = int(parts[1])
		context.scene.timeline_markers.new(name, frame=frame)


def get_first_last_marker_frame(context):
	markers = context.scene.timeline_markers
	if not markers:
		return None, None

	frames = sorted(m.frame for m in markers)

	if len(frames) == 1:
		return 0, frames[0]

	return frames[0], frames[-1]

def get_first_last_selected_marker_frame(context):
	markers = context.scene.timeline_markers
	selected = sorted(m.frame for m in markers if m.select)

	if not selected:
		return 0, max((m.frame for m in markers), default=0)

	if len(selected) == 1:
		return selected[0], selected[0]

	return selected[0], selected[-1]

def get_prev_next_marker_frame(context):
	scene = context.scene
	current = scene.frame_current
	markers = scene.timeline_markers

	prev_frames = [m.frame for m in markers if m.frame < current]
	next_frames = [m.frame for m in markers if m.frame > current]

	prev_frame = max(prev_frames) if prev_frames else current
	next_frame = min(next_frames) if next_frames else current

	return prev_frame, next_frame

def set_timeline_range(context, first, last, preview=False):
	scene = context.scene
	if preview:
		scene.use_preview_range = True
		scene.frame_preview_start = first
		scene.frame_preview_end = last
	else:
		scene.frame_start = first
		scene.frame_end = last


class Marker_OT_Auto_Rename(Operator):
	bl_idname = 'marker.auto_rename'
	bl_label = "Auto Rename"
	bl_description = "Rename shifted Marker to Frame Name (Ignore Manualy Renamed)"
	bl_options = {'REGISTER', 'UNDO'}
	
	# @classmethod
	# def poll(self, _):
	# 	return True
	
	def execute(self, context:bpy.types.Context) -> set[str]:
		for marker in context.scene.timeline_markers:
			fix_marker_name(marker)
		return{'FINISHED'}


class Marker_OT_Copy(Operator):
	bl_idname = 'marker.copy'
	bl_label = "Marker Copy"
	bl_description = "Copy Marker to other Scene or Blender"
	bl_options = {'REGISTER', 'UNDO'}

	all: BoolProperty(
		default=True,
		description="Copy All Markers"
	) # type: ignore

	@classmethod
	def poll(self, context):
		return bool(context.scene.timeline_markers)
	
	def draw(self, _) -> None:
		self.layout.prop(
			self, 'all', text="Copy All Markers"
		)
	
	def execute(self, context:bpy.types.Context) -> set[str]:
		copy_markers_to_clipboard(context, self.all)
		return{'FINISHED'}


class Marker_OT_Paste(Operator):
	bl_idname = 'marker.paste'
	bl_label = "Marker Paste"
	bl_description = "Paste Marker in other scene or blender"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context:bpy.types.Context) -> set[str]:
		paste_markers_from_clipboard(context)	
		return{'FINISHED'}


class Marker_OT_Set_Range(Operator):
	bl_idname = 'marker.set_range'
	bl_label = "Marker Set Range"
	bl_description = "Set the range with markers"
	bl_options = {'REGISTER', 'UNDO'}

	mode: EnumProperty(
		name="Mode",
		description="How to determine the frame range from markers",
		items=[
			(
				'ALL', "All",
				"Set the range from the first marker to the last marker"
			),
			(
				'TO_FIRST', "To First",
				"Set the range from the next marker to the first marker"
			),
			(
				'TO_LAST', "To Last",
				"Set the range from the previous marker to the last marker"
			),
			(
				'CURRENT', "Current", 
				"Set the range from the previous marker to the next marker"
			),
			(
				'SELECTED',
				"Selected",
				"Set the range from the first selected marker to the last selected marker"
			)
		],
		default='ALL',
	) # type: ignore

	preview: BoolProperty(
			default=False,
			description="Set Preview Range instead of Frame Range"
		) # type: ignore

	@classmethod
	def poll(self, context):
		return bool(context.scene.timeline_markers)
	
	def execute(self, context:bpy.types.Context) -> set[str]:
		if self.mode == 'ALL':
			start, end = get_first_last_marker_frame(context)
			set_timeline_range(context, start, end, preview=self.preview)
		elif self.mode == 'TO_FIRST':
			_, next = get_prev_next_marker_frame(context)
			start, _ = get_first_last_marker_frame(context)
			set_timeline_range(context, start, next-1, preview=self.preview)
		elif self.mode == 'TO_LAST':
			prev, _ = get_prev_next_marker_frame(context)
			_, end = get_first_last_marker_frame(context)
			set_timeline_range(context, prev, end, preview=self.preview)
		elif self.mode == 'CURRENT':
			prev, next = get_prev_next_marker_frame(context)
			set_timeline_range(context, prev, next-1, preview=self.preview)
		elif self.mode == 'SELECTED':
			start, end = get_first_last_selected_marker_frame(context)
			set_timeline_range(context, start, end-1, preview=self.preview)

		return{'FINISHED'}


class BsMax_MT_Marker_Set_Range(Menu):
	bl_idname = 'BSMAX_MT_marker_set_range'
	bl_label = "Marker Set Range"
	bl_description = "Set animation range based on markers"
	# bl_context = 'objectmode'

	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'OBJECT'

	def draw(self, ctx):
		layout=self.layout

		layout.operator('marker.set_range', text="All").mode='ALL'
		layout.operator('marker.set_range', text="To First").mode='TO_FIRST'
		layout.operator('marker.set_range', text="To Last").mode='TO_LAST'
		layout.operator('marker.set_range', text="Current").mode='CURRENT'
		layout.operator('marker.set_range', text="Selected").mode='SELECTED'


def marker_rename_menu(self, _):
	layout = self.layout
	layout.operator('marker.copy', text="Copy")
	layout.operator('marker.paste', text="Paste")
	layout.separator()
	layout.operator('marker.auto_rename')
	layout.menu('BSMAX_MT_marker_set_range', text="Set Range")


classes = {
	Marker_OT_Auto_Rename,
	Marker_OT_Copy,
	Marker_OT_Paste,
	Marker_OT_Set_Range,
	BsMax_MT_Marker_Set_Range
}


def register_marker():
	for cls in classes:
		register_class(cls)

	types = bpy.types
	types.DOPESHEET_MT_marker.prepend(marker_rename_menu)
	types.GRAPH_MT_marker.prepend(marker_rename_menu)
	types.NLA_MT_marker.prepend(marker_rename_menu)
	types.SEQUENCER_MT_marker.prepend(marker_rename_menu)

	if version < (5, 0, 0):
		types.TIME_MT_marker.prepend(marker_rename_menu)


def unregister_marker():
	types = bpy.types
	types.DOPESHEET_MT_marker.remove(marker_rename_menu)
	types.GRAPH_MT_marker.remove(marker_rename_menu)
	types.NLA_MT_marker.remove(marker_rename_menu)
	types.SEQUENCER_MT_marker.remove(marker_rename_menu)

	if version < (5, 0, 0):
		types.TIME_MT_marker.remove(marker_rename_menu)

	for cls in classes:
		unregister_class(cls)


if __name__ == '__main__':
	# register_marker()
	for cls in classes:
		register_class(cls)