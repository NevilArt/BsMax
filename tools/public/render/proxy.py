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

import bpy
from bpy.app.handlers import persistent

def load_hi_res(scene):
	# for obj in scene.objects:
	# 	obj.hide_viewport = False
	print("Loaded")
	#proxy = bpy.context.active_object
	#proxy.hide_viewport = True
	bpy.ops.object.select_all(action='DESELECT')
	bpy.ops.wm.link(
		filepath="Xref.blend",
		directory="C:/Users/Nevil/Desktop/Xref.blend\\Object\\",
		filename="Monkey")
		#autoselect=True)
	#hires = bpy.context.active_object
	#hires.location = proxy.location

def restor_proxys(scene):
	print("Restore")
	# for obj in scene.objects:
	# 	pass
	# deltehei
	# unhide proxy
	pass

@persistent
def render_init(scene):
	load_hi_res(scene)

@persistent
def render_complete(scene):
	restor_proxys(scene)

@persistent
def render_cancel(scene):
	restor_proxys(scene)

# @persistent
# def render_pre(scene):
# 	print("render pre")

# @persistent
# def render_post(scene):
# 	print("render post")

# @persistent
# def render_stats(scene):
# 	print("render state")

# @persistent
# def render_write(scene):
# 	print("render write")

def register_proxy():
	handlers = bpy.app.handlers
	handlers.render_init.append(render_init)
	handlers.render_complete.append(render_complete)
	handlers.render_cancel.append(render_cancel)
	# handlers.render_pre.append(render_pre)
	# handlers.render_post.append(render_post)
	# handlers.render_stats.append(render_stats)
	# handlers.render_write.append(render_write)

def unregister_proxy():
	handlers = bpy.app.handlers
	handlers.render_init.remove(render_init)
	handlers.render_complete.remove(render_complete)
	handlers.render_cancel.remove(render_cancel)
	# handlers.render_pre.remove(render_pre)
	# handlers.render_post.remove(render_post)
	# handlers.render_stats.remove(render_stats)
	# handlers.render_write.remove(render_write)