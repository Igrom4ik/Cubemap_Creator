import bpy
from .const import CUBEMAP_PRESETS
from .utils import is_pillow_installed

class CUBEMAP_PT_main_panel(bpy.types.Panel):
    bl_label = "Cubemap Renderer"
    bl_idname = "CUBEMAP_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Cubemap'

    def draw(self, context):
        layout = self.layout
        props = context.scene.cubemap_props
        
        # Get icons
        from . import preview_collections
        pcoll = preview_collections.get("main")
        
        # Helper to safely get icon_id
        def get_icon(name):
            if pcoll and name in pcoll:
                return pcoll[name].icon_id
            return 0  # Fallback to no icon if missing
        
        layout.use_property_split = True
        layout.use_property_decorate = False

        # --- HEADER ---
        row = layout.row()
        row.scale_y = 1.2
        row.label(text="Target Engine", icon='GAME')
        
        # --- ENGINE SELECTION ---
        row = layout.row(align=True)
        row.scale_y = 1.5
        row.prop(props, "engine_preset", expand=True)
        
        preset = CUBEMAP_PRESETS.get(props.engine_preset)
        if preset:
            # Show Engine Logo
            box = layout.box()
            col = box.column(align=True)
            
            # Logo Row
            row = col.row()
            row.alignment = 'CENTER'
            icon_name = f"ICON_{props.engine_preset}" # ICON_UE5 or ICON_UNITY
            logo_icon_id = get_icon(icon_name)
            
            if logo_icon_id:
                # Big icon hack: create a button or label with scale
                row.template_icon(icon_value=logo_icon_id, scale=3.0)
            else:
                row.label(text=preset['name'], icon='INFO')

            col.separator()
            row = col.row()
            row.alignment = 'CENTER'
            row.label(text=f"Faces: {preset['order_label']}")

        layout.separator()

        # --- CAMERA SETUP ---
        box = layout.box()
        row = box.row()
        row.label(text="Camera", icon='CAMERA_DATA')
        
        cam = context.scene.camera
        if cam and "Cubemap" in cam.name:
             row.label(text="Ready", icon='CHECKMARK')
        elif cam:
             row.label(text="Active", icon='INFO')
        else:
             row.label(text="Missing", icon='ERROR')

        col = box.column(align=True)
        
        row = col.row(align=True)
        row.scale_y = 1.2
        if not cam:
            row.operator("cubemap.create_camera", text="Create Camera", icon='ADD')
        else:
            row.operator("cubemap.setup_camera", text="Setup Camera Settings", icon='SETTINGS')

        layout.separator()

        # --- OUTPUT SETTINGS ---
        box = layout.box()
        box.label(text="Output", icon='OUTPUT')
        
        col = box.column(align=True)
        col.prop(props, "output_path", text="Path")
        col.prop(props, "base_name", text="Filename")
        
        col.separator()
        
        sub = col.row(align=True)
        sub.prop(props, "resolution", text="Res")
        sub.prop(props, "file_format", text="")

        # --- ACTIONS ---
        layout.separator()
        layout.label(text="Actions", icon='PLAY')

        col = layout.column(align=True)
        col.scale_y = 1.6
        
        # Render Button
        icon_render = get_icon("ICON_RENDER")
        if icon_render:
            col.operator("cubemap.render", text="Render Faces", icon_value=icon_render)
        else:
            col.operator("cubemap.render", text="Render Faces", icon='RENDER_STILL')
        
        col.separator()
        
        # Assemble Button
        if is_pillow_installed():
            icon_assemble = get_icon("ICON_ASSEMBLE")
            if icon_assemble:
                col.operator("cubemap.stitch", text="Assemble Strip", icon_value=icon_assemble)
            else:
                col.operator("cubemap.stitch", text="Assemble Strip", icon='IMAGE_PLANE')
        else:
            box_err = col.box()
            box_err.alert = True
            box_err.label(text="Library Missing", icon='ERROR')
            box_err.operator("cubemap.install_pillow", text="Install Pillow", icon='IMPORT')

        # Open Folder
        row = layout.row()
        row.scale_y = 1.0
        icon_folder = get_icon("ICON_FOLDER")
        if icon_folder:
            row.operator("cubemap.open_folder", text="Open Output Folder", icon_value=icon_folder)
        else:
            row.operator("cubemap.open_folder", text="Open Output Folder", icon='FOLDER_REDIRECT')
