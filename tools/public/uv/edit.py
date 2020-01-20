import bpy
from bpy.types import Operator
from bpy.props import BoolProperty

class BsMax_OT_TurnUV(Operator):
	bl_idname = "uv.turn"
	bl_label = "Turn (UV)"
	ccw: BoolProperty(name= "CCW")
	@classmethod
	def poll(self, ctx):
		return True
	def execute(self, ctx):
		value = 1.5708 if self.ccw else -1.5708
		bpy.ops.transform.rotate(value=value,orient_axis='Z',orient_type='VIEW',
						orient_matrix=((-1,-0,-0),(-0,-1,-0),(-0,-0,-1)),
						orient_matrix_type='VIEW',mirror=True,
						use_proportional_edit=False,proportional_edit_falloff='SMOOTH',
						proportional_size=1,use_proportional_connected=False,
						use_proportional_projected=False)
		return{"FINISHED"}

def edit_cls(register):
	classes = [BsMax_OT_TurnUV]
	if register:
		[bpy.utils.register_class(c) for c in classes]
	else:
		[bpy.utils.unregister_class(c) for c in classes]

if __name__ == '__main__':
	edit_cls(True)

__all__ = ["edit_cls"]