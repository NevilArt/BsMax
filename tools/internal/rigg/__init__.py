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

from .alignment import register_alignment, unregister_alignment
from .attach import register_attach, unregister_attach
from .bendy_bone import register_bendy_bone, unregister_bendy_bone
from .joystick import register_joystic, unregister_joystic
from .menu import register_menu, unregister_menu
from .naming import register_naming, unregister_naming
from .shapekey import register_shapekey, unregister_shapekey
from .wire_parameter import register_wire_parameter, unregister_wire_parameter



def register_rigg():
	register_alignment()
	register_attach()
	register_bendy_bone()
	register_joystic()
	register_menu()
	register_naming()
	register_shapekey()
	register_wire_parameter()



def unregister_rigg():
	unregister_alignment()
	unregister_attach()
	unregister_bendy_bone()
	unregister_joystic()
	unregister_menu()
	unregister_naming()
	unregister_shapekey()
	unregister_wire_parameter()
