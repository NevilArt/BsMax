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
	def __init__(self, space, idname, type, value,
				alt, ctrl, shift, any,
				repeat , modal, direction):
		self.space = space
		self.idname = idname
		self.type = type
		self.value = value
		self.any = any
		self.alt = alt
		self.ctrl = ctrl
		self.shift = shift
		self.repeat = repeat
		self.modal = modal
		self.direction = direction
		self.properties = []
		self._key = None
		self.keymaps = bpy.context.window_manager.keyconfigs.default.keymaps


	@property
	def key(self):
		if self._key:
			return self._key

		if self.space in self.keymaps:
			keymap_items = self.keymaps[self.space].keymap_items

			for k in keymap_items:
				if self.idname == k.idname:
					if self.type == k.type and self.value == k.value and \
						self.any == k.any and self.alt == k.alt and \
						self.ctrl == k.ctrl and self.shift == k.shift and \
						self.direction == k.direction:
						
						self._key = k
						break

	
	def compare(self, space, idname, type, value,
				alt, ctrl, shift, any,
				direction, properties):

		if self.space != space:
			return False
		if self.idname != idname:
			return False
		if self.type != type:
			return False
		if self.value != value:
			return False
		if self.any != any:
			return False
		if self.alt != alt:
			return False
		if self.ctrl != ctrl:
			return False
		if self.shift != shift:
			return False
		if self.direction != direction:
			return False

		prop_copmp = []
		for p in properties:
			for sp in self.properties:
				if p[0] == sp[0] and p[1] == sp[1]:
					prop_copmp += [p]
					break

		if len(prop_copmp) != len(prop_copmp):
			return False

		return True



class KeyMaps:
	def __init__(self):
		self.newkeys = []
		self.keymaps = []
		self.mutekeys = []
		self.kcfg = bpy.context.window_manager.keyconfigs.addon

	def space(self, name, space_type, region_type, modal=False):
		return self.kcfg.keymaps.new(name=name,
									space_type=space_type,
									region_type=region_type)

	def new(self, space, idname,
			type, value, properties,
			alt=False, ctrl=False, shift=False,
			any=False, modal=False, repeat=False,
			direction=''):

		""" check is info unique """
		isnew = True
		for key in self.newkeys:
			if key.compare(space, idname, type, value,
						alt, ctrl, shift, any,
						direction, properties):

				isnew = False
				break
		""" create newkey if it is uniqu """
		if isnew:
			newkey = KeyMap(space, idname, type, value,
							alt, ctrl, shift, any,
							repeat, modal, direction)

			newkey.properties = properties
			self.newkeys.append(newkey)
	
	def mute(self, space, idname, inputtype, value,
			alt=False, ctrl=False, shift=False,
			any=False, modal=False, direction=''):

		newkey = KeyMap(space, idname, inputtype, value,
						alt=alt, ctrl=ctrl, shift=shift, any=any,
						repeat=False, modal=modal, direction=direction)

		self.mutekeys.append(newkey)
	
	def set_mute(self, state, delay):
		for mutekey in self.mutekeys:
			if mutekey.key != None:
				mutekey.key.active = not state
		# bpy.context.window_manager.keyconfigs.default.keymaps['3D View Generic'].keymap_items['wm.context_toggle'].active

	def register(self):
		self.unregister()
		for k in self.newkeys:
			if k.modal:
				#TODO check for how to change modal key maps too
				#############################################################
				keymapitem = k.space.keymap_items.new_modal(k.idname,
															k.type,
															k.value,
															alt=k.alt,
															ctrl=k.ctrl,
															shift=k.shift,
															any=k.any)
				#############################################################
			else:
				keymapitem = k.space.keymap_items.new(k.idname,
													k.type,
													k.value,
													alt=k.alt,
													ctrl=k.ctrl,
													shift=k.shift,
													any=k.any,
													repeat=k.repeat)

			for key, val in k.properties:
				if hasattr(keymapitem.properties, key):
					setattr(keymapitem.properties, key, val)

			self.keymaps.append((k.space, keymapitem))
		self.set_mute(True, 0)

	def unregister(self):
		for km,kmi in self.keymaps:
			km.keymap_items.remove(kmi)
		self.keymaps.clear()
		self.set_mute(False, 0)