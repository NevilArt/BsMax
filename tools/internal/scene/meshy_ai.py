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
import re

from bpy.types import Operator
from bpy.utils import register_class, unregister_class




def clean_text(text):
    text = text.replace("_", " ").replace("-", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def fix_object_name(obj):
	name = obj.name



class Scene_OT_MeshyAI_FBX_Clean(Operator):
	bl_idname = 'scene.meshy_ai_fbx_clean'
	bl_label = "Meshy AI FBX Clean"
	bl_description = ""
	bl_options = {'REGISTER'}

	def draw(self, context):
		pass

	def execute(self, context):

		return{'FINISHED'}

	
	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)


classes = {
	Scene_OT_MeshyAI_FBX_Clean
}

def register_meshy_ai():
	for cls in classes:
		register_class(cls)

def unregister_meshy_ai():
	
	for cls in classes:
		unregister_class(cls)

if __name__ == '__main__':
	register_meshy_ai()