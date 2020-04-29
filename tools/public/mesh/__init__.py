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

from .meshs import register_meshs,unregister_meshs
from .smartcreate import register_smartcreate,unregister_smartcreate
from .smartloop import register_smartloop,unregister_smartloop
from .smartring import register_smartring,unregister_smartring
from .select import register_select,unregister_select
from .weld import register_weld,unregister_weld

def register_mesh():
	register_meshs()
	register_smartcreate()
	register_smartloop()
	register_smartring()
	register_select()
	register_weld()

def unregister_mesh():
	unregister_meshs()
	unregister_smartcreate()
	unregister_smartloop()
	unregister_smartring()
	unregister_select()
	unregister_weld()