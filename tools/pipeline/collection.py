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
# 2024/03/04

import bpy

from bsmax.actions import new_collection


def force_get_colection(ctx, name):
	collections = bpy.data.collections
	if name in collections:
		collection = collections[name]
		return collection

	newCollection = collections.new(name)
	ctx.scene.collection.children.link(newCollection)
	return newCollection


def force_get_empty_object(ctx, name):
	if name in bpy.data.objects:
		return bpy.data.objects[name]
	
	bpy.ops.object.empty_add(
		type='SINGLE_ARROW',
		align='WORLD',
		location=(0, 0, 0),
		scale=(1, 1, 1)
	)

	newEmpty = ctx.active_object
	newEmpty.name = name
	return newEmpty


def link_to_collection(obj, collection):
	for layer in obj.users_collection:
		layer.objects.unlink(obj)
	collection.objects.link(obj)


def create_default_Collections(ctx):
	new_collection(ctx, 'Char', 7)
	new_collection(ctx, 'Prop', 5)
	env = new_collection(ctx, 'Env', 4)
	new_collection(ctx, 'Effect', 1)
	new_collection(ctx, 'Light & Cam', 3)

	new_collection(ctx, 'Far', 5, env)
	new_collection(ctx, 'Back', 4, env)
	new_collection(ctx, 'Touch', 3, env)
	new_collection(ctx, 'Active', 2, env)


def setup_crypto_stuff(ctx):
	# Char crypto parent
	charLayer = force_get_colection(ctx, "Char")
	charCryptoParent = force_get_empty_object(ctx, "CharCryptoParent")
	link_to_collection(charCryptoParent, charLayer)
	
	# Prop Crypto Parent
	propLayer = force_get_colection(ctx, "Prop")
	propCryptoParent = force_get_empty_object(ctx, "PropCryptoParent")
	link_to_collection(propCryptoParent, propLayer)


if __name__ == '__main__':
	create_default_Collections(bpy.context)