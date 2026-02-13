bl_info = {
    "name": "Cubemap Renderer",
    "author": "Igor Unguryanov",
    "version": (1, 5, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > Cubemap",
    "description": "Render cubemaps for UE5 POM interiors and Unity",
    "category": "Render",
    "doc_url": "",
    "tracker_url": "",
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
    CUBEMAP_OT_check_pillow,
)
from .panels import CUBEMAP_PT_main_panel, CUBEMAP_PT_prefs

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
    CUBEMAP_OT_check_pillow,
    CUBEMAP_PT_main_panel,
    CUBEMAP_PT_prefs,
)

def register():
    # Register classes
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.cubemap_props = bpy.props.PointerProperty(type=CubemapProperties)

    # Register icons
    pcoll = bpy.utils.previews.new()
    icons_dir = os.path.join(os.path.dirname(__file__), "assets")
    
    # Load PNG icons
    if os.path.exists(icons_dir):
        def load_icon(name, filename):
            path = os.path.join(icons_dir, filename)
            if os.path.exists(path):
                try:
                    icon = pcoll.load(name, path, 'IMAGE')
                    print(f"✓ Loaded icon: {name} from {filename}")
                    return True
                except Exception as e:
                    print(f"⚠ Failed to load icon {filename}: {e}")
                    return False
            else:
                print(f"✗ Icon file not found: {path}")
                return False

        # Load all icons
        load_icon("ICON_UE5", "icon_ue5.png")
        load_icon("ICON_UNITY", "icon_unity.png")
        load_icon("ICON_RENDER", "icon_render.png")
        load_icon("ICON_ASSEMBLE", "icon_assemble.png")
        load_icon("ICON_FOLDER", "icon_folder.png")
    else:
        print(f"✗ Assets directory not found: {icons_dir}")

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
