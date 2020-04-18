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

import bpy,sys
from os import path
from glob import glob
from bpy.types import Menu, Operator

tmpdir = path.dirname(__file__)
tmplst = [path.splitext(path.basename(f))[0] for f in glob(tmpdir+"/*.py")]
tmplst.remove('__init__')

class BUI_OT_Template(Operator):
	bl_idname = "bui.template"
	bl_label = "BUI Template"
	name: bpy.props.StringProperty()
	def execute(self, ctx):
		fname = tmpdir + "/" + self.name + ".py"
		if path.exists(fname):
			text = open(fname).read()
			ctx.window_manager.clipboard = text
			bpy.ops.text.new()
			bpy.data.texts[-1].name = self.name.capitalize()
			bpy.ops.text.paste()
		return{"FINISHED"}

class BUI_MT_Samples(Menu):
	bl_idname = "BUI_MT_samplesmenu"
	bl_label = "BUI"
	def draw(self,ctx):
		for name in tmplst:
			self.layout.operator("bui.template",text=name.capitalize()).name=name

def Menu_CallBack(self,ctx):
	self.layout.menu("BUI_MT_samplesmenu")

classes = [BUI_MT_Samples,BUI_OT_Template]
def register():
	for c in classes:
		bpy.utils.register_class(c)
	bpy.types.TEXT_MT_templates.prepend(Menu_CallBack)

def unregister():
	for c in classes:
		bpy.utils.unregister_class(c)
	bpy.types.TEXT_MT_templates.remove(Menu_CallBack)

__all__ = ["register","unregister"]

if __name__ == "__main__":
	register()