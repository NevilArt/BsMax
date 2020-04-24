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

from .arrange import register_arrange,unregister_arrange
from .batchrename import register_batchrename,unregister_batchrename
from .clonearrayobjects import register_cloneobject,unregister_cloneobject
from .freeze import register_freeze,unregister_freeze
from .lattice import register_lattice,unregister_lattice
from .pivotpoint import register_pivotpoint,unregister_pivotpoint

def register_object():
	register_arrange()
	register_batchrename()
	register_cloneobject()
	register_freeze()
	register_lattice()
	register_pivotpoint()

def unregister_object():
	unregister_arrange()
	unregister_batchrename()
	unregister_cloneobject()
	unregister_freeze()
	unregister_lattice()
	unregister_pivotpoint()