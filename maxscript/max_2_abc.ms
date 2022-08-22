function clear_scene =
(
	/*
	*	Turn off all Turbo smoth modifiers
	*	Turn on all morpher modifiers 
	*/

	for obj in geometry do (
		for m in obj.modifiers do (
			/* Turn off turbo smoothes */
			if classof m == TurboSmooth do
				m.enabled = False

			/* Turn on morphers */
			if classof m == Morpher do
				m.enabled = True

			if classof m == FFD_Binding do	
				m.enabled = True
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



function get_character_layers =
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



function get_abc_path =
(
	return maxfilepath + "ABC\\"
)



function get_char_name_from_layer layer_name =
(
	name_parts = filterString layer_name "_"
	the_name = ""
	for i = 1 to (name_parts.count - 1) do (
		the_name += name_parts[i]
		if i < (name_parts.count - 1) do
			the_name += "_"
	)
	return the_name
)



function get_abc_filename character_name =
(
	/* analayze max file name */
	file_name = getFilenameFile maxfilename
	name_parts = filterString file_name "_"
	filename = ""

	if name_parts.count < 3 do
		return filename

	/* 	combine first 3 name parts 
	*	Projectname_Episode_Scene_charactername
	*/
	filename += name_parts[1] + "_"
	filename += name_parts[2] + "_"
	filename += name_parts[3] + "_"
	filename += character_name + ".ABC"
	
	return filename
)


function select_layer_objects layer =
(
	clearSelection()
	local nodes
	layer.nodes &nodes
	select nodes
)


function get_abc_exporter =
(
	for plg in exporterPlugin.classes do
		if plg as string == "Alembic_Export" do
			return plg
	return undefined
)


clear_scene()
for layer in get_character_layers() do (
	select_layer_objects layer
	make_poly selection
	file_name = get_abc_filename (get_char_name_from_layer layer.name)
	full_filename = get_abc_path() + file_name
	makeDir (get_abc_path()) all:True
	exportFile full_filename #noPrompt selectedOnly:True using:(get_abc_exporter())
)

register = "macroScript scene2ABC "
register += "tooltip:\"TO ABC\" "
register += "category:\"Scene Tools\" "
register += "(filein \"" + getSourceFileName() +"\")"
execute(register)