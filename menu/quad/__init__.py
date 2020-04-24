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

from .quadmenu import register_quadmenu,unregister_quadmenu
from .keymap_std import register_keymap,unregister_keypam

def register_quad(preferences):
	register_quadmenu()
	if preferences.floatmenus == 'QuadMenu_st_andkey':
		register_keymap(preferences)

def unregister_quad():
	unregister_quadmenu()
	unregister_keypam()