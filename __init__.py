bl_info = {
    "name": "Cubemap Renderer",
    "author": "Igor Unguryanov",
    "version": (1, 5, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > Cubemap",
    "description": "Render cubemaps for UE5 POM interiors and Unity",
    "category": "Render",
    "doc_url": "https://github.com/Igrom4ik/Cubemap_Creator",
    "tracker_url": "https://github.com/Igrom4ik/Cubemap_Creator/issues",
}

import bpy
import os
import bpy.utils.previews

from .properties import CubemapProperties
from .operators import (
    CUBEMAP_OT_create_camera,
    CUBEMAP_OT_setup_camera,
    CUBEMAP_OT_apply_preset,
    CUBEMAP_OT_render,
    CUBEMAP_OT_install_pillow,
    CUBEMAP_OT_stitch,
    CUBEMAP_OT_open_folder,
)
from .panels import CUBEMAP_PT_main_panel

# Global preview collection
preview_collections = {}

classes = (
    CubemapProperties,
    CUBEMAP_OT_create_camera,
    CUBEMAP_OT_setup_camera,
    CUBEMAP_OT_apply_preset,
    CUBEMAP_OT_render,
    CUBEMAP_OT_install_pillow,
    CUBEMAP_OT_stitch,
    CUBEMAP_OT_open_folder,
    CUBEMAP_PT_main_panel,
)

def register():
    # Register classes
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.cubemap_props = bpy.props.PointerProperty(type=CubemapProperties)

    # Register icons
    pcoll = bpy.utils.previews.new()
    icons_dir = os.path.join(os.path.dirname(__file__), "assets")
    
    # Load SVG icons
    if os.path.exists(icons_dir):
        # We assume Blender 4.2+ supports SVG loading for previews
        # If not, we would need to convert to PNG.
        
        # Helper to load icon if exists
        def load_icon(name, filename):
            path = os.path.join(icons_dir, filename)
            if os.path.exists(path):
                try:
                    pcoll.load(name, path, 'IMAGE')
                except Exception as e:
                    print(f"Failed to load icon {filename}: {e}")

        load_icon("ICON_UE5", "unreal_engine.svg")
        load_icon("ICON_UNITY", "unity.svg")
        load_icon("ICON_RENDER", "icon_render.svg")
        load_icon("ICON_ASSEMBLE", "icon_assemble.svg")
        load_icon("ICON_FOLDER", "icon_folder.svg")
        
    preview_collections["main"] = pcoll

def unregister():
    # Unregister icons
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()

    # Unregister classes
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.cubemap_props

if __name__ == "__main__":
    register()
