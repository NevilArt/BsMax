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

function redshift_proxy_renew =
(
	if classof $ == proxy do (
		old = selection[1]
		new = proxy pos:[0,0,0] isSelected:on
		new.gizmoscale = old.gizmoscale
		new.file = old.file
		new.displaymode = old.displaymode
		new.linkedmesh = old.linkedmesh
		new.displaypct = old.displaypct
		new.issequence = old.issequence
		new.startframe = old.startframe
		new.endframe = old.endframe
		new.pattern = old.pattern
		new.frameoffset = old.frameoffset
		new.outofrangemode = old.outofrangemode
		new.materialmode = old.materialmode
		new.namematchprefix = old.namematchprefix
		new.overrideobjectid = old.overrideobjectid
		new.overridevisibility = old.overridevisibility
		new.overridetessdisp = old.overridetessdisp
		new.overridetracesets = old.overridetracesets
		new.overrideuserdata = old.overrideuserdata
		
		new.transform = old.transform
		new.gbufferchannel = old.gbufferchannel
		new.name = old.name
		old.name += "_old"
		select old
	)
)



function clear_render_output =
(
	OpenDialog = renderSceneDialog.isOpen()
	renderSceneDialog.close()
	rendOutputFilename = ""
	if OpenDialog do (
        renderSceneDialog.open()
    )
)



rollout AETimeCalc "AE Time"
(
	spinner MaxFrame "Max Frame:" type:#integer range:[-999999, 999999, 0]
	spinner AEFrame "AE Frame:" type:#integer range:[-999999, 999999, 0] tooltip:"After effect Frame"
	edittext ClipBoard "ClipBoard" readonly:true

	function Calc =
	(
		MaxFrame.value = (filterstring (slidertime as string) "f")[1] as integer
		local S = (filterstring (animationRange.start as string) "f")[1] as integer
		AEFrame.value = MaxFrame.value - S as integer
		ClipBoard.text = "_" + MaxFrame.value as string + "-" + AEFrame.value as string
	)

	on AETimeCalc open do
	(
		Calc()
		registerTimeCallback Calc
	)

	on AETimeCalc close do (
		unregisterTimeCallback Calc
	)
	
	on MaxFrame entered a b do
	(
		slidertime = MaxFrame.value
	)

	on AEFrame entered  a b do
	(
		slidertime = AEFrame.value + (filterstring (animationRange.start as string) "f")[1] as integer
	)
)

function open_afterefect_time_calculator =
(
	createdialog AETimeCalc
)


function wirecolor_to_standard_material =
(
	for o in selection do if o.material == undefined do
	(
		--NewMat = VRayMtl()
		NewMat = Standardmaterial()
		NewMat.diffuse = o.wirecolor
		o.material = NewMat
	)
)



function copy_render_out_path =
(
	setclipboardText ( getFilenamePath rendOutputFilename)
)

