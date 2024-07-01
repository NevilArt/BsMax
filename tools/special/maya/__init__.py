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
from .tools import register_tools, unregister_tools

def register_maya(preferences):
	if preferences.viowport == "MAYA":
		register_tools()
	register_modifier()

def unregister_maya():
	unregister_tools()
	unregister_modifier()