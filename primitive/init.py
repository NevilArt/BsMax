from .ui import *
from .panel import *
from .update import *
# # Meshes
from .box import *
from .capsule import *
from .cylinder import *
from .icosphere import *
from .mesher import *
from .monkey import *
from .plane import *
from .pyramid import *
from .sphere import *
from .tube import *
from .torus import *
from .vertex import *
# # Curves
from .arc import *
from .circle import *
from .ellipse import *
from .extrude import *
from .donut import *
from .ngon import *
from .helix import *
from .line import *
#from .logo import *
from .profilo import *
from .rectangle import *
from .star import *
# # Others
from .bone import *
from .effector import *
from .empty import *
from .camera import *
from .lattice import *
from .light import *
from .lightprobe import *
from .metaball import *
from .speaker import *
from .text import *
from .greacepencil import *

# UI
from .createmenu import *

def primitive_cls(register, pref):
	update_cls(register)
	ui_cls(register)
	panel_cls(register)
	arc_cls(register)
	box_cls(register)
	bone_cls(register)
	capsule_cls(register)
	camera_cls(register)
	circle_cls(register)
	createmenu_cls(register)
	cylinder_cls(register)
	donut_cls(register)
	effector_cls(register)
	ellipse_cls(register)
	empty_cls(register)
	extrude_cls(register)
	greacepencil_cls(register)
	helix_cls(register)
	icosphere_cls(register)
	lattice_cls(register)
	light_cls(register)
	lightprobe_cls(register)
	line_cls(register)
	#logo_cls(register)
	mesher_cls(register)
	metaball_cls(register)
	monkey_cls(register)
	ngon_cls(register)
	plane_cls(register)
	profilo_cls(register)
	pyramid_cls(register)
	rectangle_cls(register)
	speaker_cls(register)
	sphere_cls(register)
	star_cls(register)
	text_cls(register)
	torus_cls(register)
	tube_cls(register)
	vertex_cls(register)
	if pref.assistpack == "Rigg":
		# import and register rigg primitives
		pass

__all__ = ["primitive_cls"]