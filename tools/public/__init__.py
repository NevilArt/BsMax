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

from .animation import register_animation,unregister_animation
from .armature import register_armature,unregister_armature
from .camera import register_camera,unregister_camera
from .curve import register_curve,unregister_curve
# from .font import 
from .ligth import register_light,unregister_light
from .mesh import register_mesh,unregister_mesh
from .object import register_object,unregister_object
from .render import register_render,unregister_render
from .select import register_select,unregister_select
from .transform import register_transform,unregister_transform
from .uv import register_uv,unregister_uv
from .view import register_view,unregister_view

from .rigg import register_rigg,unregister_rigg
from .menu import register_menu,unregister_menu

def register_public(preferences):
	register_animation()
	register_armature()
	register_camera()
	register_curve()
	register_light()
	register_mesh()
	register_object()
	register_render()
	register_select()
	register_transform()
	register_uv()
	register_view(preferences)
	register_rigg()
	register_menu()

def unregister_public():
	unregister_animation()
	unregister_armature()
	unregister_camera()
	unregister_curve()
	unregister_light()
	unregister_mesh()
	unregister_object()
	unregister_render()
	unregister_select()
	unregister_transform()
	unregister_uv()
	unregister_view()
	unregister_rigg()
	unregister_menu()