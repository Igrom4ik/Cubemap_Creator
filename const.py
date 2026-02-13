import math

# Presets for cubemaps
CUBEMAP_PRESETS = {
    'UE5': {
        'name': 'Unreal Engine 5',
        'faces': [
            ("posx", (math.radians(90), 0, math.radians(90))),
            ("negx", (math.radians(90), 0, math.radians(-90))),
            ("negy", (math.radians(180), 0, 0)),
            ("posy", (math.radians(180), math.radians(180), 0)),
            ("posz", (math.radians(90), 0, math.radians(180))),
            ("negz", (math.radians(90), 0, 0)),
        ],
        'order_label': '+X, -X, -Y, +Y, +Z, -Z',
        'default_format': 'OPEN_EXR',
    },
    'UNITY': {
        'name': 'Unity',
        'faces': [
            ("right", (math.radians(90), 0, math.radians(90))),
            ("left", (math.radians(90), 0, math.radians(-90))),
            ("up", (math.radians(0), 0, 0)),
            ("down", (math.radians(180), 0, 0)),
            ("front", (math.radians(90), 0, 0)),
            ("back", (math.radians(90), 0, math.radians(180))),
        ],
        'order_label': 'right, left, up, down, front, back',
        'default_format': 'PNG',
    },
}
