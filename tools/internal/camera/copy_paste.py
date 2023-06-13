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

from bpy.types import Operator



class FloatKey:
	def __init__(self):
		self.frame = 0
		self.value = 0
		self.type = None
	
	def from_string(self, string, pick):
		field = string.split(',')
		self.frame = int(field[0])
		self.value = float(field[pick])

	def to_string(self):
		return ""
	


class TransformKey:
	def __init__(self):
		self.frame = 0

		self.px = 0
		self.py = 0
		self.pz = 0

		self.rx = 0
		self.ry = 0
		self.rz = 0

		# scale has no use for camera
		self.sx = 1
		self.sy = 1
		self.sz = 1
	
	def from_string(self, string):
		field = string.split(',')

		self.frame = int(field[0])

		self.px = float(field[1])
		self.py = float(field[2])
		self.pz = float(field[3])

		self.rx = float(field[4])
		self.ry = float(field[5])
		self.rz = float(field[6])

	def to_string(self):
		return ""



"""
# Field format
# line0 = identefyKey
# line1 = camera name
# line2 = scene name
#             0           1         2
# line3 = startFrame, endFrame, frameRate
# line4+ data fields
#   0     1   2   3   4   5   6   7    8
# frame, px, py, pz, rx, ry, rz, fov, lens
"""
class ClipboardCameraAnimation:
	def __init__(self):
		self.identefyKey = "3DSMAXTOCLIPBOARNEVILDCAMERACOPYPASTDATAVERSION02"
		self.cameraName = "Camera"
		self.sequenceName = "Sequence"
		self.startFrame = 0
		self.endFrame = 250
		self.frameRate = 25
		self.fov = []
		self.lens = []
		self.transform = []

	def read_clipboard(self):
		cb = bpy.context.window_manager.clipboard
		text = cb.get_clipboard_text()
		lines = text.splitlines()

		# ignore if data not detected
		if not lines:
			return False

		# ignore if ID key not detcted
		if lines[0] != self.identefyKey:
			return False
		
		# read camera and sequence name
		self.cameraName = lines[1]
		self.sequenceName = lines[2]
		
		# read sequence settings
		field = lines[3].split(',')
		self.startFrame = int(field[0])
		self.endFrame = int(field[1])
		self.frameRate = int(field[2])
		
		# read keyframes
		for line in lines[4:]:
			newLens = FloatKey()
			newLens.from_string(line, 7)
			self.lens.append(newLens)
			
			newFov = FloatKey()
			newFov.from_string(line, 8)
			self.fov.append(newFov)
					
			newTransformKey = TransformKey()
			newTransformKey.from_string(line)
			self.transform.append(newTransformKey)
		
		# return True if camera succesfully created
		return True



def create_camera(cameraData):
	camera_data = bpy.data.cameras.new(name=cameraData.cameraName)
	camera_object = bpy.data.objects.new(cameraData.cameraName, camera_data)
	bpy.context.scene.collection.objects.link(camera_object)

	for transform in cameraData.transform:
		print(transform)

	return camera_object


def paste_camera_from_clipboard():
	cameraData = ClipboardCameraAnimation()
	cameraData.read_clipboard()
	create_camera(cameraData)


class Camera_OT_Copy(Operator):
	bl_idname = "camera.copy"
	bl_label = "Copy Camera"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, ctx):
		return ctx.mode == "OBJECT"
	
	def execute(self, ctx):
		
		return{"FINISHED"}



class Camera_OT_Paste(Operator):
	bl_idname = "camera.paste"
	bl_label = "Paste Camera"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return ctx.mode == "OBJECT"
	
	def execute(self, ctx):
		
		return{"FINISHED"}



classes = (
    Camera_OT_Copy,
    Camera_OT_Paste
)

def register_copy_past():
	for c in classes:
		bpy.utils.register_class(c)

def unregister_copy_past():
	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == "__main__":
	register_copy_past()