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

from .animation import register_animation,unregister_animation
from .render import register_render,unregister_render
from .rigg import register_rigg,unregister_rigg
from .menu import register_menu,unregister_menu

def register_assistant():
	register_animation()
	register_render()
	register_rigg()
	register_menu()

def unregister_assistant():
	unregister_animation()
	unregister_render()
	unregister_rigg()
	unregister_menu()
