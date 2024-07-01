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

from .attach import register_attach, unregister_attach
from .boolean import register_boolean, unregister_boolean
from .chamfer import register_chamfer, unregister_chamfer
from .divid import register_divid, unregister_divid
from .menu import register_menu, unregister_menu
from .outline import register_outline, unregister_outline
from .selection import register_selection, unregister_selection
from .weld import register_weld, unregister_weld


def register_curve():
	register_attach() #Done
	register_boolean()
	register_chamfer()
	register_divid() #<<
	register_menu()
	register_outline() #DONE but need to refactor
	register_selection()
	register_weld()


def unregister_curve():
	unregister_attach()
	unregister_boolean()
	unregister_chamfer()
	unregister_divid()
	unregister_menu()
	unregister_outline()
	unregister_selection()
	unregister_weld()