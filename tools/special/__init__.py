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

from .blender import register_blender, unregister_blender
from .max import register_max, unregister_max
from .maya import register_maya, unregister_maya



class RegisterData:
	def __init__(self):
		self.pack_max = False
		self.pack_maya = False
		self.pack_blender = False

reg = RegisterData()




def get_active_apps(preferences):
	prefs = [preferences.viowport]
		# preferences.sculpt,
		# preferences.uv_editor,
		# preferences.node_editor,
		# preferences.graph_editor,
		# preferences.dope_sheet,
		# preferences.clip_editor,
		# preferences.video_sequencer,
		# preferences.text_editor,
		# preferences.file_browser]
	apps = []
	for app in prefs:
		if not app in apps:
			apps.append(app)
	return apps



def register_special(preferences):
	unregister_special()
	
	if not reg.pack_max:
		register_max()
		reg.pack_max = True
	
	if not reg.pack_blender:
		register_blender()
		reg.pack_blender = True
	
	if not reg.pack_maya:
		register_maya()
		reg.pack_maya = True



def unregister_special():
	if reg.pack_blender:
		unregister_blender()
	
	if reg.pack_max:
		unregister_max()
	
	if reg.pack_maya:
		unregister_maya()