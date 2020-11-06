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
from .clip_editor import register_clip_editor,unregister_clip_editor
from .curve import register_curve,unregister_curve
from .ligth import register_light,unregister_light
from .material import register_material,unregister_material
from .mesh import register_mesh,unregister_mesh
from .modifier import register_modifier,unregister_modifier
from .object import register_object,unregister_object
from .particle import register_particle,unregister_particle
from .render import register_render,unregister_render
from .select import register_select,unregister_select
from .text import register_text,unregister_text
from .transform import register_transform,unregister_transform
from .uv import register_uv,unregister_uv
from .view import register_view,unregister_view

from .rigg import register_rigg,unregister_rigg
from .menu import register_menu,unregister_menu

def register_public(preferences):
	register_animation()
	register_armature()
	register_camera()
	register_clip_editor()
	register_curve()
	register_light()
	register_material()
	register_mesh()
	register_modifier()
	register_object(preferences)
	register_particle()
	register_render()
	register_select()
	register_text()
	register_transform()
	register_uv()
	register_view(preferences)
	register_rigg()
	register_menu()

def unregister_public():
	unregister_animation()
	unregister_armature()
	unregister_camera()
	unregister_clip_editor()
	unregister_curve()
	unregister_light()
	unregister_material()
	unregister_mesh()
	unregister_modifier()
	unregister_object()
	unregister_particle()
	unregister_render()
	unregister_select()
	unregister_text()
	unregister_transform()
	unregister_uv()
	unregister_view()
	unregister_rigg()
	unregister_menu()