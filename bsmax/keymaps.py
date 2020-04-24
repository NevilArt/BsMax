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
from time import sleep
from _thread import start_new_thread

class KeyMap:
	def __init__(self,space,idname,inputtype,value,alt,ctrl,shift,any):
		self.space = space
		self.idname = idname
		self.inputtype = inputtype
		self.value = value
		self.any = any
		self.alt = alt
		self.ctrl = ctrl
		self.shift = shift
	def __eq__(self, key):
		return self.idname == key.idname and self.inputtype == key.type and self.value == key.value and \
			self.alt == key.alt and self.ctrl == key.ctrl and self.shift == key.shift and self.any == key.any

class KeyMaps:
	def __init__(self):
		self.keymaps = []
		self.mutekeys = []

	def space(self,name,space_type,region_type,modal=False):
		kcfg = bpy.context.window_manager.keyconfigs.addon
		return kcfg.keymaps.new(name=name,space_type=space_type,region_type=region_type)
	
	def new(self,space,idname,inputtype,value,properties,
			alt=False,ctrl=False,shift=False,any=False):
		keymapitem = space.keymap_items.new(idname, inputtype, value,
								alt=alt, ctrl=ctrl, shift=shift, any=any)
		self.keymaps.append((space, keymapitem))
		for p in properties:
			kama = "'" if type(p[1]) == str else ""
			exec("keymapitem.properties." + p[0] + "=" + kama + str(p[1]) + kama)
	
	def mute(self,space,idname,inputtype,value,alt=False,ctrl=False,shift=False,any=False):
		newkey = KeyMap(space,idname,inputtype,value,alt=alt,ctrl=ctrl,shift=shift,any=any)
		self.mutekeys.append(newkey)
	
	def set_mute(self,state):
		try:
			sleep(0.1)
			kdif = bpy.context.window_manager.keyconfigs.default
			km = kdif.keymaps[space]
			for key in km.keymap_items:
				for mk in self.mutekeys:
					if mk == key:
						key.active = not state
		except:
			start_new_thread(self.set_mute,tuple([state]))

	def reset(self):
		for km,kmi in self.keymaps:
			km.keymap_items.remove(kmi)
		self.keymaps.clear()
		self.set_mute(False)