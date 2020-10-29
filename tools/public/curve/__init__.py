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
from .attach import register_attach,unregister_attach
from .chamfer import register_chamfer,unregister_chamfer
from .outline import register_outline,unregister_outline
from .boolean import register_boolean,unregister_boolean
from .divid import register_divid,unregister_divid
from .menu import register_menu,unregister_menu
from .weld import register_weld,unregister_weld
# from .panel import *

def register_curve():
	register_attach()
	register_chamfer()
	register_outline()
	register_boolean()
	register_divid()
	register_menu()
	register_weld()

def unregister_curve():
	unregister_attach()
	unregister_chamfer()
	unregister_outline()
	unregister_boolean()
	unregister_divid()
	unregister_menu()
	unregister_weld()