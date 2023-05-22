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

struct characterData
(
	layer = undefined,
	newName = "",
	origName = ""
)



function clearScene =
(
	/*
	*	Turn off all Turbo smoth modifiers
	*	Turn on all morpher modifiers 
	*/

	for obj in geometry do (
		for m in obj.modifiers do (
			modClass = classof m
			/* Turn off turbo smoothes */
			if modClass == TurboSmooth do
				m.enabled = False

			/* Turn on morphers */
			if modClass == Morpher or
				modClass == FFD_Binding or
				modClass == Skin_Wrap do
				m.enabled = m.enabledInViews = True
		)
	)
)



function make_poly objs =
(
	/*
	* make sure given object returns poly mesh object
	*/
	for obj in objs do
		if ClassOf obj != PolyMeshObject do
			addModifier obj (Turn_to_Poly())
)



function getCharacterLayers =
(
	/* Collect mesh objects with Skin modifier */
	skined_meshs = #()
	for obj in geometry do
		for m in obj.modifiers do
			if classof m == Skin do
				append skined_meshs obj

	/* Collect layers of skined objs */
	skined_layers = #()
	for obj in skined_meshs do
		appendIfUnique skined_layers obj.layer
	
	return skined_layers
)



function getAlembicPath subDir =
(
	if subDir == "" then
		return maxfilepath
	return maxfilepath + subDir + "\\"
)



function getCharNameFromLayer layerName =
(
	nameParts = filterString layerName "_"
	the_name = ""
	for i = 1 to (nameParts.count - 1) do (
		the_name += nameParts[i]
		if i < (nameParts.count - 1) do
			the_name += "_"
	)
	
	if the_name == "" do
		return layerName

	return the_name
)



function getAlembicFileName characterName =
(
	/* analayze max file name */
	fileName = getFilenameFile maxfilename
	nameParts = filterString fileName "_"

	if nameParts.count == 1 do
		return fileName + ".ABC"
	
	if nameParts.count < 3 do
		return nameParts[1] + ".ABC"

	/* 	combine first 3 name parts 
	*	Projectname_Episode_Scene_charactername
	*/
	fileName = nameParts[1] + "_"
	fileName += nameParts[2] + "_"
	fileName += nameParts[3] + "_"
	fileName += characterName + ".ABC"

	return fileName
)



function selectLayerObjects layer =
(
	clearSelection()
	local nodes
	layer.nodes &nodes
	select nodes
)


function selectMoreLayerObjects layer =
(
	local nodes
	layer.nodes &nodes
	selectmore nodes
)



function getAlembicExporter =
(
	for plg in exporterPlugin.classes do
		if plg as string == "Alembic_Export" do
			return plg
	return undefined
)



function hasSkin obj =
(
	for m in obj.modifiers do
		if ClassOf m == Skin do
			return True
	return False
)



function skinTheMesh meshObj boneObj =
(
	addModifier meshObj (Skin())
	skinMod = meshObj.modifiers[#Skin]
	skinOps.addBone skinMod boneObj 1 node:meshObj
)



function skinEyes charName =
(
	leftEye = getnodebyname(charName + "_EyeBall_L")
	rightEye = getnodebyname(charName + "_EyeBall_R")
	
	leftEyeBone = getnodebyname(charName + "_LeftEyeLookCtrl_001")
	rightEyeBone = getnodebyname(charName + "_RightEyeLookCtrl_001")

	if leftEye != undefined and leftEyeBone != undefined do
		if not hasSkin leftEye do
			skinTheMesh leftEye leftEyeBone

	if rightEye != undefined and rightEyeBone != undefined do
		if not hasSkin rightEye do
			skinTheMesh rightEye rightEyeBone
)



function export caharacterList subDire doExport =
(
	clearScene()

	for char in caharacterList do(
		selectLayerObjects char.layer
		make_poly selection

		skinEyes char.origName

		fileName = getAlembicFileName char.newName
		alembicPath = getAlembicPath subDire
		fullFileName = alembicPath + fileName

		if doExport do (
			makeDir (alembicPath) all:True
			exportFile fullFileName #noPrompt selectedOnly:True using:(getAlembicExporter())
		)
	)
)



function select_meshes caharacterList =
(
	clearSelection()
	for char in caharacterList do
		selectMoreLayerObjects char.layer
)



rollout maxToABC "Max to ABC"
(
	button refreshBtn "Refresh" width:145
	multilistbox namesMlb "" heigth:10
		tooltip:"Doubleclick for rename"

	edittext charName "ReName"

	edittext ABCSubdire "Sub-Dir  " text:"ABC"
		tooltip:"Put *.ABC file to sub directory\n
				Leave blank for use same directory"

	button selectBtn "Select" width:45 across:3
	button applyBtn "Apply" width:45
	button exportBtn "Export" width:45

	local caharacterList = #()
	local activeIndex = 0

	function getExportList =
	(
		exportList = #()
		for i in namesMlb.selection do
			append exportList caharacterList[i]
		return exportList
	)

	function namesFromCharacterList =
	(
		nameList = #()
		for char in caharacterList do
			append nameList char.newName
		namesMlb.items = nameList
	)

	function refresh =
	(
		caharacterList = #()
		activeIndex = 0
		for layer in getCharacterLayers() do(
			theName = getCharNameFromLayer layer.name
			newCharacter = characterData()
			newCharacter.layer = layer
			newCharacter.newName = theName
			newCharacter.origName = theName
			append caharacterList newCharacter
		)
		namesFromCharacterList()
	)

	on maxToABC open do (
		refresh()
	)

	on refreshBtn pressed do (
		refresh()
	)

	on selectBtn pressed do (
		select_meshes (getExportList())
	)

	on applyBtn pressed do (
		export (getExportList()) ABCSubdire.text False
	)

	on exportBtn pressed do (
		export (getExportList()) ABCSubdire.text True
	)

	on namesMlb doubleClicked arg do (
		charName.text = namesMlb.items[arg]
		activeIndex = arg
	)

	on charName entered arg do (
		if activeIndex > 0 do
			caharacterList[activeIndex].newName = arg
		namesFromCharacterList()
	)
)

function open_character_to_abc_dialog =
(
	CreateDialog maxToABC
)