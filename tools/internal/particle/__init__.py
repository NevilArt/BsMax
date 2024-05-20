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
from .hair_cache import register_hair_cache, unregister_hair_cache
from .hair_guide import register_hair_guide, unregister_hair_guide
from .mesh_to_hair import register_mesh_to_hair, unregister_mesh_to_hair
from .paint import register_paint, unregister_paint

def register_particle():
	register_hair_cache()
	register_hair_guide()
	register_mesh_to_hair()
	register_paint()

def unregister_particle():
	unregister_hair_cache()
	unregister_hair_guide()
	unregister_mesh_to_hair()
	unregister_paint()