import bpy
from bpy.app.handlers import persistent

@persistent
def frame_Update(scene):
	pass

def frameupdate_cls(register):
	if register:
		bpy.app.handlers.frame_change_post.append(frame_Update)
	else:
		pass # remove the handler

if __name__ == '__main__':
	frameupdate_cls(True)

__all__ = ["frameupdate_cls"]