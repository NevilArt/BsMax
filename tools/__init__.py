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

from .external import register_external, unregister_external
from .internal import register_internal, unregister_internal
from .special import register_special, unregister_special
from .pipeline import register_pipeline, unregister_pipeline
# from .patrion import register_patreon, unregister_patreon

def register_tools(preferences):
	register_external()
	register_internal(preferences)
	register_special(preferences)
	register_pipeline(preferences)
	# register_patreon()

def unregister_tools():
	unregister_external()
	unregister_internal()
	unregister_special()
	unregister_pipeline()
	# unregister_patreon()