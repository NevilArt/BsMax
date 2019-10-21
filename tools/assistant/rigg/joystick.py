import bpy
from bpy.types import Operator

def GetDimantion(obj):
	MinX, MaxX, MinY, MaxY = 0, 0, 0, 0
	for V in bpy.context.object.data.vertices:
		if MaxX < V.co[0]: MaxX = V.co[0]
		if MinX > V.co[0]: MinX = V.co[0]
		if MaxY < V.co[1]: MaxY = V.co[1]
		if MinY > V.co[1]: MinY = V.co[1]
	return (MinX, MaxX, MinY, MaxY)

# Create Joystick function
def CreateJoystick (Frame):
	# Convert Plane to a Wire frame #
	bpy.context.scene.objects.active = Frame
	bpy.ops.object.mode_set(mode = 'EDIT')
	bpy.ops.mesh.select_all(action='SELECT')
	bpy.ops.mesh.delete(type='ONLY_FACE')
	bpy.ops.object.mode_set(mode = 'OBJECT')
	# Get Joystick needed Data from plan #
	Dim = GetDimantion(Frame)
	Width = Dim[1] - Dim[0]
	Height = Dim[3] - Dim[2]
	# Calculate the joy stick or slider direction
	Mode = "J"
	Radius = (min(Width, Height)) / 10
	if Width < Height / 4:
		Mode, Radius = "V" , Width / 2
	elif Height < Width / 4:
		Mode, Radius = "H", Height / 2
	# Create Joystick handle #
	bpy.ops.mesh.primitive_circle_add(radius= Radius, location=(0, 0, 0))
	Joy = bpy.context.scene.objects.active
	Joy.select = True
	bpy.context.scene.objects.active = Frame
	# Set Limit Controlers
	bpy.context.scene.objects.active = Joy
	bpy.ops.object.constraint_add(type='LIMIT_LOCATION')
	Joy.constraints["Limit Location"].use_min_x = True
	Joy.constraints["Limit Location"].use_max_x = True
	Joy.constraints["Limit Location"].min_x = Dim[0] + Radius
	Joy.constraints["Limit Location"].max_x = Dim[1] - Radius
	Joy.constraints["Limit Location"].use_min_y = True
	Joy.constraints["Limit Location"].use_max_y = True
	Joy.constraints["Limit Location"].min_y = Dim[2] + Radius
	Joy.constraints["Limit Location"].max_y = Dim[3] - Radius
	Joy.constraints["Limit Location"].use_min_z = True
	Joy.constraints["Limit Location"].use_max_z = True
	bpy.ops.object.constraint_add(type='CHILD_OF')
	Joy.constraints["Child Of"].target = Frame

class BsMax_TO_JoyStickCreator(Operator):
	bl_idname = "bsmax.joystickcreator"
	bl_label = "Joystick Creator"
	def execute(self, contecxt):
		# Collect Framable object from selected objects #
		Frames = []
		if bpy.context.mode == 'OBJECT':
			for obj in bpy.context.selected_objects:
				if obj.type == 'MESH':
					if(len(bpy.data.meshes[obj.name].vertices)) == 4:
						X, Y, Z = 0, 0, 0
						for i in range(0,3):
							X += abs(bpy.data.meshes[obj.name].vertices[i].co[0])
							Y += abs(bpy.data.meshes[obj.name].vertices[i].co[1])
							Z += abs(bpy.data.meshes[obj.name].vertices[i].co[2])
						if (X != 0 and Y != 0 and Z < (X + Y) / 10.0): Frames.append(obj)
		# apply to all selected frame after filtering
		for F in Frames: CreateJoystick(F)
		return{"FINISHED"}

def joystick_cls(register):
	classes = [BsMax_TO_JoyStickCreator]
	for c in classes:
		if register: bpy.utils.register_class(c)
		else: bpy.utils.unregister_class(c)
	return classes

if __name__ == '__main__':
	joystick_cls(True)

__all__ = ["joystick_cls"]