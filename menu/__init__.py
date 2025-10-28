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

from .quad import register_quad, unregister_quad
from .numpie import register_numpie_main, unregister_numpie_main

def register_menu(preferences):
	if preferences.floatmenus == 'NUMPIE':
		register_numpie_main()
	elif preferences.floatmenus == '3DSMAX':
		register_quad(preferences)
	

def unregister_menu():
	unregister_quad()
	unregister_numpie_main()
