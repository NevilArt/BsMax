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

-- C:\Users\<USER>\AppData\Local\Autodesk\3dsMax\2020 - 64bit\ENU\usermacros
-- pathConfig.GetDir #userMacros

scriptPath = getFilenamePath  (getSourceFileName())
createdMacroCount = 0



function get_macro_name toolName =
(
    newString = ""
    lowerCaption = tolower toolName
    leagle = "abcdefghijklmnopqrstuvwxyz1234567890"
    
    for i = 1 to lowerCaption.count do (
        v = lowerCaption[i]
        isLeagel = False

        for j = 1 to leagle.count do (
            if v == leagle[j] do (
                isLeagel = True
                exit
            )
        )

        newString += if isLeagel then v else "_"
    )

    return newString
)


function update_macro category macroName script =
(
    userMacroPath = pathConfig.GetDir #userMacros
    userMacroPath += "\\"
    macroFileName = userMacroPath + category + "-" + macroName + ".mcr"
    
    openedMacroFile = openfile macroFileName mode:"w"
    format script to:openedMacroFile
    close openedMacroFile
)



function register toolName category fileName fnName arguments:#() =
(
    -- Register as Macro
    macroName = get_macro_name toolName

    argsStr = ""
    for i = 1 to arguments.count do (
        arg = arguments[i]
        argsStr += if ClassOf arg == String then "\""+ arg +"\""  else arg as string
        if i < arguments.count do (
            argsStr += ","
        )
    )

    --## Template Script for genarate user macro ##--
    templateScript  = "macroScript " + macroName + " "
    templateScript += "category:\"" + category +"\" "
    templateScript += "tooltip:\"" + toolName + "\"\n"
    templateScript += "(\n"
    templateScript += " print \"\""
    templateScript += ")"

    --## Main Script for replace inside the macro ##--
    script  = "macroScript " + macroName + " "
    script += "category:\"" + category +"\" "
    script += "tooltip:\"" + toolName + "\"\n"
    script += "(\n"
    
    -- Add script main file include
    if filename != "" do (
        /*
        script += " filein @\"" + scriptPath + filename + ".ms\"\n"
        Execute include couses copy all ms file inside the macro
        I need to put only one line code for include
        the only way is change the macro file after create
        */
        script += " include @\"" + scriptPath + filename + ".ms\"\n"
    )
    
    -- Add exutable function name with argoments
    script += " " + fnName + "("+ argsStr +")\n"

    script += ")"

    --## Create template macro script file ##--
    execute(templateScript)
    createdMacroCount += 1

    --## update macro with real script ##--
    update_macro category macroName script
)



function call fileName fnName =
(
    script = "filein @\"" + scriptPath + filename + ".ms\"\n"
    script += " " + fnName + "()\n"
    execute(script)
    createdMacroCount += 1
)



function print_log =
(
    actionMan.executeAction 0 "40472"
    -- clearlistener()
    logText = createdMacroCount as string + " macroscript inistaled."
    print logText
)



/* ABC */
register "Characters To ABC..." "Render Tools" "abc" "open_character_to_abc_dialog"

/* Animation */
register "Transform To Key..." "Nevil Tools" "animation" "open_transform_to_key_dialog"
-- register "Timeslider Tools..." "Nevil Tools" "animation" "open_time_slider_tool_dialog" --<<<<<<<<
register "Previous Key" "Animation Tools" "animation" "set_slider_time_to_previous_key"
register "Next Key" "Animation Tools" "animation" "set_slider_time_to_next_key"
register "Hide Bone Toggle" "Tools" "animation" "hide_bone_toggle"
register "Time Cam Tool" "Animation Tools" "animation" "open_camera_tools_dialog"
register "Character (Cat Rigg) Base Lister" "Animation Tools" "animation" "open_cat_character_base_lister"
register "Silhouate Toggle" "Animation Tools" "animation" "display_silhouate_toggle"
-- register "Auto Facial GUI" "Animation Tools" "auto_facial_gui" "open_auto_face_gui_dialog" --<<<<<<


-- /* Camera */
-- register "Copy Camera" "Nevil Tools" "camera" "copy_selected_transform_to_clipboard" --<<<<<<<<<<<<<
register "Physical Camera Convertor" "Camera Tools" "camera" "physical_camera_convertor"
register "Camera Movment Catcher" "Camera Tools" "camera" "camera_movment_catcher"


-- /* Character */
register "Character Auto Rename" "Nevil Tools" "character" "character_auto_rename" --<<<<<<<<<<<<<


-- /* Scene */
-- register "Instancer" "Nevil Tools" "scene" "open_instancer_dialog" --<<<<<<<
-- register "Arrange by Distance" "Nevil Tools" "scene" "arrange_by_distance" --<<<<<<
-- register "Arrange on path" "Nevil Tools" "scene" "arrange_on_shape" --<<<<<<<
-- register "Root Cleaner" "Nevil Tools" "scene" "open_root_cleaner"
-- register "Ground Picker" "Scene Tools" "scene" "open_ground_picker_dialog"
-- register "Copy..." "Scene Tools" "scene" "open_copy_dialog"
-- register "Paste..." "Scene Tools" "scene" "open_paste_dialog"
-- register "Mesh Layer Select" "Scene Tools" "scene" "mesh_layer_selector"
-- register "Dublicated Names Fixer" "Scene Tools" "scene" "fix_dublicated_names"
-- register "After Efect Time Calculator..." "Scene Tools" "scene" "open_afterefect_time_calculator"
-- register "Select My Layer" "Scene Tools" "scene" "select_my_layer"
-- register "Add Note Modifier" "Scene Tools" "scene" "add_note_modifier"
-- register "Multi Mesh Cache" "Scene Tools" "scene" "multi_mesh_cache"
-- register "Script Runner..." "Scene Tools" "scene" "open_script_runner_dialog"
-- register "Show None Xforms" "Scene Tools" "scene" "show_non_xform"
-- register "Set Select Filter All" "Scene Tools" "" "SetSelectFilter" arguments:#(1)
-- register "Set Select Filter Geometry" "Scene Tools" "" "SetSelectFilter" arguments:#(2)
-- register "Set Select Filter Shapes" "Scene Tools" "" "SetSelectFilter" arguments:#(3)
-- register "Set Select Filter Lights" "Scene Tools" "" "SetSelectFilter" arguments:#(4)
-- register "Set Select Filter Cameras" "Scene Tools" "" "SetSelectFilter" arguments:#(5)
-- register "Set Select Filter Helpers" "Scene Tools" "" "SetSelectFilter" arguments:#(6)
-- register "Set Select Filter Warps" "Scene Tools" "" "SetSelectFilter" arguments:#(7)
-- register "Set Select Filter Bone" "Scene Tools" "" "SetSelectFilter" arguments:#(8)
-- register "Set Select Filter IK Chain Object" "Scene Tools" "" "SetSelectFilter" arguments:#(9)
-- register "Set Select Filter Point" "Scene Tools" "" "SetSelectFilter" arguments:#(10)


-- /* Modeling */
-- call "modeling" "select_flat_surface"
-- register "Use Nurms 1" "Nevil Tools" "modeling" "poly_nurms_toggle" arguments:#(1)
-- register "Use Nurms 2" "Nevil Tools" "modeling" "poly_nurms_toggle" arguments:#(2)
-- register "Use Nurms 3" "Nevil Tools" "modeling" "poly_nurms_toggle" arguments:#(3)
-- register "Create Image Plane" "Nevil Tools" "modeling" "create_image_plane"
-- register "Pivot Tools" "Nevil Tools" "modeling" "open_pivot_tools_dialog"
-- register "Corner Edge Select" "Nevil Tools" "modeling" "corner_edge_select"


-- /* material */
-- register "New Material" "Nevil Tools" "material" "open_new_multi_material_creator_dialog"
-- register "Gray Material" "Nevil Tools" "material" "set_gray_material"
-- register "Remove Material" "Nevil Tools" "material" "remove_material"


-- /* render */
-- register "Redshift Proxy Renew" "Render Tools" "render" "redshift_proxy_renew"
-- register "Clear Render Output" "Render Tools" "render" "clear_render_output"
-- register "Wirecolore to Diffuse..." "Render Tools" "render" "wirecolor_to_standard_material"
-- register "Copy Render Path" "Render Tools" "render" "copy_render_out_path"


-- /* Rigg */
-- register "Make Stretch IK" "Rigg Tools" "rigg" "make_ik_stretchable"
-- register "Clear Transform Controllers" "Rigg Tools" "rigg" "clear_transform_controllers"
-- register "Spline Control" "Rigg Tools" "rigg" "spline_control"
-- register "Morpher Connector" "Rigg Tools" "rigg" "morpher_connector"
-- register "Joystick Creator" "Rigg Tools" "rigg" "joystick_creator"
-- register "HI Solver" "Rigg Tools" "rigg" "hi_solver"
-- register "Transform Holder" "Rigg Tools" "rigg" "open_transform_holder_dialog"

print_log()