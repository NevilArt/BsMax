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

# from .make_ready_render_v1 import (
# 	register_make_ready_render_v1, unregister_make_ready_render_v1
# )

# from .make_render_ready_v2 import (
# 	register_make_ready_render_v2, unregister_make_ready_render_v2
# )

from .make_render_ready_v3 import (
	register_make_ready_render_v3, unregister_make_ready_render_v3
)


def register_pipeline(preferences):
	if preferences.nevil_stuff:
		# register_make_ready_render_v1()
		# register_make_ready_render_v2()
		register_make_ready_render_v3()


def unregister_pipeline():
	# unregister_make_ready_render_v1()
	# unregister_make_ready_render_v2()
	unregister_make_ready_render_v3()
