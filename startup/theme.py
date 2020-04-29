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

v3camera, v3empty, v3light = None, None, None

def store_original_theme():
	#TODO save to ini file and read again
	v3camera = bpy.context.preferences.themes[0].view_3d.camera
	v3empty = bpy.context.preferences.themes[0].view_3d.empty
	v3light = bpy.context.preferences.themes[0].view_3d.light

def restore_original_theme():
	if v3camera != None:
		bpy.context.preferences.themes[0].view_3d.camera = v3camera
	if v3empty !=  None:
		bpy.context.preferences.themes[0].view_3d.empty = v3empty
	if v3light != None:
		bpy.context.preferences.themes[0].view_3d.light = v3light

def set_3dsmax_theme():
	bpy.context.preferences.themes[0].view_3d.camera = (0.341,0.47,0.8)
	bpy.context.preferences.themes[0].view_3d.empty = (0.054,1,0.007)
	bpy.context.preferences.themes[0].view_3d.light = (1,0.898,0,1)

def register_theme(preferences):
	store_original_theme()
	if preferences.keymaps == '3DsMax':
		set_3dsmax_theme()

def unregister_theme():
	store_original_theme()
