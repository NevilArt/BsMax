import bpy
from bpy.types import Operator

class BsMax_OT_SelectInstance(Operator):
	bl_idname = "bsmax.select_instance"
	bl_label = "Select Instance"
	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return len(ctx.selected_objects) > 0
		return False
	def execute(self, ctx):
		if ctx.active_object != None and len(ctx.selected_objects) == 1:
			for obj in ctx.scene.objects:
				if ctx.active_object.data == obj.data:
					obj.select_set(True)
		return{"FINISHED"}

def BsMax_ReadPrimitiveData(obj):
	params = []
	if obj != None:
		params = obj.PrimitiveData.split(' ,')
	return params

class BsMax_OT_SelectSimilar(Operator):
	bl_idname = "bsmax.select_similar"
	bl_label = "Select Similar"
	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return len(ctx.selected_objects) > 0
		return False
	def execute(self, ctx):
		matt,clss,inst,subcls = [],[],[],[]
		if ctx.active_object != None and len(ctx.selected_objects) == 1:
			me = ctx.active_object
			for obj in ctx.scene.objects:
				if me != obj:
					# Collect instances
					if me.data == obj.data:
						inst.append(obj)
					# type and sub types
					if me.type == obj.type:
						clss.append(obj)
						if me.type in ['MESH','CURVE']:
							if me.data.primitivedata.classname != "":
								mecls = me.data.primitivedata.classname
								objcls = obj.data.primitivedata.classname
								if mecls == objcls:
									subcls.append(obj)
							# Material
							if me.data.materials == obj.data.materials:
								matt.append(obj)	
						if me.type == 'EMPTY':
							if me.empty_display_type == obj.empty_display_type:
								subcls.append(obj)
						if me.type == 'LIGHT':
							if me.data.type == obj.data.type:
								subcls.append(obj)
		if len(matt) > 0:
			for o in matt:
				o.select_set(True)
		elif len(subcls) > 0:
			for o in subcls:
				o.select_set(True)
		elif len(clss) > 0:
			for o in clss:
				o.select_set(True)
		elif len(inst) > 0:
			for o in inst:
				o.select_set(True)
		return{"FINISHED"}

def select_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("bsmax.select_instance")
	layout.operator("bsmax.select_similar")

def selection_cls(register):
	classes = [BsMax_OT_SelectInstance, BsMax_OT_SelectSimilar]

	if register:
		[bpy.utils.register_class(c) for c in classes]
		bpy.types.VIEW3D_MT_select_object.append(select_menu)
	else:
		bpy.types.VIEW3D_MT_select_object.remove(select_menu)
		[bpy.utils.unregister_class(c) for c in classes]

if __name__ == '__main__':
	selection_cls(True)

__all__ = ["selection_cls"]