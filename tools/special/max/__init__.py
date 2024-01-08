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

# from .menu import register_menu,unregister_menu
from .modifier import register_modifier,unregister_modifier
from .side_panel import register_side_panel, unregister_side_panel

def register_max(preferences):
	register_modifier()
	if preferences.experimental:
		register_side_panel()

def unregister_max():
	unregister_modifier()
	unregister_side_panel()
