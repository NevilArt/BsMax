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

def proxy_cls(register):
	handlers = bpy.app.handlers
	if register:
		handlers.render_init.append(render_init)
		handlers.render_complete.append(render_complete)
		handlers.render_cancel.append(render_cancel)
		# handlers.render_pre.append(render_pre)
		# handlers.render_post.append(render_post)
		# handlers.render_stats.append(render_stats)
		# handlers.render_write.append(render_write)
	else:
		handlers.render_init.remove(render_init)
		handlers.render_complete.remove(render_complete)
		handlers.render_cancel.remove(render_cancel)
		# handlers.render_pre.remove(render_pre)
		# handlers.render_post.remove(render_post)
		# handlers.render_stats.remove(render_stats)
		# handlers.render_write.remove(render_write)

if __name__ == '__main__':
	proxy_cls(True)

__all__ = ["proxy_cls"]