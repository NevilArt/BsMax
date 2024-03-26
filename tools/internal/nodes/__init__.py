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

from .auto_exr import register_auto_exr, unregister_auto_exr
from .presets import register_presets, unregister_presets
from .matt import register_matt, unregister_matt
from .gnodes import register_gnodes, unregister_gnodes
from .menu import register_nodes_menu, unregister_nodes_menu

def register_nodes():
	register_auto_exr()
	register_presets()
	register_matt()
	register_gnodes()
	register_nodes_menu()

def unregister_nodes():
	unregister_auto_exr()
	unregister_presets()
	unregister_matt()
	unregister_gnodes()
	unregister_nodes_menu()