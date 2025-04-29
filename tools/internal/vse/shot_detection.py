# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Detect Shots and Split Strips",
    "author": "Tintwotin, Brandon Castellano(PySceneDetect-module)",
    "version": (1, 0),
    "blender": (2, 90, 0),
    "location": "Sequencer > Strip Menu or Context Menu",
    "description": "Detect shots in active strip and split all selected strips accordingly.",
    "warning": "",
    "doc_url": "",
    "category": "Sequencer",
}

import bpy, subprocess, os, sys
from bpy.types import Operator
from bpy.props import (
    IntProperty,
    BoolProperty,
    EnumProperty,
    StringProperty,
    FloatProperty,
)
#import site
#app_path = site.USER_SITE
#if app_path not in sys.path:
#    sys.path.append(app_path)

def find_scenes(video_path, threshold, start, end):
    pybin = sys.executable  # bpy.app.binary_path_python # Use for 2.83
    try:
        subprocess.call([pybin, "-m", "ensurepip"])
    except ImportError:
        pass
    try:
        from scenedetect import open_video#, detect
        from scenedetect import SceneManager
        from scenedetect.detectors import ContentDetector
    except ImportError:
        subprocess.check_call([pybin, "-m", "pip", "install", "scenedetect[opencv]"])
        from scenedetect import open_video#, detect
        from scenedetect import SceneManager
        from scenedetect.detectors import ContentDetector
        
    render = bpy.context.scene.render
    fps = round((render.fps / render.fps_base), 3)
    video = open_video(video_path,framerate=fps)
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=threshold))
    video.seek((start/fps))
    scene_manager.detect_scenes(video, end_time=(end/fps))

    return scene_manager.get_scene_list()


class SEQUENCER_OT_split_selected(bpy.types.Operator):
    """Split Unlocked Un/Seleted Strips Soft"""

    bl_idname = "sequencer.split_selected"
    bl_label = "Split Selected"
    bl_options = {"REGISTER", "UNDO"}

    type: EnumProperty(
        name="Type",
        description="Split Type",
        items=(
            ("SOFT", "Soft", "Split Soft"),
            ("HARD", "Hard", "Split Hard"),
        ),
    )

    @classmethod
    def poll(cls, context):
        if context.sequences:
            return True
        return False

    def execute(self, context):
        selection = context.selected_sequences
        sequences = bpy.context.scene.sequence_editor.sequences_all
        cf = bpy.context.scene.frame_current
        at_cursor = []
        cut_selected = False

        # find unlocked strips at cursor
        for s in sequences:
            if s.frame_final_start <= cf and s.frame_final_end > cf:
                if s.lock == False:
                    at_cursor.append(s)
                    if s.select == True:
                        cut_selected = True
        for s in at_cursor:
            if cut_selected:
                if s.select:  # only cut selected
                    bpy.ops.sequencer.select_all(action="DESELECT")
                    s.select = True
                    bpy.ops.sequencer.split(
                        frame=bpy.context.scene.frame_current,
                        type=self.type,
                        side="RIGHT",
                    )

                    # add new strip to selection
                    for i in bpy.context.scene.sequence_editor.sequences_all:
                        if i.select:
                            selection.append(i)
                    bpy.ops.sequencer.select_all(action="DESELECT")
                    for s in selection:
                        s.select = True
        return {"FINISHED"}


class SEQUENCER_OT_detect_shots(Operator):
    """Detect shots in active strip and split all selected strips accordingly"""

    bl_idname = "sequencer.detect_shots"
    bl_label = "Detect Shots & Split Strips"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if (
            context.scene
            and context.scene.sequence_editor
            and context.scene.sequence_editor.active_strip
        ):
            return context.scene.sequence_editor.active_strip.type == "MOVIE"
        else:
            return False

    def execute(self, context):
        scene = context.scene
        sequencer = bpy.ops.sequencer
        cf = context.scene.frame_current
        path = context.scene.sequence_editor.active_strip.filepath
        path = (os.path.realpath(bpy.path.abspath(path))).replace("\\", "\\\\")

        msg = "Please wait. Detecting shots in "+str(path)+"."
        self.report({'INFO'}, msg)
        
        path = path.replace("\\", "\\\\")
        active = context.scene.sequence_editor.active_strip
        start_time = active.frame_offset_start
        end_time = active.frame_duration - active.frame_offset_end
        scenes = find_scenes(path, 32, start_time, end_time)
        for i, scene in enumerate(scenes):
            context.scene.frame_current = int(scene[1].get_frames()+active.frame_start)
            sequencer.split_selected()

        context.scene.frame_current = cf

        msg = "Finished: Shot detection and strip splitting."
        self.report({'INFO'}, msg)
        return {'FINISHED'}


def menu_detect_shots(self, context):
    self.layout.separator()
    self.layout.operator("sequencer.detect_shots")


classes = (
    SEQUENCER_OT_detect_shots,
    SEQUENCER_OT_split_selected,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.SEQUENCER_MT_context_menu.append(menu_detect_shots)
    bpy.types.SEQUENCER_MT_strip.append(menu_detect_shots)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    bpy.types.SEQUENCER_MT_context_menu.remove(menu_detect_shots)
    bpy.types.SEQUENCER_MT_strip.remove(menu_detect_shots)


if __name__ == "__main__":
    register()
