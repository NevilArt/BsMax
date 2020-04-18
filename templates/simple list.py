import bpy
from bui import *

class BUI_OT_SimpleDialog(Dialog):
	bl_idname = "bui.simplediaog"
	bl_label = "BUI Dialog"
	
	def setup(self):
		Button(self,text="Button",row=1)
		CheckButton(self,text="CheckButton",row=2)
		CheckBox(self,text="CheckBox",row=3)
		Label(self,text="Label",row=4)
		self.num = Numeric(self,default=10,row=5,onupdate=self.pr_set)
		rb = RadioButtons(self,row=6)
		rb.add("Radio1",column=0)
		rb.add("Radio2",column=1)
		rb.add("Radio3",column=2)
		tab = Tab(self,row=7)
		t1 = tab.add("Tab1")
		Label(t1,text="Tab 1 Label")
		t2 = tab.add("Tab2")
		Label(t2,text="Tab 2 Label")
		TextBox(self,text="TextBox",row=8)
		self.pb = ProgressBar(self,size=[240,30],percent=10,row=11)
		box = Box(self,row=10) # box combine the controlers to single one
		Button(box,text="0",row=0,column=1,onclick=self.btn_0)
		Button(box,text="50",row=0,column=2,onclick=self.btn_50)
		Button(box,text="100",row=0,column=3,onclick=self.btn_100)

	def pr_set(self):
		self.pb.percent = self.num.value.value
	def btn_0(self):
		self.pb.percent = 0
	def btn_50(self):
		self.pb.percent = 50
	def btn_100(self):
		self.pb.percent = 100

def register():
	bpy.utils.register_class(BUI_OT_SimpleDialog)

def unregister():
	bpy.utils.unregister_class(BUI_OT_SimpleDialog)

if __name__ == '__main__':
	register()
	bpy.ops.bui.simplediaog('INVOKE_DEFAULT')