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
from .coordinate import register_coordinate,unregister_coordinate
from .dragclone import register_dragclone,unregister_dragclone
from .floateditor import register_floateditor,unregister_floateditor
from .hold import register_hold,unregister_hold
from .menu import register_menu,unregister_menu
from .modifier import register_modifier,unregister_modifier
from .navigation import register_navigation,unregister_navigation
# from .objectproperties import *
from .snap import register_snap,unregister_snap
from .subobjectlevel import register_subobjectlevel,unregister_subobjectlevel
from .transform import register_transform,unregister_transform
from .viewport import register_viewport,unregister_viewport
from .viewportbg import register_viewportbg,unregister_viewportbg

def register_max():
	register_attach()
	register_coordinate()
	register_dragclone()
	register_floateditor()
	register_hold()
	register_menu()
	register_modifier()
	# register_navigation()
	register_snap()
	register_subobjectlevel()
	register_transform()
	register_viewport()
	register_viewportbg()

def unregister_max():
	unregister_attach()
	unregister_coordinate()
	unregister_dragclone()
	unregister_floateditor()
	unregister_hold()
	unregister_menu()
	unregister_modifier()
	# unregister_navigation()
	unregister_snap()
	unregister_subobjectlevel()
	unregister_transform()
	unregister_viewport()
	unregister_viewportbg()