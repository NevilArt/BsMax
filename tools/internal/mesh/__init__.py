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
from .meshs import register_meshs, unregister_meshs
from .edit import register_edit, unregister_edit
from .loop import register_loop, unregister_loop
from .outline import register_outline, unregister_outline
from .select import register_select, unregister_select
from .weld import register_weld, unregister_weld

def register_mesh():
	register_attach()
	register_edit()
	register_loop()
	register_meshs()
	register_outline()
	register_select()
	register_weld()

def unregister_mesh():
	unregister_attach()
	unregister_edit()
	unregister_loop()
	unregister_meshs()
	unregister_outline()
	unregister_select()
	unregister_weld()