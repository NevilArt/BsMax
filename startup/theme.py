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
import os

from bsmax.graphic import get_header_color


#TODO need to refresh on file open too
def autokey_state_updated(preferences):
	ctx = bpy.context
	autoKey = ctx.scene.tool_settings.use_keyframe_insert_auto
	color = (0.5, 0.0, 0.0, 1.0) if autoKey else get_header_color()
	# allow to update if affect_theme active in preference
	if color and preferences.affect_theme:
		ctx.preferences.themes['Default'].dopesheet_editor.space.header = color



def read_original_theme(self):
	theme = bpy.context.preferences.themes['Default']
	self.v3camera = theme.view_3d.camera
	self.v3empty = theme.view_3d.empty
	self.v3light = theme.view_3d.light



def to_string(color):
	count = len(color)
	string = "("

	for index in range(count):
		string += str(color[index])
		if index < count-1:
			string += ", "

	string += ")"

	return string



def save_original_theme_to_file(self):
	read_original_theme(self)

	# Save only once at inistal
	#TODO need a solution to update on theme changed
	if not os.path.exists(self.fileName):
		view_3d = self.theme.view_3d

		string = "view_3d.camera = " + to_string(view_3d.camera) + "\n"
		string += "view_3d.empty = " + to_string(view_3d.empty) + "\n"
		string += "view_3d.light = " + to_string(view_3d.light) + "\n"

		ini = open(self.fileName, 'w')
		ini.write(string)
		ini.close()



def load_original_theme_from_file(self):
	if os.path.exists(self.fileName):
		string = "view_3d = bpy.context.preferences.themes[0].view_3d\n"
		string += open(self.fileName).read()
		exec(string)



def restore_original_theme_from_file(self):
	load_original_theme_from_file(self)
	view_3d = self.theme.view_3d
	if self.v3camera:
		view_3d.camera = self.v3camera
	if self.v3empty:
		view_3d.empty = self.v3empty
	if self.v3light:
		view_3d.light = self.v3light



def set_3dsmax_theme(self, preferences):
	if preferences.affect_theme:
		view_3d = self.theme.view_3d
		view_3d.camera = (0.341, 0.47, 0.8)
		view_3d.empty = (0.054, 1, 0.007)
		view_3d.light = (0.8, 0.8, 0, 0.12)



class ThemaData():
	def __init__(self):
		self.theme = bpy.context.preferences.themes[0]
		self.fileName = bpy.utils.user_resource('SCRIPTS') + '\\addons\\BsMaxTheme.ini'
		self.v3camera = None
		self.v3empty = None
		self.v3light = None

	def save(self):
		save_original_theme_to_file(self)

	def restore(self):
		restore_original_theme_from_file(self)

	def apply(self, preferences):
		if preferences.affect_theme:
			if preferences.keymaps == '3DsMax':
				set_3dsmax_theme(self, preferences)

themaData = ThemaData()



def register_theme(preferences):
	global themaData
	themaData.save()
	themaData.apply(preferences)
	autokey_state_updated(preferences)



def unregister_theme():
	global themaData
	themaData.restore()