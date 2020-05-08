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

class KeyMap:
	def __init__(self,space,idname,type,value,alt,ctrl,shift,any):
		self.space = space
		self.idname = idname
		self.type = type
		self.value = value
		self.any = any
		self.alt = alt
		self.ctrl = ctrl
		self.shift = shift
		self.properties = []
		self._key = None

	@property
	def key(self):
		if self._key == None:
			keymaps = bpy.context.window_manager.keyconfigs.default.keymaps
			if self.space in keymaps:
				keymap_items = keymaps[self.space].keymap_items
				for k in keymap_items:
					if self.idname == k.idname:
						if self.type == k.type and self.value == k.value and \
							self.any == k.any and self.alt == k.alt and \
							self.ctrl == k.ctrl and self.shift == k.shift:
							self._key = k
							break
		return self._key

class KeyMaps:
	def __init__(self):
		self.newkeys = []
		self.keymaps = []
		self.mutekeys = []

	def space(self,name,space_type,region_type,modal=False):
		kcfg = bpy.context.window_manager.keyconfigs.addon
		return kcfg.keymaps.new(name=name,space_type=space_type,region_type=region_type)
	
	def new(self,space,idname,type,value,properties,
			alt=False,ctrl=False,shift=False,any=False):
		newkey = KeyMap(space,idname,type,value,alt,ctrl,shift,any)
		newkey.properties = properties
		self.newkeys.append(newkey)
	
	def mute(self,space,idname,inputtype,value,alt=False,ctrl=False,shift=False,any=False):
		newkey = KeyMap(space,idname,inputtype,value,alt=alt,ctrl=ctrl,shift=shift,any=any)
		self.mutekeys.append(newkey)
	
	def set_mute(self,state,delay):
		for mutekey in self.mutekeys:
			if mutekey.key != None:
				mutekey.key.active = not state

	def register(self):
		self.unregister()
		for k in self.newkeys:
			keymapitem = k.space.keymap_items.new(k.idname, k.type, k.value,
						alt=k.alt, ctrl=k.ctrl, shift=k.shift, any=k.any)
			for key,val in k.properties:
				if hasattr(keymapitem.properties,key):
					setattr(keymapitem.properties,key,val)
			self.keymaps.append((k.space, keymapitem))
		self.set_mute(True,0)

	def unregister(self):
		for km,kmi in self.keymaps:
			km.keymap_items.remove(kmi)
		self.keymaps.clear()
		self.set_mute(False,0)