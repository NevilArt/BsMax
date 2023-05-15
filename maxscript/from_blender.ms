/*##########################################################################
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
##########################################################################*/

function frame_to_int frame =
(
	return (FilterString (frame as string) "f")[1] as  integer
)

/* Compar Transform */
function compar_transfrom transform_a transform_b tolerance=
(
	pa = transform_a.position
	pb = transform_b.position
	
	ra = transform_a.rotation
	rb = transform_a.rotation
	
	sa = transform_a.scale
	sb = transform_b.scale
	
	t = tolerance / 2

	if pb.x - t > pa.x and pa.x < pb.x + t do
		return false
	if pb.y - t > pa.y and pa.y < pb.y + t do
		return false
	if pb.z - t > pa.z and pa.z < pb.z + t do
		return false

	if rb.x - t > ra.x and ra.x < rb.x + t do
		return false
	if rb.y - t > ra.y and ra.y < rb.y + t do
		return false
	if rb.z - t > ra.z and ra.z < rb.z + t do
		return false
	
	if sb.x - t > sa.x and sa.x < sb.x + t do
		return false
	if sb.y - t > sa.y and sa.y < sb.y + t do
		return false
	if sb.z - t > sa.z and sa.z < sb.z + t do
		return false

	return true
)

function fix_time_range =
(
	start = frame_to_int animationRange.start 
	end = frame_to_int animationRange.end
	animationRange = interval start end
)

-- ABC Camera to Free Camera --
function abc_to_free_camera abc_camera =
(
	new_camera = Freecamera fov:35 targetDistance:1
	/* set transform and set key if not mach with other camera  */
	start = frame_to_int animationRange.start 
	end = frame_to_int animationRange.end
	on animate on
		for frame = start to end do
			at time frame
				if not compar_transfrom new_camera.transform abc_camera.transform 0.000025 do
					new_camera.transform = abc_camera.transform
)

-- ABC Object to mesh --
function abc_obj_to_mesh abs_obj =
(
	transforms = #()
	start = frame_to_int animationRange.start 
	end = frame_to_int animationRange.end
	
	/* collect transform data */
	for frame = start to end do
		at time frame
			append transforms abs_obj.transform
	
	abs_obj.Transform.controller = prs ()
			
	index = 0
	on animate on
		for frame = start to end do (
			index += 1
			at time frame
				if not compar_transfrom abs_obj.transform transforms[index] 0.000025 do
					abs_obj.transform = transforms[index]
		)
	
	convertToMesh abs_obj
)


function scene_scan =
(
	fix_time_range()

	for obj in objects do (

		if classof obj == AlembicCamera do (
			abc_to_free_camera obj
		)

		if classof obj == AlembicObject do (
			--TODO check is deformed object or not
			--abc_obj_to_mesh obj
		)

		if classof obj == AlembicContainer do (
			delete obj
		)
	)
)

scene_scan()