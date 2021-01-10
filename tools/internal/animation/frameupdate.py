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
from bpy.app.handlers import persistent

@persistent
def frame_Update(scene):
	pass


dopesheet_editor = bpy.context.preferences.themes[0].dopesheet_editor
@persistent
def depsgraph_update(scene):
	""" called on each click and check the time slider header collor """
	if bpy.context.scene.tool_settings.use_keyframe_insert_auto:
		color = (0.5, 0.0, 0.0, 1.0)
	else:
		color = (0.2588, 0.2588, 0.2588, 1.0)
	
	# make sure mouse is over the time line and dopesheet to execute this command #
	# if dopesheet_editor.space.header != color:
		# dopesheet_editor.space.header = color
	# print("header> ",dopesheet_editor.space.header)
	# print("New> ",color)

def register_frameupdate():
	# bpy.app.handlers.frame_change_pre.append(frame_Update)
	bpy.app.handlers.depsgraph_update_pre.append(depsgraph_update)

def unregister_frameupdate():
	# bpy.app.handlers.frame_change_pre.remove(frame_Update)
	bpy.app.handlers.depsgraph_update_pre.remove(depsgraph_update)

if __name__ == "__main__":
	register_frameupdate()