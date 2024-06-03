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

def register_default(preferences):
	if preferences.keymaps == '3DSMAX':
		try:
			for area in bpy.context.screen.areas:
				if area.type == 'VIEW_3D':
					ctx = bpy.context
					ctx.space_data.overlay.show_cursor = False
					ctx.space_data.overlay.show_annotation = False
					ctx.space_data.lens = 45
					ctx.space_data.clip_start = 0.001
		except:
			pass

def unregister_default():
	pass