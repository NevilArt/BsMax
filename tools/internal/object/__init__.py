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

from .arrange import register_arrange, unregister_arrange
from .attach import register_attach, unregister_attach
# from .bake import register_bake, unregister_bake
from .batchrename import register_batchrename, unregister_batchrename
from .clonearrayobjects import register_cloneobject, unregister_cloneobject
from .collection import register_collection, unregister_collection
from .convert import register_convert, unregister_convert
from .create import register_create, unregister_create
from .freeze import register_freeze, unregister_freeze
from .lattice import register_lattice, unregister_lattice
from .link_to import register_link_to, unregister_link_to
from .objectproperties import register_objectproperties, unregister_objectproperties
from .pivot_point import register_pivot_point, unregister_pivot_point
from .subobject_level import register_subobject_level, unregister_subobject_level

def register_object(preferences):
	register_arrange()
	register_attach()
	# register_bake()
	register_batchrename()
	register_cloneobject()
	register_collection()
	register_convert()
	register_create()
	register_freeze()
	register_lattice(preferences)
	register_link_to()
	register_objectproperties()
	register_pivot_point()
	register_subobject_level()

def unregister_object():
	unregister_arrange()
	unregister_attach()
	# unregister_bake()
	unregister_batchrename()
	unregister_cloneobject()
	unregister_collection()
	unregister_convert()
	unregister_create()
	unregister_freeze()
	unregister_lattice()
	unregister_link_to()
	unregister_objectproperties()
	unregister_pivot_point()
	unregister_subobject_level()