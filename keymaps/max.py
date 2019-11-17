import bpy, rna_keymap_ui
from time import sleep
from _thread import start_new_thread

KeyMaps = []

def is_in_keymaps(key,keymaps):
	for k in keymaps:
		if key.idname == k[0]:
			if key.type == k[1] and key.value == k[2] and \
			   key.alt  == k[3] and key.ctrl  == k[4] and key.shift == k[5]:
			   return True
	return False

def set_extera_keymaps(space,keymaps,state):
	try:
		sleep(0.1)
		kdif = bpy.context.window_manager.keyconfigs.default
		km = kdif.keymaps[space]
		for k in km.keymap_items:
			if is_in_keymaps(k,keymaps):
				k.active = state
	except:
		pass
		#set_extera_keymaps(space,keymaps,state)

def max_dif_keys_set(state):
	# Disable/Enable Unwanted Default ShortKeys
	sks = []
		   #(    idname     ,   type  , value , alt ,ctrl ,shift)
	keys = [('view3d.select','LEFTMOUSE','CLICK',False,False,False),
			('view3d.select','LEFTMOUSE','CLICK',True ,False,False),
			('view3d.select','LEFTMOUSE','CLICK',False,True ,False),
			('view3d.select','LEFTMOUSE','CLICK',False,False,True )]
	sks.append(('3D View',keys))

	keys = [('wm.context_toggle','T','ANY',False,False,False)]
	sks.append(('3D View Generic',keys))

	keys = [('view3d.select_box','EVT_TWEAK_L','ANY',False,True,False)]
	sks.append(('3D View Tool: Select Box',keys))

	keys = [('view3d.select_circle','LEFTMOUSE','PRESS',False,True,False)]
	sks.append(('3D View Tool: Select Circle',keys))

	keys = [('view3d.select_lasso','EVT_TWEAK_L','ANY',False,True,False)]
	sks.append(('3D View Tool: Select Lasso',keys))

	keys = [('mesh.shortest_path_pick','LEFTMOUSE','CLICK',False,True,False)]
	sks.append(('Mesh',keys))

	keys = [('wm.quit_blender','Q','PRESS',False,True,False)]
	sks.append(('Window',keys))
	
	for space,keys in sks:
		set_extera_keymaps(space,keys,state)

def create_subobject_mode_keymap(km):
	kmi = km.keymap_items.new("bsmax.subobjectlevel","ONE","PRESS")
	kmi.properties.level = 1
	KeyMaps.append((km,kmi))
	kmi = km.keymap_items.new("bsmax.subobjectlevel","TWO","PRESS")
	kmi.properties.level = 2
	KeyMaps.append((km,kmi))
	kmi = km.keymap_items.new("bsmax.subobjectlevel","THREE","PRESS")
	kmi.properties.level = 3
	KeyMaps.append((km,kmi))
	kmi = km.keymap_items.new("bsmax.subobjectlevel","FOUR","PRESS")
	kmi.properties.level = 4
	KeyMaps.append((km,kmi))
	kmi = km.keymap_items.new("bsmax.subobjectlevel","FIVE","PRESS")
	kmi.properties.level = 5
	KeyMaps.append((km,kmi))
	kmi = km.keymap_items.new("bsmax.subobjectlevel","SIX","PRESS")
	kmi.properties.level = 6
	KeyMaps.append((km,kmi))
	kmi = km.keymap_items.new("bsmax.subobjectlevel","SEVEN","PRESS")
	kmi.properties.level = 7
	KeyMaps.append((km,kmi))
	kmi = km.keymap_items.new("bsmax.subobjectlevel","EIGHT","PRESS")
	kmi.properties.level = 8
	KeyMaps.append((km,kmi))
	kmi = km.keymap_items.new("bsmax.subobjectlevel","NINE","PRESS")
	kmi.properties.level = 9
	KeyMaps.append((km,kmi))
	kmi = km.keymap_items.new("bsmax.subobjectlevel","ZERO","PRESS")
	kmi.properties.level = 0
	KeyMaps.append((km,kmi))

def create_switch_view_keymap(km):
	kmi = km.keymap_items.new("view3d.view_persportho","P","PRESS")
	KeyMaps.append((km,kmi))
	kmi = km.keymap_items.new("view3d.view_axis","F","PRESS")
	kmi.properties.type = "FRONT"
	KeyMaps.append((km,kmi))
	kmi = km.keymap_items.new("view3d.view_axis","L","PRESS")
	kmi.properties.type = "LEFT"
	KeyMaps.append((km,kmi))
	kmi = km.keymap_items.new("view3d.view_axis","T","PRESS")
	kmi.properties.type = "TOP"
	KeyMaps.append((km,kmi))
	kmi = km.keymap_items.new("view3d.view_axis","B","PRESS")
	kmi.properties.type = "BOTTOM"
	KeyMaps.append((km,kmi))

def create_view3d_click_celection_keymap(km):
	kmi = km.keymap_items.new("view3d.select","LEFTMOUSE","CLICK")
	kmi.properties.deselect_all = True
	KeyMaps.append((km,kmi))
	kmi = km.keymap_items.new("view3d.select","LEFTMOUSE","CLICK",ctrl=True)
	kmi.properties.toggle = True
	KeyMaps.append((km,kmi))
	kmi = km.keymap_items.new("view3d.select","LEFTMOUSE","CLICK",alt=True)
	kmi.properties.deselect = True
	KeyMaps.append((km,kmi))

def create_view3d_tweak_selection_keymap(km):
	kmi = km.keymap_items.new("view3d.select_box","EVT_TWEAK_L","ANY")
	kmi.properties.mode = 'SET'
	KeyMaps.append((km,kmi))
	kmi = km.keymap_items.new("view3d.select_box","EVT_TWEAK_L","ANY",ctrl=True )
	kmi.properties.mode = 'ADD'
	KeyMaps.append((km,kmi))
	kmi = km.keymap_items.new("view3d.select_box","EVT_TWEAK_L","ANY",alt=True )
	kmi.properties.mode = 'SUB'
	KeyMaps.append((km,kmi))


# Create Keymaps
def create_3dsmax_keymaps():
	kcfg = bpy.context.window_manager.keyconfigs.addon
	if kcfg:
		# Window ---------------------------------------------------------------
		km = kcfg.keymaps.new(name ='Window',space_type ='EMPTY')

		kmi = km.keymap_items.new("wm.search_menu","X","PRESS")
		KeyMaps.append((km,kmi))

		# 2D View --------------------------------------------------------------
		# km = kcfg.keymaps.new(name='View2D',space_type='EMPTY',region_type='WINDOW')

		# kmi = km.keymap_items.new("view2d.zoom","MIDDLEMOUSE","PRESS",ctrl=True,alt=True)
		# KeyMaps.append((km,kmi))

		# 3D View --------------------------------------------------------------
		km = kcfg.keymaps.new(name='3D View',space_type='VIEW_3D')

		kmi = km.keymap_items.new("wm.search_menu","X","PRESS")
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("screen.header","SIX","PRESS",alt=True)
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("screen.region_quadview","W","PRESS",alt=True)
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("bsmax.transformgizmosize","EQUAL","PRESS")
		kmi.properties.step = 10
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.transformgizmosize","MINUS","PRESS")
		kmi.properties.step = -10
		KeyMaps.append((km,kmi))

		# View
		create_switch_view_keymap(km)

		# Display
		kmi = km.keymap_items.new("view3d.localview","Q","PRESS",alt=True)
		KeyMaps.append((km,kmi))

		# Set tools
		kmi = km.keymap_items.new("wm.tool_set_by_id","Q","PRESS")
		kmi.properties.name="builtin.select_box"
		kmi.properties.cycle = True
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.move","W","PRESS")
		#kmi = km.keymap_items.new("wm.tool_set_by_id","W","PRESS")
		#kmi.properties.name="builtin.move"
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.rotate","E","PRESS")
		#kmi = km.keymap_items.new("wm.tool_set_by_id","E","PRESS")
		#kmi.properties.name="builtin.rotate"
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.scale","R","PRESS")
		#kmi = km.keymap_items.new("wm.tool_set_by_id","R","PRESS")
		#kmi.properties.name="builtin.scale"
		#kmi.properties.cycle = True
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.scale","E","PRESS",ctrl=True)
		#kmi = km.keymap_items.new("wm.tool_set_by_id","E","PRESS",ctrl=True)
		#kmi.properties.name="builtin.scale"
		#kmi.properties.cycle = True
		KeyMaps.append((km,kmi))

		# selection
		kmi = km.keymap_items.new("view3d.select","LEFTMOUSE","CLICK",ctrl=True)
		kmi.properties.extend = True
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("view3d.select","LEFTMOUSE","CLICK",alt=True)
		kmi.properties.deselect = True
		KeyMaps.append((km,kmi))

		create_view3d_tweak_selection_keymap(km)

		# Tools From BsMax
		kmi = km.keymap_items.new("bsmax.zoomextended","Z","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.setasactivecamera","C","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.showhidegride","G","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.showstatistics","Y","PRESS") #Temprary
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("object.batchrename","F2","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.wireframetoggle","F3","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.edgefacestoggle","F4","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.lightingtoggle","L","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.snaptoggle","S","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.angelsnap","A","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.viewport_background","B","PRESS",alt=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.subobjectlevel","B","PRESS",ctrl=True)
		kmi.properties.level = 6
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.show_safe_areas","F","PRESS",shift=True)
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("bsmax.setframe","HOME","PRESS")
		kmi.properties.frame = 'First'
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.setframe","END","PRESS")
		kmi.properties.frame = 'Last'
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.setframe","PERIOD","PRESS")
		kmi.properties.frame = 'Next'
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.setframe","COMMA","PRESS")
		kmi.properties.frame = 'Previous'
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("bsmax.hold","H","PRESS",ctrl=True,alt=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.fetch","F","PRESS",ctrl=True,alt=True)
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("wm.call_menu","A","PRESS",ctrl=True,shift=True)
		kmi.properties.name="BSMAX_MT_createmenu"
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("bsmax.homeview","HOME","PRESS",alt=True)
		KeyMaps.append((km,kmi))

		# kmi = km.keymap_items.new("bsmax.droptool", "RIGHTMOUSE", "PRESS")
		# KeyMaps.append((km, kmi))

		kmi = km.keymap_items.new("view.undoredo","Z","PRESS",shift=True)
		kmi.properties.redo=False
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("view.undoredo","Y","PRESS",shift=True)
		kmi.properties.redo=True
		KeyMaps.append((km,kmi))

		# Float Editors
		kmi = km.keymap_items.new("bsmax.openmaterialeditor","M","PRESS")
		KeyMaps.append((km,kmi))

		# 3D View Tool: Select ------------------------------------------------
		km = kcfg.keymaps.new(name='3D View Tool: Select',space_type='VIEW_3D')

		kmi = km.keymap_items.new("bsmax.tweakbetter","EVT_TWEAK_L","ANY")
		KeyMaps.append((km,kmi))

		create_view3d_tweak_selection_keymap(km)

		# 3D View Tool: Transform ---------------------------------------------
		km = kcfg.keymaps.new(name='3D View Tool: Transform',space_type='VIEW_3D')

		kmi = km.keymap_items.new("view3d.select_box","EVT_TWEAK_L","ANY")
		kmi.properties.mode = 'SET'
		KeyMaps.append((km,kmi))

		# 3D View Tool: Move ---------------------------------------------------
		km = kcfg.keymaps.new(name='3D View Tool: Move',space_type='VIEW_3D')
		
		kmi = km.keymap_items.new("view3d.select_box","EVT_TWEAK_L","ANY")
		kmi.properties.mode = 'SET'
		KeyMaps.append((km,kmi))

		# 3D View Tool: Rotate -------------------------------------------------
		km = kcfg.keymaps.new(name='3D View Tool: Rotate',space_type='VIEW_3D')

		kmi = km.keymap_items.new("view3d.select_box","EVT_TWEAK_L","ANY")
		kmi.properties.mode = 'SET'
		KeyMaps.append((km,kmi))

		# 3D View Tool: Scale --------------------------------------------------        
		km = kcfg.keymaps.new(name='3D View Tool: Scale',space_type='VIEW_3D')

		kmi = km.keymap_items.new("view3d.select_box","EVT_TWEAK_L","ANY")
		kmi.properties.mode = 'SET'
		KeyMaps.append((km,kmi))

		# 3D View Tool: Select Box ---------------------------------------------
		km = kcfg.keymaps.new(name='3D View Tool: Select Box',space_type='VIEW_3D')

		kmi = km.keymap_items.new("view3d.select_box","EVT_TWEAK_L","ANY",ctrl=True )
		kmi.properties.mode = 'ADD'
		KeyMaps.append((km,kmi))

		# 3D View Tool: Select Circle ------------------------------------------
		km = kcfg.keymaps.new(name='3D View Tool: Select Circle',space_type='VIEW_3D')

		kmi = km.keymap_items.new("view3d.select_circle","EVT_TWEAK_L","ANY",ctrl=True )
		kmi.properties.mode = 'ADD'
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("view3d.select_circle","EVT_TWEAK_L","ANY",alt=True )
		kmi.properties.mode = 'SUB'
		KeyMaps.append((km,kmi))

		# 3D View Tool: Select Lasso -------------------------------------------
		km = kcfg.keymaps.new(name='3D View Tool: Select Lasso',space_type='VIEW_3D')

		kmi = km.keymap_items.new("view3d.select_lasso","EVT_TWEAK_L","ANY",ctrl=True )
		kmi.properties.mode = 'ADD'
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("view3d.select_lasso","EVT_TWEAK_L","ANY",alt=True )
		kmi.properties.mode = 'SUB'
		KeyMaps.append((km,kmi))

		# Transform Modal Map --------------------------------------------------
		km = kcfg.keymaps.new(name='Transform Modal Map',space_type='EMPTY',
							  region_type='WINDOW',      modal = True)

		#kmi = km.keymap_items.new("AXIS_X","F5","ANY")
		#KeyMaps.append((km,kmi))

		"""
		("AXIS_X",{"type": 'X',"value": 'PRESS',"ctrl": True},None),
		("AXIS_Y",{"type": 'Y',"value": 'PRESS'},None),
		("AXIS_Z",{"type": 'Z',"value": 'PRESS'},None),
		("PLANE_X",{"type": 'X',"value": 'PRESS',"shift": True,"ctrl": True},None),
		("PLANE_Y",{"type": 'Y',"value": 'PRESS',"shift": True},None),
		("PLANE_Z",{"type": 'Z',"value": 'PRESS',"shift": True},None),
		{"type": 'F12',"value": 'PRESS',"ctrl": True},
		"""

		# Object Non-modal --------------------------------------------------------------------
		km = kcfg.keymaps.new(name='Object Non-modal',space_type='EMPTY',region_type='WINDOW')

		kmi = km.keymap_items.new("bsmax.mode_set",'TAB',"PRESS")
		KeyMaps.append((km,kmi))
		
		# Object Mode -------------------------------------------------------------------------
		km = kcfg.keymaps.new(name='Object Mode',space_type='EMPTY',region_type='WINDOW')

		# Global
		kmi = km.keymap_items.new("wm.search_menu","X","PRESS")
		KeyMaps.append((km,kmi))

		# selection
		create_view3d_tweak_selection_keymap(km)
		create_view3d_click_celection_keymap(km)
		kmi = km.keymap_items.new("view3d.select","LEFTMOUSE","RELEASE",shift=True)
		kmi.properties.enumerate = True
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("object.select_all","A","PRESS",ctrl=True )
		kmi.properties.action = 'SELECT'
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("object.select_all","D","PRESS",ctrl=True )
		kmi.properties.action = 'DESELECT'
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("object.select_all","I","PRESS",ctrl=True )
		kmi.properties.action = 'INVERT'
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("object.select_hierarchy","PAGE_UP","PRESS")
		kmi.properties.direction = 'PARENT'
		kmi.properties.extend  = False
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("object.select_hierarchy","PAGE_UP","PRESS",ctrl=True)
		kmi.properties.direction = 'PARENT'
		kmi.properties.extend  = True
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("object.select_hierarchy","PAGE_DOWN","PRESS")
		kmi.properties.direction = 'CHILD'
		kmi.properties.extend  = False
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("object.select_hierarchy","PAGE_DOWN","PRESS",ctrl=True)
		kmi.properties.direction = 'CHILD'
		kmi.properties.extend  = True
		KeyMaps.append((km,kmi))

		#kmi = km.keymap_items.new("object.select_similar","Q","PRESS",ctrl=True)
		kmi = km.keymap_items.new("bsmax.select_similar","Q","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))

		# Hide/Unhide
		kmi = km.keymap_items.new("object.hide_view_set","H","PRESS",alt=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("object.hide_view_set","I","PRESS",alt=True)
		kmi.properties.unselected = True
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("object.hide_view_clear","U","PRESS",alt=True)
		KeyMaps.append((km,kmi))
		
		kmi = km.keymap_items.new("bsmax.showgeometrytoggle","G","PRESS",shift=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.showhelpertoggle",  "H","PRESS",shift=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.showshapetoggle",   "S","PRESS",shift=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.showlighttoggle",   "L","PRESS",shift=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.showbonetoggle",    "B","PRESS",shift=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.showcameratoggle",  "C","PRESS",shift=True)
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("object.modifypivotpoint","INSERT","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("wm.call_menu","INSERT","PRESS",ctrl=True)
		kmi.properties.name="BSMAX_MT_SetPivotPoint"
		KeyMaps.append((km,kmi))

		# Float Editors
		kmi = km.keymap_items.new("bsmax.openmaterialeditor","M","PRESS")
		KeyMaps.append((km,kmi))

		# Tools
		kmi = km.keymap_items.new("bsmax.alignselectedobjects","A","PRESS",alt=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.setkeys","K","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.autokeymodetoggle","N","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.transformtypein","F12","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.angelsnap","A","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.lightingtoggle","L","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("bsmax.jumptofirstframe","HOME","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.jumptolastframe","END","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.nextframe","PERIOD","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.previousframe","COMMA","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("screen.animation_play","SLASH","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.selectcamera","C","PRESS")
		KeyMaps.append((km,kmi))

		# kmi = km.keymap_items.new("bsmax.droptool", "RIGHTMOUSE", "PRESS")
		# KeyMaps.append((km, kmi))
		
		# Set Subobject Mode
		create_subobject_mode_keymap(km)

		# Mesh -----------------------------------------------------------------
		km = kcfg.keymaps.new(name='Mesh',space_type='EMPTY')

		# Global
		kmi = km.keymap_items.new("wm.search_menu","X","PRESS")
		KeyMaps.append((km,kmi))

		# Selection
		kmi = km.keymap_items.new("mesh.select_all","A","PRESS",ctrl=True)
		kmi.properties.action = "SELECT"
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("mesh.select_all","D","PRESS",ctrl=True)
		kmi.properties.action = "DESELECT"
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("mesh.select_all","I","PRESS",ctrl=True)
		kmi.properties.action = "INVERT"
		KeyMaps.append((km,kmi))

		create_view3d_click_celection_keymap(km)
		create_view3d_tweak_selection_keymap(km)
		
		kmi = km.keymap_items.new("mesh.shortest_path_pick","LEFTMOUSE","PRESS",shift=True)
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("mesh.select_more","PAGE_UP","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("mesh.select_less","PAGE_DOWN","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("mesh.smart_select_loop","LEFTMOUSE","DOUBLE_CLICK")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("mesh.smart_select_loop","L","PRESS",alt=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("mesh.smart_select_ring","R","PRESS",alt=True)
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("mesh.select_similar","Q","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))

		# View
		create_switch_view_keymap(km)

		kmi = km.keymap_items.new("screen.screen_full_area","X","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))

		# Hide/Unhide
		kmi = km.keymap_items.new("mesh.hide","H","PRESS",alt=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("mesh.hide","I","PRESS",alt=True)
		kmi.properties.unselected = True
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("mesh.reveal","U","PRESS",alt=True)
		KeyMaps.append((km,kmi))

		# Edit
		kmi = km.keymap_items.new("bsmax.connectpoly","E","PRESS",ctrl=True,shift=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("view3d.edit_mesh_extrude_move_normal","E","PRESS",shift=True)
		KeyMaps.append((km,kmi)) 
		kmi = km.keymap_items.new("mesh.knife_tool","C","PRESS",alt=True)
		kmi.properties.use_occlude_geometry = True
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("mesh.bevel","C","PRESS",ctrl=True,shift=True)
		kmi.properties.vertex_only= False
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("transform.vert_slide","X","PRESS",shift=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("mesh.merge","C","PRESS",alt=True,ctrl=True)
		kmi.properties.type = 'CENTER'
		KeyMaps.append((km,kmi))
		#kmi = km.keymap_items.new("mesh.edge_face_add","P","PRESS",alt=True)
		kmi = km.keymap_items.new("mesh.smart_create","P","PRESS",alt=True)
		KeyMaps.append((km,kmi))
		#kmi = km.keymap_items.new("Bevel","B","PRESS",ctrl=True,shift=True)
		#KeyMaps.append((km,kmi))
		#kmi = km.keymap_items.new("spline extrud ","E","PRESS",alt=True)
		#KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("wm.context_toggle","I","PRESS",shift=True,ctrl=True)
		kmi.properties.data_path = "space_data.shading.show_xray"
		KeyMaps.append((km,kmi))
		#kmi = km.keymap_items.new("smooth ","M","PRESS",ctrl=True)
		#KeyMaps.append((km,kmi))
		#kmi = km.keymap_items.new("wm.tool_set_by_name","Q","PRESS",shift=True,ctrl=True)
		#kmi.properties.name="Bisect"
		#KeyMaps.append((km,kmi))
		#kmi = km.keymap_items.new("mesh.remove_doubles","W","PRESS",shift=True,ctrl=True)
		kmi = km.keymap_items.new("bsmax.targetweld","W","PRESS",shift=True,ctrl=True)
		
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.removemesh","BACK_SPACE","PRESS")
		kmi.properties.vert = False
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.removemesh","BACK_SPACE","PRESS",ctrl=True)
		kmi.properties.vert = True
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.deletemesh","DEL","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.transformtypein","F12","PRESS")
		KeyMaps.append((km,kmi))

		# Set Subobject Mode
		create_subobject_mode_keymap(km)

		# Tools
		kmi = km.keymap_items.new("bsmax.shadeselectedfaces","F2","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.autokeymodetoggle","N","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.selectcamera","C","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("wm.tool_set_by_id","E","PRESS")
		kmi.properties.name="builtin.rotate"
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("wm.tool_set_by_id","R","PRESS")
		kmi.properties.name="builtin.scale"
		kmi.properties.cycle = True
		# kmi = km.keymap_items.new("bsmax.droptool", "RIGHTMOUSE", "PRESS")
		# KeyMaps.append((km, kmi))

		# Curve ----------------------------------------------------------------
		km = kcfg.keymaps.new(name='Curve',space_type='EMPTY')

		# Global
		kmi = km.keymap_items.new("wm.search_menu","X","PRESS")
		KeyMaps.append((km,kmi))

		# Selection
		kmi = km.keymap_items.new("curve.select_all","A","PRESS",ctrl=True)
		kmi.properties.action = "SELECT"
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("curve.select_all","D","PRESS",ctrl=True)
		kmi.properties.action = "DESELECT"
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("curve.select_all","I","PRESS",ctrl=True)
		kmi.properties.action = "INVERT"
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("curve.select_more","PAGE_UP","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("curve.select_less","PAGE_DOWN","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("curve.select_similar","Q","PRESS",ctrl=True)
		KeyMaps.append((km,kmi)) 

		# Set Subobject Mode
		create_subobject_mode_keymap(km)

		# View
		create_switch_view_keymap(km)
		kmi = km.keymap_items.new("screen.screen_full_area","X","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))

		# Tools
		kmi = km.keymap_items.new("bsmax.autokeymodetoggle","N","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.selectcamera","C","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("wm.tool_set_by_id","E","PRESS")
		kmi.properties.name="builtin.rotate"
		KeyMaps.append((km,kmi))
		# kmi = km.keymap_items.new("bsmax.droptool", "RIGHTMOUSE", "PRESS")
		# KeyMaps.append((km, kmi))

		# Armature -------------------------------------------------------------
		km = kcfg.keymaps.new(name='Armature',space_type='EMPTY')

		# Global
		kmi = km.keymap_items.new("wm.search_menu","X","PRESS")
		KeyMaps.append((km,kmi))

		# Selection
		create_view3d_click_celection_keymap(km)

		kmi = km.keymap_items.new("armature.select_all","A","PRESS",ctrl=True)
		kmi.properties.action = "SELECT"
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("armature.select_all","D","PRESS",ctrl=True)
		kmi.properties.action = "DESELECT"
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("armature.select_all","I","PRESS",ctrl=True)
		kmi.properties.action = "INVERT"
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("armature.select_more","PAGE_UP","PRESS",ctrl=True,shift=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("armature.select_less","PAGE_DOWN","PRESS",ctrl=True,shift=True)
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("armature.select_hierarchy","PAGE_UP","PRESS")
		kmi.properties.direction = 'PARENT'
		kmi.properties.extend  = False
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("armature.select_hierarchy","PAGE_UP","PRESS",ctrl=True)
		kmi.properties.direction = 'PARENT'
		kmi.properties.extend  = True
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("armature.select_hierarchy","PAGE_DOWN","PRESS")
		kmi.properties.direction = 'CHILD'
		kmi.properties.extend  = False
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("armature.select_hierarchy","PAGE_DOWN","PRESS",ctrl=True)
		kmi.properties.direction = 'CHILD'
		kmi.properties.extend  = True
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("armature.select_similar","Q","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))

		# Hide/Unhide
		kmi = km.keymap_items.new("armature.hide","H","PRESS",alt=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("armature.hide","I","PRESS",alt=True)
		kmi.properties.unselected = True
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("armature.reveal","U","PRESS",alt=True)
		KeyMaps.append((km,kmi))

		# Set Subobject Mode
		create_subobject_mode_keymap(km)

		# View
		create_switch_view_keymap(km)
		kmi = km.keymap_items.new("screen.screen_full_area","X","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("armature.batchrename","F2","PRESS")
		KeyMaps.append((km,kmi))

		# Tools
		kmi = km.keymap_items.new("bsmax.autokeymodetoggle","N","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.selectcamera","C","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("wm.tool_set_by_id","E","PRESS")
		kmi.properties.name="builtin.rotate"
		KeyMaps.append((km,kmi))
		# kmi = km.keymap_items.new("bsmax.droptool", "RIGHTMOUSE", "PRESS")
		# KeyMaps.append((km, kmi))

		# Metaball -------------------------------------------------------------
		km = kcfg.keymaps.new(name='Metaball',space_type='EMPTY')

		# Global
		kmi = km.keymap_items.new("wm.search_menu","X","PRESS")
		KeyMaps.append((km,kmi))

		# Selection
		kmi = km.keymap_items.new("mball.select_all","A","PRESS",ctrl=True)
		kmi.properties.action = "SELECT"
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("mball.select_all","D","PRESS",ctrl=True)
		kmi.properties.action = "DESELECT"
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("mball.select_all","I","PRESS",ctrl=True)
		kmi.properties.action = "INVERT"
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("mball.select_similar","Q","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))

		# Set Subobject Mode
		create_subobject_mode_keymap(km)

		#View
		kmi = km.keymap_items.new("screen.screen_full_area","X","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))

		# Tools
		kmi = km.keymap_items.new("bsmax.autokeymodetoggle","N","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.selectcamera","C","PRESS")
		KeyMaps.append((km,kmi))
		# kmi = km.keymap_items.new("bsmax.droptool", "RIGHTMOUSE", "PRESS")
		# KeyMaps.append((km, kmi))

		# Lattice --------------------------------------------------------------
		km = kcfg.keymaps.new(name='Lattice',space_type='EMPTY')

		# Global
		kmi = km.keymap_items.new("wm.search_menu","X","PRESS")
		KeyMaps.append((km,kmi))

		# Selection
		kmi = km.keymap_items.new("lattice.select_all","A","PRESS",ctrl=True)
		kmi.properties.action = "SELECT"
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("lattice.select_all","D","PRESS",ctrl=True)
		kmi.properties.action = "DESELECT"
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("lattice.select_all","I","PRESS",ctrl=True)
		kmi.properties.action = "INVERT"
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("lattice.select_more","PAGE_UP","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("lattice.select_less","PAGE_DOWN","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("lattice.select_similar","Q","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))

		# Set Subobject Mode
		create_subobject_mode_keymap(km)

		#View
		kmi = km.keymap_items.new("screen.screen_full_area","X","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))

		# Tools
		kmi = km.keymap_items.new("bsmax.autokeymodetoggle","N","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.selectcamera","C","PRESS")
		KeyMaps.append((km,kmi))
		# kmi = km.keymap_items.new("bsmax.droptool", "RIGHTMOUSE", "PRESS")
		# KeyMaps.append((km, kmi))

		# Font -----------------------------------------------------------------

		# Pose -----------------------------------------------------------------
		km = kcfg.keymaps.new(name='Pose',space_type='EMPTY')

		# Selection
		create_view3d_click_celection_keymap(km)

		kmi = km.keymap_items.new("pose.select_all","A","PRESS",ctrl=True)
		kmi.properties.action = "SELECT"
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("pose.select_all","D","PRESS",ctrl=True)
		kmi.properties.action = "DESELECT"
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("pose.select_all","I","PRESS",ctrl=True)
		kmi.properties.action = "INVERT"
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("pose.select_more","PAGE_UP","PRESS",ctrl=True,shift=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("pose.select_less","PAGE_DOWN","PRESS",ctrl=True,shift=True)
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("pose.select_hierarchy","PAGE_UP","PRESS")
		kmi.properties.direction = 'PARENT'
		kmi.properties.extend  = False
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("pose.select_hierarchy","PAGE_UP","PRESS",ctrl=True)
		kmi.properties.direction = 'PARENT'
		kmi.properties.extend  = True
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("pose.select_hierarchy","PAGE_DOWN","PRESS")
		kmi.properties.direction = 'CHILD'
		kmi.properties.extend  = False
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("pose.select_hierarchy","PAGE_DOWN","PRESS",ctrl=True)
		kmi.properties.direction = 'CHILD'
		kmi.properties.extend  = True
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("pose.select_similar","Q","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))

		# Set Subobject Mode
		create_subobject_mode_keymap(km)

		#View
		kmi = km.keymap_items.new("screen.screen_full_area","X","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))

		# Tools
		kmi = km.keymap_items.new("bsmax.autokeymodetoggle","N","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.selectcamera","C","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.setkeys","K","PRESS")
		KeyMaps.append((km,kmi))
		# kmi = km.keymap_items.new("bsmax.droptool", "RIGHTMOUSE", "PRESS")
		# KeyMaps.append((km, kmi))

		# Vertex Paint
		km = kcfg.keymaps.new(name='Vertex Paint',space_type='EMPTY')

		create_switch_view_keymap(km)
		kmi = km.keymap_items.new("bsmax.showcameratoggle",  "C","PRESS",shift=True)
		KeyMaps.append((km,kmi))

		# Weight Paint
		km = kcfg.keymaps.new(name='Weight Paint',space_type='EMPTY')

		create_switch_view_keymap(km)
		kmi = km.keymap_items.new("bsmax.showcameratoggle",  "C","PRESS",shift=True)
		KeyMaps.append((km,kmi))

		# Whight Paint Vertex Selection

		# Face Mask

		# Image Paint

		# Sculpt
		km = kcfg.keymaps.new(name='Sculpt',space_type='EMPTY')

		create_switch_view_keymap(km)

		kmi = km.keymap_items.new("bsmax.showcameratoggle",  "C","PRESS",shift=True)
		KeyMaps.append((km,kmi))

		# Particle

		# 3D View Generic ------------------------------------------------------------
		km = kcfg.keymaps.new(name='3D View Generic',space_type='VIEW_3D',region_type='WINDOW')

		kmi = km.keymap_items.new("view3d.properties","LEFT_BRACKET","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("view3d.toolshelf","RIGHT_BRACKET","PRESS")
		KeyMaps.append((km,kmi))

		# Outliner --------------------------------------------------------------------
		km = kcfg.keymaps.new(name='Outliner',space_type='OUTLINER',region_type='WINDOW')

		# Global
		kmi = km.keymap_items.new("wm.search_menu","X","PRESS")
		KeyMaps.append((km,kmi))

		# upper than 2.80 do not need this part
		if bpy.app.version[1] == 80:
			# Selection
			kmi = km.keymap_items.new("outliner.item_activate","LEFTMOUSE","PRESS",ctrl=True)
			kmi.properties.extend = True
			KeyMaps.append((km,kmi))

			kmi = km.keymap_items.new("outliner.select_box","EVT_TWEAK_L","EAST")
			kmi.properties.mode = "SET"
			KeyMaps.append((km,kmi))
			kmi = km.keymap_items.new("outliner.select_box","EVT_TWEAK_L","SOUTH_EAST")
			kmi.properties.mode = "SET"
			KeyMaps.append((km,kmi))
			kmi = km.keymap_items.new("outliner.select_box","EVT_TWEAK_L","NORTH_EAST")
			kmi.properties.mode = "SET"
			KeyMaps.append((km,kmi))

			kmi = km.keymap_items.new("outliner.select_box","EVT_TWEAK_L","EAST",ctrl=True )
			kmi.properties.mode = "ADD"
			KeyMaps.append((km,kmi))
			kmi = km.keymap_items.new("outliner.select_box","EVT_TWEAK_L","SOUTH_EAST",ctrl=True )
			kmi.properties.mode = "ADD"
			KeyMaps.append((km,kmi))
			kmi = km.keymap_items.new("outliner.select_box","EVT_TWEAK_L","NORTH_EAST",ctrl=True )
			kmi.properties.mode = "ADD"
			KeyMaps.append((km,kmi))

			kmi = km.keymap_items.new("outliner.select_box","EVT_TWEAK_L","EAST",alt=True )
			kmi.properties.mode = "SUB"
			KeyMaps.append((km,kmi))
			kmi = km.keymap_items.new("outliner.select_box","EVT_TWEAK_L","SOUTH_EAST",alt=True )
			kmi.properties.mode = "SUB"
			KeyMaps.append((km,kmi))
			kmi = km.keymap_items.new("outliner.select_box","EVT_TWEAK_L","NORTH_EAST",alt=True )
			kmi.properties.mode = "SUB"
			KeyMaps.append((km,kmi))

			kmi = km.keymap_items.new("outliner.select_all","A","PRESS",ctrl=True)
			kmi.properties.action = "SELECT"
			KeyMaps.append((km,kmi))
			kmi = km.keymap_items.new("outliner.select_all","D","PRESS",ctrl=True)
			kmi.properties.action = "DESELECT"
			KeyMaps.append((km,kmi))
			kmi = km.keymap_items.new("outliner.select_all","I","PRESS",ctrl=True)
			kmi.properties.action = "INVERT"
			KeyMaps.append((km,kmi))

			kmi = km.keymap_items.new("outliner.collection_objects_select","LEFTMOUSE","DOUBLE_CLICK")
			KeyMaps.append((km,kmi))

			# Tools
			kmi = km.keymap_items.new("outliner.item_rename","F2","PRESS")
			KeyMaps.append((km,kmi))

			kmi = km.keymap_items.new("outliner.collection_new","N","PRESS",ctrl=True)
			KeyMaps.append((km,kmi))

			# TODO need a outliner delete object
			kmi = km.keymap_items.new("object.delete","DEL","PRESS",ctrl=True)
			kmi.properties.confirm = False
			KeyMaps.append((km,kmi))

			kmi = km.keymap_items.new("outliner.hide","H","PRESS",alt=True)
			KeyMaps.append((km,kmi))
			# kmi = km.keymap_items.new("outliner.hide_unselected","I","PRESS",alt=True)
			# KeyMaps.append((km,kmi)) # had to write in bsmax
			kmi = km.keymap_items.new("outliner.unhide_all","U","PRESS",alt=True)
			KeyMaps.append((km,kmi))

		# Node Editor -----------------------------------------------------------------
		km = kcfg.keymaps.new(name="Node Editor",space_type="NODE_EDITOR",region_type='WINDOW')

		# Global
		kmi = km.keymap_items.new("wm.search_menu","X","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("node.batchrename","F2","PRESS")
		KeyMaps.append((km,kmi))

		# Selection
		kmi = km.keymap_items.new("node.select","LEFTMOUSE","PRESS",ctrl=True)
		kmi.properties.extend = True
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("node.select_all","A","PRESS",ctrl=True)
		kmi.properties.action = "SELECT"
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("node.select_all","D","PRESS",ctrl=True)
		kmi.properties.action = "DESELECT"
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("node.select_all","I","PRESS",ctrl=True)
		kmi.properties.action = "INVERT"
		KeyMaps.append((km,kmi))

		# tools
		kmi = km.keymap_items.new("node.view_selected","Z","PRESS")
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("wm.call_menu","RIGHTMOUSE","PRESS")
		kmi.properties.name="NODE_MT_add"
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("node.duplicate_move","EVT_TWEAK_L","ANY",shift=True )
		KeyMaps.append((km,kmi))

		#node.links_cut

		# Screen ----------------------------------------------------------------------
		km = kcfg.keymaps.new(name='Screen',space_type='EMPTY')

		kmi = km.keymap_items.new("render.render","F9","PRESS")
		kmi.properties.use_viewport = True
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("render.render","Q","PRESS",shift=True)
		kmi.properties.use_viewport = True
		kmi.properties.animation = True
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("screen.repeat_last","SEMI_COLON","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("screen.screen_full_area","X","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("screen.screen_full_area","X","PRESS",alt=True,ctrl=True)
		kmi.properties.use_hide_panels = True
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.scriptlistener","F11","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("ed.redo","Y","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))

		# Text ----------------------------------------------------------------------
		km = kcfg.keymaps.new(name='Text',space_type='TEXT_EDITOR',region_type='WINDOW')

		kmi = km.keymap_items.new("text.run_script","E","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("text.run_script","F5","PRESS") # From MVS
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("text.autocomplete","RET","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("text.new","N","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("text.open","O","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("text.save","S","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("text.save_as","S","PRESS",ctrl=True,shift=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("text.reload","R","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("text.unlink","W","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))

		# Console ---------------------------------------------------------------------
		km = kcfg.keymaps.new(name='Console',space_type='CONSOLE',region_type='WINDOW')

		kmi = km.keymap_items.new("text.new","N","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("text.open","O","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("text.save","S","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))

		# Info ------------------------------------------------------------------------
		km = kcfg.keymaps.new(name='Info',space_type='INFO',region_type='WINDOW')

		# TODO Replase with if text editor not open create new else just new text
		kmi = km.keymap_items.new("text.new","N","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("text.open","O","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("text.save","S","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("info.select_box","EVT_TWEAK_L","ANY")
		kmi.properties.mode = "SET"
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("info.select_box","EVT_TWEAK_L","ANY",ctrl=True)
		kmi.properties.mode = "ADD"
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("info.select_box","EVT_TWEAK_L","ANY",alt=True)
		kmi.properties.mode = "SUB"
		KeyMaps.append((km,kmi))
		# TODO replase with select all
		kmi = km.keymap_items.new("info.select_all_toggle","A","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))
		# TODO repelase with delete all
		kmi = km.keymap_items.new("info.report_delete","D","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))

		# Frames ----------------------------------------------------------------------
		km = kcfg.keymaps.new(name='Frames',space_type='EMPTY',region_type='WINDOW')

		kmi = km.keymap_items.new("bsmax.jumptofirstframe","HOME","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.jumptolastframe","END","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.nextframe","PERIOD","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.previousframe","COMMA","PRESS")
		KeyMaps.append((km,kmi))

		# GRAPH_EDITOR ----------------------------------------------------------------
		km = kcfg.keymaps.new(name="Graph Editor",space_type="GRAPH_EDITOR",region_type='WINDOW')
		
		# Global
		kmi = km.keymap_items.new("wm.search_menu","X","PRESS")
		KeyMaps.append((km,kmi))

		# Selection
		kmi = km.keymap_items.new("graph.clickselect","LEFTMOUSE","PRESS")
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("graph.select_box","EVT_TWEAK_L","ANY")
		kmi.properties.mode = "SET"
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("graph.select_box","EVT_TWEAK_L","ANY",ctrl=True )
		kmi.properties.mode = "ADD"
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("graph.select_box","EVT_TWEAK_L","ANY",alt=True )
		kmi.properties.mode = "SUB"
		KeyMaps.append((km,kmi))  

		kmi = km.keymap_items.new("graph.select_all","A","PRESS",ctrl=True)
		kmi.properties.action = "SELECT"
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("graph.select_all","D","PRESS",ctrl=True)
		kmi.properties.action = "DESELECT"
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("graph.select_all","I","PRESS",ctrl=True)
		kmi.properties.action = "INVERT"
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("graph.select_more","PAGE_UP","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("graph.select_less","PAGE_DOWN","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))

		# Translate 
		# TODO for test
		kmi = km.keymap_items.new("transform.translate","EVT_TWEAK_L","ANY")
		KeyMaps.append((km,kmi))

		# Tools
		kmi = km.keymap_items.new("bsmax.setkeys","K","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.autokeymodetoggle","N","PRESS")
		KeyMaps.append((km,kmi))
		
		# DOPESHEET_EDITOR (Timeline)--------------------------------------------------
		km = kcfg.keymaps.new(name="Dopesheet",space_type="DOPESHEET_EDITOR")

		# Global
		kmi = km.keymap_items.new("wm.search_menu","X","PRESS")
		KeyMaps.append((km,kmi))

		# Tools
		kmi = km.keymap_items.new("bsmax.setkeys","K","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.autokeymodetoggle","N","PRESS")
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.settimelinerange","LEFTMOUSE","PRESS",alt=True,ctrl=True)
		kmi.properties.mode = 'First'
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.settimelinerange","RIGHTMOUSE","PRESS",alt=True,ctrl=True)
		kmi.properties.mode = 'End'
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("bsmax.settimelinerange","MIDDLEMOUSE","PRESS",alt=True,ctrl=True)
		kmi.properties.mode = 'Shift'
		KeyMaps.append((km,kmi))

		# Menu
		# kmi = km.keymap_items.new("wm.call_menu","RIGHTMOUSE","PRESS",alt=True)
		# kmi.properties.name="bsmax.coordinatesmenu"
		# KeyMaps.append((km,kmi))

		# Selection
		kmi = km.keymap_items.new("action.select_box","EVT_TWEAK_L","ANY")
		kmi.properties.mode = "SET"
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("action.select_box","EVT_TWEAK_L","ANY",ctrl=True )
		kmi.properties.mode = "ADD"
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("action.select_box","EVT_TWEAK_L","ANY",alt=True )
		kmi.properties.mode = "SUB"
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("action.select_all","A","PRESS",ctrl=True)
		kmi.properties.action = "SELECT"
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("action.select_all","D","PRESS",ctrl=True)
		kmi.properties.action = "DESELECT"
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("action.select_all","I","PRESS",ctrl=True)
		kmi.properties.action = "INVERT"
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("action.select_more","PAGE_UP","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("action.select_less","PAGE_DOWN","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("screen.animation_play","SLASH","PRESS")
		KeyMaps.append((km,kmi))

		# UV Editor--------------------------------------------------------------------
		km = kcfg.keymaps.new(name='UV Editor',space_type='EMPTY',region_type='WINDOW')

		# Selection
		kmi = km.keymap_items.new("wm.tool_set_by_id","Q","PRESS")
		kmi.properties.name="builtin.select_box"
		kmi.properties.cycle = True
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("uv.select","EVT_TWEAK_L","ANY")
		kmi.properties.extend = True
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("uv.select_box","EVT_TWEAK_L","ANY")
		kmi.properties.mode = 'SET'
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("uv.select_box","EVT_TWEAK_L","ANY",ctrl=True )
		kmi.properties.mode = 'ADD'
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("uv.select_box","EVT_TWEAK_L","ANY",alt=True )
		kmi.properties.mode = 'SUB'
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("uv.select_more","PAGE_UP","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("uv.select_less","PAGE_DOWN","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))

		kmi = km.keymap_items.new("uv.select_all","A","PRESS",ctrl=True)
		kmi.properties.action = "SELECT"
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("uv.select_all","D","PRESS",ctrl=True)
		kmi.properties.action = "DESELECT"
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("uv.select_all","I","PRESS",ctrl=True)
		kmi.properties.action = "INVERT"
		KeyMaps.append((km,kmi))

		#Note: multi loop command not working on uv yet
		#kmi = km.keymap_items.new("bsmax.uvloopselect","L","PRESS",alt=True)
		#KeyMaps.append((km,kmi))
		#kmi = km.keymap_items.new("bsmax.uvringselect","R","PRESS",alt=True)
		#KeyMaps.append((km,kmi))

		# Hide/Unhide
		kmi = km.keymap_items.new("uv.hide","H","PRESS",alt=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("uv.hide","I","PRESS",alt=True)
		kmi.properties.unselected = True
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("uv.reveal","U","PRESS",alt=True)
		KeyMaps.append((km,kmi))

		#
		kmi = km.keymap_items.new("uv.select_split","B","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("uv.weld","W","PRESS",ctrl=True)
		KeyMaps.append((km,kmi))

		# SEQUENCE_EDITOR--------------------------------------------------------------------
		km = kcfg.keymaps.new(name='Sequencer',space_type='SEQUENCE_EDITOR',region_type='WINDOW')

		kmi = km.keymap_items.new("sequencer.batchrename","F2","PRESS")
		KeyMaps.append((km,kmi))

		# File Browser ----------------------------------------------------------------
		km = kcfg.keymaps.new(name='File Browser',space_type='FILE_BROWSER',region_type='WINDOW')

		kmi = km.keymap_items.new("filebrowser.scaleicons","WHEELUPMOUSE",'PRESS',ctrl=True)
		kmi.properties.up = True
		KeyMaps.append((km,kmi))
		kmi = km.keymap_items.new("filebrowser.scaleicons","WHEELDOWNMOUSE",'PRESS',ctrl=True)
		kmi.properties.up = False
		KeyMaps.append((km,kmi))

		# Knife Tool Modal Map --------------------------------------------------------
		#km = kcfg.keymaps.new(name='Knife Tool Modal Map',space_type='EMPTY',region_type='WINDOW',modal = True)

		#kmi = km.keymap_items.new("CONFIRM","RIGHTMOUSE","PRESS",any = True)
		#KeyMaps.append((km,kmi))
		#------------------------------------------------------------------------------

def remove_3dsmax_keymaps():
	for km,kmi in KeyMaps:
		km.keymap_items.remove(kmi)
	KeyMaps.clear()
	max_dif_keys_set(True)

def max_keys(register):
	if register:
		remove_3dsmax_keymaps()
		create_3dsmax_keymaps()
		start_new_thread(max_dif_keys_set,tuple([False]))
	else:
		remove_3dsmax_keymaps()

if __name__ == '__main__':
	max_keys(True)

__all__=["max_keys"]