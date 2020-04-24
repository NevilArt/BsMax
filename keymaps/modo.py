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
from bsmax.keymaps import KeyMaps

def collect_mute_keymaps(km):
	pass

def create_keymaps(km):
	if bpy.context.window_manager.keyconfigs.addon:
		print("add Modo keymaps")
		# Window ---------------------------------------------------------------
		# space = km.space('Object Non-modal','EMPTY','WINDOW')
		# km.new(space,"bsmax.mode_set",'F9',"PRESS",[])
		
keymaps = KeyMaps()

def register_modo():
	keymaps.reset()
	create_keymaps(keymaps)
	collect_mute_keymaps(keymaps)
	keymaps.set_mute(False)

def unregister_modo():
	keymaps.reset()