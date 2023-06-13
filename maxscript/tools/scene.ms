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



function has_skin Obj =
(
    local result = false
    for m in Obj.modifiers do (
        if classof m == Skin do (
            result = true
            exit
        )
    )
    return result
)

function find_skin Objs =
(
    local result = false
    for o in Objs do (
        if has_skin o do (
            result = true
            exit
        )
    )
    return result
)


function get_master_layer Layer =
(
    Ret = undefined
    while true do (
        LP = Layer.getParent()
        if LP != undefined then (
            Ret = LP
            Layer = LP
        )
        else (
            exit
        )
    )
    return ret
)


function mesh_layer_selector =
(
	meshLayers = #()
	MeshObjs = #()

    -- create a beter method to get all characters
    CatParents = ( for obj in helpers where classof obj == CATParent collect obj )

    for C in CatParents do (
        MasterLayer = get_master_layer C.Layer
        for i = 1 to MasterLayer.getNumChildren() do (
            M = MasterLayer.getChild i
            M.Nodes &objs
            if find_skin objs do (
                append meshLayers M
                exit
            )
        )
    )

    for M in meshLayers do (
        M.Nodes &objs
        join MeshObjs objs
    )

    select MeshObjs
)



function fix_dublicated_names =
(
	names = #()
	for o in objects do (
		for n in names do (
            if o.name == n then (
                o.name = uniquename o.name
                break
            )
        )
		append names o.name
	)
)



function select_my_layer =
(
	local Objs = #()
	for S in Selection do (
		NewObjs = #()
		S.layer.Nodes &NewObjs
		join Objs NewObjs
	)
	select Objs
)



function add_note_modifier =
(
	NoteModifier = (EmptyModifier ())
	NoteModifier.name = "Note"
	addModifier selection NoteModifier 

    ca = attributes addNoteAttribute
	(
		parameters params_pr rollout:params_ro
		(
			note type:#string ui:note_et
		)
		rollout params_ro "Note"
		( 
			edittext note_et "" pos:[-1,3] width:160 height:500
		)
	)

    for i in selection do (
        custAttributes.add i.modifiers[#Note] ca
    )
)



function multi_mesh_cache =
(
    if selection.count == 0 do (
        return undefined
    )

    slidertime = 0
    OrigObjs = selection as array
    NewObjs = #()
    maxOps.CloneNodes OrigObjs cloneType:#instance newNodes:&NewObjs
    select NewObjs
    macros.run "Modifier Stack" "Convert_to_Mesh"
    NewNode = NewObjs[1]

    local OrigTransform = NewNode.transform

    try( NewNode.Transform.controller = prs ())catch()
    try( NewNode.pos.controller = Position_XYZ ())catch()
    try(NewNode.pos.controller.X_Position.controller = bezier_float ())catch()
    try(NewNode.pos.controller.Y_Position.controller = bezier_float ())catch()
    try(NewNode.pos.controller.Z_Position.controller = bezier_float ())catch()

    try(NewNode.rotation.controller = Euler_XYZ ())catch()
    try(NewNode.rotation.controller.X_Rotation.controller = bezier_float ())catch()
    try(NewNode.rotation.controller.Y_Rotation.controller = bezier_float ())catch()
    try(NewNode.rotation.controller.Z_Rotation.controller = bezier_float ())catch()

    try(NewNode.scale.controller = bezier_scale ())catch()
    try(NewNode.transform = OrigTransform)catch()

    NewNode.Parent = Undefined	
    NewNode.transform = OrigTransform
    NewNode.name += "_PCache"
    deleteItem NewObjs 1
    addModifier NewNode (Edit_Poly())
    select NewNode
    setCommandPanelTaskMode #modify
    NewNode.modifiers[#Edit_Poly].AttachList NewObjs
    addModifier NewNode (Edit_Mesh())
    maxOps.CollapseNode NewNode true

    addModifier NewNode (Skin_Wrap())
    NewNode.modifiers[#Skin_Wrap].engine = 0
    NewNode.modifiers[#Skin_Wrap].meshList = OrigObjs
    addModifier NewNode (Point_Cache())
)



function show_non_xform =
(
    select (for obj in objects where obj.scale != [1, 1, 1] collect obj)
)



function hide_by_layer =
(
    for S in Selection do (
        S.layer.on = false
    )
)