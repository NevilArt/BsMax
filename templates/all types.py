import bpy
from bui import Dialog,Label,Button,Numeric,TextBox,CheckBox,RadioButtons,CheckButton,Tab,Box

class BUI_OT_Types(Dialog):
	bl_idname = "bui.types"
	bl_label = "BUI Types"
	
	def setup(self):
		""" Create tabs """
		self.tab = Tab(self)
		self.tab1 = self.tab.add("Button")
		self.tab2 = self.tab.add("TextBox")
		self.tab3 = self.tab.add("Numeric")
		self.tab4 = self.tab.add("CheckBox")
		self.tab5 = self.tab.add("RadioButtons")

		""" Button tab """
		self.btn1 = Button(self.tab1,text="Add Cube",column=1,row=1,onclick=self.btn1_clicked)
		self.btn2 = Button(self.tab1,text="Add Sphere",column=2,row=1,onclick=self.btn2_clicked)
		self.btn3 = Button(self.tab1,text="Add Monkey",column=3,row=1,onclick=self.btn3_clicked)
		self.cbtn1 = CheckButton(self.tab1,text="Check 01",column=1,row=2)
		self.cbtn2 = CheckButton(self.tab1,text="Check 02",column=2,row=2)
		self.cbtn3 = CheckButton(self.tab1,text="Check 03",column=3,row=2)

		""" TextBox tab """
		btnbox = Box(self.tab2,column=1,row=2)
		self.tb_clear = Button(btnbox,text="Clear",column=1,row=3,onclick=self.tb_clear_clicked)
		self.tb_fill = Button(btnbox,text="Fill",column=2,row=3,onclick=self.tb_fill_clicked)
		tbbox = Box(self.tab2,column=1,row=1)
		self.tb1 = TextBox(tbbox,size=[200,30],column=1,row=1)
		self.tb2 = TextBox(tbbox,size=[200,30],column=1,row=2)
		self.tb3 = TextBox(tbbox,size=[200,30],column=1,row=3)

		""" Numeric tab """
		self.num1 = Numeric(self.tab3,size=[120,30],minimum=0,maximum=100,default=0,column=1,row=1)
		self.num2 = Numeric(self.tab3,size=[120,30],minimum=0,maximum=100,default=50,column=2,row=1)
		self.num3 = Numeric(self.tab3,size=[120,30],minimum=0,maximum=100,default=100,column=3,row=1)
		self.num_reset = Button(self.tab3,text="Reset",column=1,row=2,onclick=self.num_reset_clicked)

		""" Checkbox """
		self.cb11 = CheckBox(self.tab4,text="Check 1",column=1,row=1)
		self.cb12 = CheckBox(self.tab4,text="Check 2",column=2,row=1)
		self.cb13 = CheckBox(self.tab4,text="Check 3",column=3,row=1)
		self.cb21 = CheckBox(self.tab4,text="Check 4",column=1,row=2)
		self.cb22 = CheckBox(self.tab4,text="Check 5",column=2,row=2)
		self.cb23 = CheckBox(self.tab4,text="Check 6",column=3,row=2)
		self.cb31 = CheckBox(self.tab4,text="Check 7",column=1,row=3)
		self.cb32 = CheckBox(self.tab4,text="Check 8",column=2,row=3)
		self.cb33 = CheckBox(self.tab4,text="Check 9",column=3,row=3)

		self.cbs = [self.cb11,self.cb12,self.cb13,self.cb21,self.cb22,self.cb23,self.cb31,self.cb32,self.cb33]

		self.cb_none = Button(self.tab4,text="None",column=1,row=4,onclick=self.cb_none_clicked)
		self.cb_all = Button(self.tab4,text="All",column=2,row=4,onclick=self.cb_all_clicked)
		self.cb_invert = Button(self.tab4,text="Invert",column=3,row=4,onclick=self.cb_invert_clicked)
				
		""" RadioButtons """
		self.radioLabel1 = Label(self.tab5,text="Verticl",column=1,row=1)
		self.radio1 = RadioButtons(self.tab5,column=1,row=2)
		self.radio1.add(text="radio A 01",column=1,row=1)
		self.radio1.add(text="radio A 02",column=1,row=2)
		self.radio1.add(text="radio A 03",column=1,row=3)
		self.radio1.add(text="radio A 04",column=1,row=4)

		self.rgap2 = Box(self.tab5,size=[0,10],column=1,row=3)
		self.rlabel2 = Label(self.tab5,text="Horisontal",column=1,row=4)

		self.radio2 = RadioButtons(self.tab5,column=1,row=5)
		self.radio2.add(text="radio B 01",column=2,row=5)
		self.radio2.add(text="radio B 02",column=3,row=5)
		self.radio2.add(text="radio B 03",column=4,row=5)
		self.radio2.add(text="radio B 04",column=5,row=5)

		self.rgap3 = Box(self.tab5,size=[0,10],column=1,row=6)
		self.rlabel3 = Label(self.tab5,text="Sheet",column=1,row=7)

		self.radio3 = RadioButtons(self.tab5,column=1,row=8)
		self.radio3.add(text="radio C 11",column=1,row=1)
		self.radio3.add(text="radio C 21",column=2,row=1)
		self.radio3.add(text="radio C 31",column=3,row=1)
		self.radio3.add(text="radio C 12",column=1,row=2)
		self.radio3.add(text="radio C 22",column=2,row=2)
		self.radio3.add(text="radio C 32",column=3,row=2)
		self.radio3.add(text="radio C 13",column=1,row=3)
		self.radio3.add(text="radio C 23",column=2,row=3)
		self.radio3.add(text="radio C 33",column=3,row=3)

	def btn1_clicked(self):
		bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, location=(0, 0, 0))


	def btn2_clicked(self):
		bpy.ops.mesh.primitive_uv_sphere_add(enter_editmode=False, location=(0, 0, 0))


	def btn3_clicked(self):
		bpy.ops.mesh.primitive_monkey_add(size=2, enter_editmode=False, location=(0, 0, 0))

	def tb_clear_clicked(self):
		tbs = [self.tb1,self.tb2,self.tb3]
		for tb in tbs:
			tb.text = ""

	def tb_fill_clicked(self):
		self.tb1.text = "TextBox1"
		self.tb2.text = "TextBox2"
		self.tb3.text = "TextBox3"

	def num_reset_clicked(self):
		self.num1.value.reset()
		self.num2.value.reset()
		self.num3.value.reset()

	def cb_none_clicked(self):
		for cb in self.cbs:
			cb.checked = False

	def cb_all_clicked(self):
		for cb in self.cbs:
			cb.checked = True

	def cb_invert_clicked(self):
		for cb in self.cbs:
			cb.checked = not cb.checked

if __name__ == '__main__':
	bpy.utils.register_class(BUI_OT_Types)
	bpy.ops.bui.types('INVOKE_DEFAULT')