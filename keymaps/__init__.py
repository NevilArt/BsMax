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

from .max import register_max,unregister_max
from .blender import register_blender,unregister_blender
from .cinema4d import register_cinema4d,unregister_cinema4d
from .maya import register_maya,unregister_maya
from .modo import register_modo,unregister_modo
from .softimage import register_softimage,unregister_softimage
from .navigation import register_navigation,unregister_navigation
from .public import register_public,unregister_public

def register_keymaps(preferences):
	unregister_keymaps()
	
	keymaps = preferences.keymaps
	if keymaps == '3DsMax':
		register_max()
	elif keymaps == 'Blender':
		register_blender()
	elif keymaps == 'Cinema4D':
		register_cinema4d()
	elif keymaps == 'Maya':
		register_maya()
	elif keymaps == 'Modo':
		register_modo()
	elif keymaps == 'Softimage':
		register_softimage()
	register_public()
	register_navigation(preferences)

def unregister_keymaps():
	unregister_max()
	unregister_blender()
	unregister_cinema4d()
	unregister_maya()
	unregister_modo()
	unregister_softimage()
	unregister_public()
	unregister_navigation()