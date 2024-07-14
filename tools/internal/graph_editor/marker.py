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
# 2024/07/12

import bpy

from bpy.types import Operator
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


class Marker_OT_shift(Operator):
	bl_idname = 'marker.shiftm'


def marker_rename_menu(self, _):
	layout = self.layout
	layout.separator()
	layout.operator('marker.auto_rename')


classes = {
    Marker_OT_Auto_Rename
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
	register_marker()