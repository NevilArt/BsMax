#####################################
#	SMA YN Make Ready for Render
#	Base on EEVEE
#	Version 1.0.8 2021-09-10
#	
#	How to use:
#		Open Blender scene.
#		Open and apply this script.
#	Scene file naming rule:
#	(Short Name) + _ + 'B' + (Episod Number) + _ + (Scene Name) + _ + ('Render') + _ + (Number)
#		Example:
#			YN_B02_S17_Render_07.blend
#			YN_B02_S05Ek2_Render_03.blend
#			YN_B02_S07B_Render_00_rev.blend
#	What the script does:
#		Set Render Preset.
#		Creat out put pathes.
#		Check and Fix light setting and count (Sun).
#		Check and Fix Camera Setting.
#		Check and Fix Meta data setting.
#		Set Passes Mist/Mask.
#		Create Composit node setup and passes out puts.
#####################################


import bpy

from bpy.types import Operator



def get_node_name(node):
	newName = ""
	for l in node.name.lower():
		if l in "abcdefghijklmnopqrstuvwxyz0123456789":
			newName += l
	return newName



def get_node_location(node):
	x = int(node.location.x)
	y = int(node.location.y)
	return str(x) + ", " + str(y)


def get_inputs_as_string(node):
	string = ""
	for index, input in enumerate(node.inputs):
		string += "inputs[" + str(index) +"].default_value = "
		string += str(input.default_value)
		string += "\n"
	return string


def math_node_to_string(node):
	string = "operation = '" + node.operation + "'\n"
	string += get_inputs_as_string(node)
	return string


def node_to_script(node):
	script = get_node_name(node) + " = gn.new_node("
	script += node.bl_idname + ", "
	script += get_node_location(node) + ", "
	script += ")\n"
	
	if node.type == 'MATH':
		script += math_node_to_string(node)
	
	return script
	


def print_active_node_tree(ctx):
	if not ctx.object:
		return
	
	active = ctx.object.modifiers.active
	if not active:
		return
	
	if active.type != 'NODES':
		return
	
	node_group = active.node_group
	nodes = node_group.nodes

	# print("--<<Nodes>>--")
	for node in nodes:
		print(node_to_script(node))
	
	# print("--<<Linkes>>--")




class Nevil_OT_Print_Active_GeoNode(Operator):
	bl_idname = "nevil.print_active_geonode"
	bl_label = "Print Active Geo Nodes (Nevil)"
	bl_description = ""
	bl_options = {'REGISTER'}

	def execute(self, ctx):
		print_active_node_tree(ctx)
		return{"FINISHED"}



classes = (
	Nevil_OT_Print_Active_GeoNode,
)



def register_geometry_node_tools():
	for c in classes:
		bpy.utils.register_class(c)



def unregister_geometry_node_tools():
	for c in classes:
		bpy.utils.unregister_class(c)



if __name__ == '__main__':
	register_geometry_node_tools()