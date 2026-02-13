import bpy
from bpy.props import StringProperty, IntProperty, EnumProperty, PointerProperty
from .const import CUBEMAP_PRESETS

def update_engine_preset(self, context):
    props = context.scene.cubemap_props
    preset = CUBEMAP_PRESETS.get(props.engine_preset)
    if preset:
        props.file_format = preset['default_format']

class CubemapProperties(bpy.types.PropertyGroup):
    engine_preset: EnumProperty(
        name="Engine",
        description="Target game engine (affects face naming and order)",
        items=[
            ('UE5', "Unreal Engine 5", "Cubemap for UE5 (posx, negx, posy, negy, posz, negz)"),
            ('UNITY', "Unity", "Cubemap for Unity (right, left, up, down, front, back)"),
        ],
        default='UE5',
        update=update_engine_preset
    )

    output_path: StringProperty(
        name="Output Folder",
        description="Folder to save cubemap faces. Use // for relative path to .blend file",
        default="//cubemaps/",
        subtype='DIR_PATH'
    )

    base_name: StringProperty(
        name="File Name",
        description="Base filename for cubemap faces",
        default="room"
    )

    resolution: IntProperty(
        name="Resolution",
        description="Resolution of each cubemap face (square)",
        default=2048,
        min=512,
        max=8192,
        step=512
    )

    file_format: EnumProperty(
        name="Format",
        description="Image file format",
        items=[
            ('PNG', "PNG (.png)", "Standard PNG format, lossless"),
            ('JPEG', "JPEG (.jpg)", "JPEG format (lossy, smaller file size)"),
        ],
        default='PNG'
    )
