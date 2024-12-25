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
# 2024/10/21

import bpy

from bpy.types import Operator
from bpy.props import BoolProperty
from bpy.utils import register_class, unregister_class


def is_digits(string):
	for char in string:
		if not char in '0123456789':
			return False
	return True


def fix_marker_name(marker):
	parts = marker.name.split('_')
	if len(parts) != 2:
		return
	if parts[0] == 'F' and is_digits(parts[1]):
		marker.name = "F_" + str(marker.frame)


def copy_markers_to_clipboard(ctx, copy_all):
	markers =[
		marker for marker in ctx.scene.timeline_markers
		if marker.select or copy_all
	]
	text = "BSMAXCOPYMARKERKEYWORD\n"
	for marker in markers:
		text += marker.name + ','
		text += str(marker.frame) + '\n'

	ctx.window_manager.clipboard = text


def paste_markers_from_clipboard(ctx):
	keys = ctx.window_manager.clipboard.split('\n')

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
		ctx.scene.timeline_markers.new(name, frame=frame)


class Marker_OT_Auto_Rename(Operator):
	bl_idname = 'marker.auto_rename'
	bl_label = "Auto Rename"
	bl_description = "Rename shifted Marker to Frame Name (Ignore Manualy Renamed)"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(self, ctx):
		return True
	
	def execute(self, ctx):
		for marker in ctx.scene.timeline_markers:
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
	def poll(self, ctx):
		return True
	
	def draw(self, ctx):
		self.layout.prop(
			self, 'all', text="Copy All Markers"
		)
	
	def execute(self, ctx):
		copy_markers_to_clipboard(ctx, self.all)
		return{'FINISHED'}


class Marker_OT_Paste(Operator):
	bl_idname = 'marker.paste'
	bl_label = "Marker Paste"
	bl_description = "Paste Marker in other scene or blender"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return True
	
	def execute(self, ctx):
		paste_markers_from_clipboard(ctx)	
		return{'FINISHED'}


class Marker_OT_shift(Operator):
	bl_idname = 'marker.shiftm'


def marker_rename_menu(self, _):
	layout = self.layout
	layout.operator('marker.copy', text="Copy")
	layout.operator('marker.paste', text="Paste")
	layout.separator()
	layout.operator('marker.auto_rename')


classes = {
    Marker_OT_Auto_Rename,
	Marker_OT_Copy,
	Marker_OT_Paste
}


def register_marker():
	for cls in classes:
		register_class(cls)
	
	bpy.types.DOPESHEET_MT_marker.prepend(marker_rename_menu)
	bpy.types.GRAPH_MT_marker.prepend(marker_rename_menu)
	bpy.types.NLA_MT_marker.prepend(marker_rename_menu)
	bpy.types.SEQUENCER_MT_marker.prepend(marker_rename_menu)
	bpy.types.TIME_MT_marker.prepend(marker_rename_menu)


def unregister_marker():
	bpy.types.DOPESHEET_MT_marker.remove(marker_rename_menu)
	bpy.types.GRAPH_MT_marker.remove(marker_rename_menu)
	bpy.types.NLA_MT_marker.remove(marker_rename_menu)
	bpy.types.SEQUENCER_MT_marker.remove(marker_rename_menu)
	bpy.types.TIME_MT_marker.remove(marker_rename_menu)

	for cls in classes:
		unregister_class(cls)


if __name__ == '__main__':
	# register_marker()
	for cls in classes:
		register_class(cls)