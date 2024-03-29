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

from .max_pie_menu import register_pie_max, unregister_pie_max
from .sub_menu import register_sub_menu, unregister_sub_menu

def register_quad(preferences):
	register_sub_menu()
	register_pie_max(preferences)

def unregister_quad():
	unregister_pie_max()
	unregister_sub_menu()