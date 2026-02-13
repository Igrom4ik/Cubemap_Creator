#!/usr/bin/env python3
"""
Generate colorful PNG icons for Cubemap Renderer buttons.
Uses Pillow to create simple, colorful icons.
"""

from PIL import Image, ImageDraw
import os

assets_dir = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(assets_dir, exist_ok=True)

def create_render_icon():
    """Create a colorful render/camera icon."""
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Camera body (dark blue)
    draw.rectangle((40, 60, 216, 180), fill=(41, 128, 185), outline=(25, 75, 130), width=3)

    # Camera lens (yellow circle)
    draw.ellipse((95, 95, 161, 161), fill=(243, 156, 18), outline=(230, 126, 0), width=3)

    # Lens inner circle
    draw.ellipse((110, 110, 146, 146), fill=(255, 200, 87))

    img.save(os.path.join(assets_dir, "icon_render.png"))
    print("✓ Created icon_render.png")

def create_assemble_icon():
    """Create a colorful assemble/stitch icon."""
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Two overlapping squares (green)
    draw.rectangle((30, 60, 140, 170), fill=(46, 204, 113), outline=(25, 135, 84), width=3)
    draw.rectangle((116, 86, 226, 196), fill=(52, 152, 219), outline=(25, 100, 155), width=3)

    img.save(os.path.join(assets_dir, "icon_assemble.png"))
    print("✓ Created icon_assemble.png")

def create_folder_icon():
    """Create a colorful folder icon."""
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Folder tab (orange)
    draw.rectangle((50, 50, 140, 90), fill=(230, 126, 34), outline=(180, 95, 20), width=2)

    # Folder body (orange, slightly darker)
    draw.rectangle((40, 85, 216, 200), fill=(243, 156, 18), outline=(180, 95, 20), width=3)

    img.save(os.path.join(assets_dir, "icon_folder.png"))
    print("✓ Created icon_folder.png")

def create_ue5_icon():
    """Create a colorful UE5 logo icon."""
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background circle (blue)
    draw.ellipse((30, 30, 226, 226), fill=(52, 152, 219), outline=(25, 100, 155), width=3)

    # White U-shape
    # Left vertical bar
    draw.rectangle((70, 100, 95, 170), fill=(255, 255, 255))
    # Bottom horizontal bar
    draw.rectangle((70, 170, 161, 185), fill=(255, 255, 255))
    # Right vertical bar
    draw.rectangle((161, 100, 186, 170), fill=(255, 255, 255))

    img.save(os.path.join(assets_dir, "icon_ue5.png"))
    print("✓ Created icon_ue5.png")

def create_unity_icon():
    """Create a colorful Unity logo icon."""
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background (white)
    draw.rectangle((0, 0, size, size), fill=(255, 255, 255))

    # Unity symbol: three triangles forming a circle
    # This is a simplified version
    points_top = [(128, 60), (170, 140), (86, 140)]
    points_bottom_left = [(60, 150), (100, 230), (40, 200)]
    points_bottom_right = [(196, 150), (216, 200), (156, 230)]

    draw.polygon(points_top, fill=(0, 0, 0))
    draw.polygon(points_bottom_left, fill=(0, 0, 0))
    draw.polygon(points_bottom_right, fill=(0, 0, 0))

    img.save(os.path.join(assets_dir, "icon_unity.png"))
    print("✓ Created icon_unity.png")

if __name__ == "__main__":
    print("Generating colorful PNG icons...")
    create_render_icon()
    create_assemble_icon()
    create_folder_icon()
    create_ue5_icon()
    create_unity_icon()
    print("\n✅ All icons created successfully!")

