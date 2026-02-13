import bpy
import os
import math
import platform
import subprocess
from .const import CUBEMAP_PRESETS
from .utils import install_pillow, is_pillow_installed

class CUBEMAP_OT_create_camera(bpy.types.Operator):
    bl_idname = "cubemap.create_camera"
    bl_label = "Create Cubemap Camera"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.camera_add(location=context.scene.cursor.location)
        cam = context.active_object
        cam.name = "CubemapCamera"
        context.scene.camera = cam
        self.report({'INFO'}, f"Camera '{cam.name}' created at cursor location")
        return {'FINISHED'}


class CUBEMAP_OT_setup_camera(bpy.types.Operator):
    bl_idname = "cubemap.setup_camera"
    bl_label = "Setup Camera for Cubemap"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        cam = context.scene.camera
        if cam is None:
            self.report({'ERROR'}, "No active camera in scene")
            return {'CANCELLED'}

        cam.data.type = 'PERSP'
        cam.data.angle = math.radians(90.0)
        cam.data.clip_start = 0.01
        cam.data.clip_end = 100.0

        scene = context.scene
        props = scene.cubemap_props
        scene.render.resolution_x = props.resolution
        scene.render.resolution_y = props.resolution
        scene.render.resolution_percentage = 100

        self.report({'INFO'}, f"Camera '{cam.name}' configured: 90° FOV, {props.resolution}x{props.resolution}")
        return {'FINISHED'}


class CUBEMAP_OT_apply_preset(bpy.types.Operator):
    bl_idname = "cubemap.apply_preset"
    bl_label = "Apply Preset"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.cubemap_props
        preset = CUBEMAP_PRESETS.get(props.engine_preset)
        if preset:
            props.file_format = preset['default_format']
            self.report({'INFO'}, f"Applied {preset['name']} preset")
        return {'FINISHED'}


class CUBEMAP_OT_render(bpy.types.Operator):
    bl_idname = "cubemap.render"
    bl_label = "Render Cubemap"
    bl_options = {'REGISTER'}

    def execute(self, context):
        scene = context.scene
        props = scene.cubemap_props
        cam = scene.camera

        if cam is None:
            self.report({'ERROR'}, "No active camera. Create or select a camera first.")
            return {'CANCELLED'}

        output_dir = bpy.path.abspath(props.output_path)
        if not output_dir or output_dir == "":
            self.report({'ERROR'}, "Output path is not set")
            return {'CANCELLED'}
        os.makedirs(output_dir, exist_ok=True)

        # Save original state
        orig_rot = cam.rotation_euler.copy()
        orig_rot_mode = cam.rotation_mode
        orig_filepath = scene.render.filepath
        orig_res_x = scene.render.resolution_x
        orig_res_y = scene.render.resolution_y
        orig_format = scene.render.image_settings.file_format

        # Setup render settings
        cam.rotation_mode = 'XYZ'
        scene.render.resolution_x = props.resolution
        scene.render.resolution_y = props.resolution
        scene.render.image_settings.file_format = props.file_format

        if props.file_format == 'OPEN_EXR':
            scene.render.image_settings.color_depth = '32'
            scene.render.image_settings.exr_codec = 'ZIP'

        cam.data.angle = math.radians(90.0)

        preset = CUBEMAP_PRESETS.get(props.engine_preset)
        if not preset:
            self.report({'ERROR'}, "Invalid engine preset")
            return {'CANCELLED'}

        faces = preset['faces']
        self.report({'INFO'}, f"Starting {preset['name']} cubemap render...")

        try:
            for idx, (suffix, rot) in enumerate(faces):
                cam.rotation_euler[0] = rot[0]
                cam.rotation_euler[1] = rot[1]
                cam.rotation_euler[2] = rot[2]

                filepath = os.path.join(output_dir, f"{props.base_name}_{idx+1}_{suffix}")
                scene.render.filepath = filepath
                
                # Update view layer to ensure camera update takes effect
                bpy.context.view_layer.update()

                bpy.ops.render.render(write_still=True)
                print(f"[{idx+1}/6] Rendered: {suffix} -> {filepath}")
                self.report({'INFO'}, f"Rendered {idx+1}/6: {suffix}")

        except Exception as e:
            self.report({'ERROR'}, f"Failed to render: {str(e)}")
            return {'CANCELLED'}
            
        finally:
            # Restore original state
            cam.rotation_euler = orig_rot
            cam.rotation_mode = orig_rot_mode
            scene.render.filepath = orig_filepath
            scene.render.resolution_x = orig_res_x
            scene.render.resolution_y = orig_res_y
            scene.render.image_settings.file_format = orig_format
            bpy.context.view_layer.update()

        self.report({'INFO'}, f"✓ {preset['name']} cubemap complete! 6 files saved to: {output_dir}")
        return {'FINISHED'}


class CUBEMAP_OT_install_pillow(bpy.types.Operator):
    bl_idname = "cubemap.install_pillow"
    bl_label = "Install Pillow"
    bl_description = "Install Pillow library required for cubemap assembly"

    def execute(self, context):
        self.report({'INFO'}, "Installing Pillow... Please wait (may take 30-60 seconds)")
        if install_pillow():
            self.report({'WARNING'}, "✓ Pillow installed! PLEASE RESTART BLENDER to activate it.")

            def draw(self_popup, context_popup):
                self_popup.layout.label(text="Pillow installed successfully!")
                self_popup.layout.label(text="Please RESTART Blender to use Assemble Cubemap")

            context.window_manager.popup_menu(draw, title="Restart Required", icon='INFO')
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Failed to install Pillow. Check console for details.")
            return {'CANCELLED'}


class CUBEMAP_OT_stitch(bpy.types.Operator):
    bl_idname = "cubemap.stitch"
    bl_label = "Assemble Cubemap"
    bl_options = {'REGISTER'}

    def execute(self, context):
        props = context.scene.cubemap_props
        output_dir = bpy.path.abspath(props.output_path)

        if not os.path.exists(output_dir):
            self.report({'ERROR'}, "Output folder doesn't exist. Render cubemap first.")
            return {'CANCELLED'}

        if not is_pillow_installed():
            self.report({'ERROR'}, "Pillow not installed or Blender not restarted. Click 'Install Pillow' then RESTART Blender.")
            return {'CANCELLED'}
        
        try:
            from PIL import Image
        except ImportError:
             self.report({'ERROR'}, "Pillow import failed despite check.")
             return {'CANCELLED'}

        preset = CUBEMAP_PRESETS.get(props.engine_preset)
        if not preset:
            self.report({'ERROR'}, "Invalid engine preset")
            return {'CANCELLED'}

        ext = ".exr" if props.file_format == 'OPEN_EXR' else (".png" if props.file_format == 'PNG' else ".jpg")
        if ext == ".exr":
            self.report({'ERROR'}, "EXR stitching not supported. Change format to PNG or JPEG.")
            return {'CANCELLED'}

        images = []
        for idx, (suffix, _) in enumerate(preset['faces']):
            filepath = os.path.join(output_dir, f"{props.base_name}_{idx+1}_{suffix}{ext}")
            if not os.path.exists(filepath):
                self.report({'ERROR'}, f"File not found: {filepath}. Render cubemap first.")
                return {'CANCELLED'}
            try:
                img = Image.open(filepath)
                images.append(img)
            except Exception as e:
                self.report({'ERROR'}, f"Failed to open {filepath}: {str(e)}")
                return {'CANCELLED'}

        widths, heights = zip(*(i.size for i in images))
        total_width = sum(widths)
        max_height = max(heights)

        stitched = Image.new('RGB', (total_width, max_height))

        x_offset = 0
        for img in images:
            stitched.paste(img, (x_offset, 0))
            x_offset += img.size[0]

        output_path = os.path.join(output_dir, f"{props.base_name}_cubemap_strip{ext}")
        try:
            stitched.save(output_path)
        except Exception as e:
             self.report({'ERROR'}, f"Failed to save stitched image: {e}")
             return {'CANCELLED'}

        self.report({'INFO'}, f"✓ Cubemap strip saved: {output_path} ({total_width}x{max_height})")
        return {'FINISHED'}


class CUBEMAP_OT_open_folder(bpy.types.Operator):
    bl_idname = "cubemap.open_folder"
    bl_label = "Open Output Folder"

    def execute(self, context):
        props = context.scene.cubemap_props
        output_dir = bpy.path.abspath(props.output_path)

        if not os.path.exists(output_dir):
            self.report({'WARNING'}, "Output folder doesn't exist yet")
            return {'CANCELLED'}

        try:
            if platform.system() == "Windows":
                os.startfile(output_dir)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", output_dir])
            else:
                subprocess.Popen(["xdg-open", output_dir])
            self.report({'INFO'}, f"Opened: {output_dir}")
        except Exception as e:
            self.report({'ERROR'}, f"Could not open folder: {str(e)}")
            return {'CANCELLED'}

        return {'FINISHED'}


class CUBEMAP_OT_check_pillow(bpy.types.Operator):
    bl_idname = "cubemap.check_pillow"
    bl_label = "Check Pillow Version"

    def execute(self, context):
        try:
            from PIL import Image
            version = Image.__version__ if hasattr(Image, '__version__') else "Unknown"
            self.report({'INFO'}, f"Pillow version: {version}")
        except ImportError:
            self.report({'ERROR'}, "Pillow is not installed. Please install it from preferences.")
            return {'CANCELLED'}

        return {'FINISHED'}

