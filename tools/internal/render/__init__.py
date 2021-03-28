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

from .backburner import register_backburner, unregister_backburner
from .light_lister import register_light_lister,unregister_light_lister
from .matt import register_matt, unregister_matt
from .preset import register_preset, unregister_preset
# from .quick_render import register_quick_render,unregister_quick_render

def register_render():
	register_backburner()
	register_light_lister()
	register_matt()
	register_preset()
	# register_quick_render()

def unregister_render():
	unregister_backburner()
	unregister_light_lister()
	unregister_matt()
	unregister_preset()
	# unregister_quick_render()