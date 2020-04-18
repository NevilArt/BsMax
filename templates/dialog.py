import bpy
from bui import Dialog,Button,Numeric,TextBox,CheckBox

def btn2_clicked():
	bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, location=(0, 0, 0))

class BUI_OT_SimpleDialog(Dialog):
	bl_idname = "bui.simplediaog"
	bl_label = "BUI Dialog"
	
	def setup(self):
		self.btn1 = Button(self,text="Reset",size=[100,30],column=1,row=1)
		self.btn1.onclick = self.btn1_clicked

		self.btn2 = Button(self,text="Add a Cube",size=[100,30],column=2,row=1)
		self.btn2.onclick = btn2_clicked

		self.num1 = Numeric(self,size=[100,30],column=1,row=2)
		self.tb1 = TextBox(self,size=[100,30],column=1,row=3)
		self.tb2 = TextBox(self,size=[100,30],column=2,row=3)

	def btn1_clicked(self):
		self.num1.value.value = 20
		self.tb1.kb.str = "TextBox 01"
		self.tb2.kb.str = "TextBox 02"

def register():
	bpy.utils.register_class(BUI_OT_SimpleDialog)

def unregister():
	bpy.utils.unregister_class(BUI_OT_SimpleDialog)

if __name__ == '__main__':
	register()
	bpy.ops.bui.simplediaog('INVOKE_DEFAULT')