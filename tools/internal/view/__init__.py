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

from .droptool import register_droptool,unregister_droptool
from .filebrowser import register_filebrowser,unregister_filebrowser
from .floate_ditor import register_float_editor,unregister_float_editor
from .gride import register_gride, unregister_gride
# from .hold import register_hold,unregister_hold
from .undo import register_undo,unregister_undo
from .view3d import register_view3d,unregister_view3d
from .viewport import register_viewport,unregister_viewport
from .viewportbg import register_viewportbg,unregister_viewportbg

def register_view(preferences):
	register_droptool(preferences)
	register_filebrowser()
	register_float_editor()
	register_undo(preferences)
	register_gride()
	register_view3d()
	register_viewport()
	register_viewportbg()

def unregister_view():
	unregister_droptool()
	unregister_filebrowser()
	unregister_float_editor()
	unregister_undo()
	unregister_gride()
	unregister_view3d()
	unregister_viewport()
	unregister_viewportbg()