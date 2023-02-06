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

from .ui import register_ui, unregister_ui
from .panel import register_panel, unregister_panel
from .update import register_update, unregister_update
# # Meshes
# from .adaptive_plane import register_adaptive_plane, unregister_adaptive_plane
from .box import register_box, unregister_box
from .capsule import register_capsule, unregister_capsule
from .cylinder import register_cylinder, unregister_cylinder
from .icosphere import register_icosphere, unregister_icosphere
from .monkey import register_monkey, unregister_monkey
from .oiltank import register_oiltank, unregister_oiltank
from .plane import register_plane, unregister_plane
from .pyramid import register_pyramid, unregister_pyramid
from .sphere import register_sphere, unregister_sphere
from .teapot import register_teapot, unregister_teapot
from .tube import register_tube, unregister_tube
from .torus import register_torus, unregister_torus
from .torusknot import register_torusknot, unregister_torusknot
from .vertex import register_vertex, unregister_vertex
# # Curves
from .arc import register_arc, unregister_arc
from .circle import register_circle, unregister_circle
from .ellipse import register_ellipse, unregister_ellipse
from .extrude import register_extrude, unregister_extrude
from .donut import register_donut, unregister_donut
from .ngon import register_ngon, unregister_ngon
from .helix import register_helix, unregister_helix
from .line import register_line, unregister_line
# from .logo import register_logo, unregister_logo
from .profilo import register_profilo, unregister_profilo
from .rectangle import register_rectangle, unregister_rectangle
from .star import register_star, unregister_star
# Others
from .bone import register_bone, unregister_bone
from .effector import register_effector, unregister_effector
from .empty import register_empty, unregister_empty
from .camera import register_camera, unregister_camera
from .lattice import register_lattice, unregister_lattice
from .light import register_light, unregister_light
from .lightprobe import register_lightprobe, unregister_lightprobe
from .metaball import register_metaball, unregister_metaball
from .speaker import register_speaker, unregister_speaker
from .text import register_text, unregister_text
from .greacepencil import register_greacepencil, unregister_greacepencil
# Extera
from .presets import register_preset, unregister_preset
# UI
from .menu import register_menu, unregister_menu

def register_primitives():
	register_update()
	register_ui()
	register_panel()
	# register_adaptive_plane()
	register_arc()
	register_box()
	register_bone()
	register_capsule()
	register_camera()
	register_circle()
	register_cylinder()
	register_donut()
	register_effector()
	register_ellipse()
	register_empty()
	register_extrude()
	register_greacepencil()
	register_helix()
	register_icosphere()
	register_lattice()
	register_light()
	register_lightprobe()
	register_line()
	#register_logo()
	register_menu()
	register_metaball()
	register_monkey()
	register_oiltank()
	register_ngon()
	register_plane()
	register_preset()
	register_profilo()
	register_pyramid()
	register_rectangle()
	register_speaker()
	register_sphere()
	register_star()
	register_text()
	register_teapot()
	register_torus()
	register_torusknot()
	register_tube()
	register_vertex()
	
def unregister_primitives():
	unregister_update()
	unregister_ui()
	unregister_panel()
	# unregister_adaptive_plane()
	unregister_arc()
	unregister_box()
	unregister_bone()
	unregister_capsule()
	unregister_camera()
	unregister_circle()
	unregister_cylinder()
	unregister_donut()
	unregister_effector()
	unregister_ellipse()
	unregister_empty()
	unregister_extrude()
	unregister_greacepencil()
	unregister_helix()
	unregister_icosphere()
	unregister_lattice()
	unregister_light()
	unregister_lightprobe()
	unregister_line()
	#unregister_logo()
	unregister_menu()
	unregister_metaball()
	unregister_monkey()
	unregister_oiltank()
	unregister_ngon()
	unregister_plane()
	unregister_preset()
	unregister_profilo()
	unregister_pyramid()
	unregister_rectangle()
	unregister_speaker()
	unregister_sphere()
	unregister_star()
	unregister_text()
	unregister_teapot()
	unregister_torus()
	unregister_torusknot()
	unregister_tube()
	unregister_vertex()