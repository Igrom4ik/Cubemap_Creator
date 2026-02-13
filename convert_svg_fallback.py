import os
import re

def convert_simple_svg_to_png(svg_path, png_path, size=256):
    """
    A very simple SVG parser that approximates the shapes using Pillow.
    This is a fallback since Cairo is not available.
    """
    from PIL import Image, ImageDraw
    
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    filename = os.path.basename(svg_path).lower()
    
    # Custom drawing based on file type since we can't truly parse SVG without heavy libs
    if "unreal" in filename:
        # Draw Unreal-like icon
        # Circle
        draw.ellipse((10, 10, size-10, size-10), fill=(20, 20, 20))
        # U Shape
        cx, cy = size/2, size/2
        r = size * 0.35
        # U Arc
        draw.arc((cx-r, cy-r, cx+r, cy+r), 0, 180, fill='white', width=int(size*0.1))
        # U Vertical lines
        w = int(size*0.1)
        draw.line((cx-r, cy, cx-r, cy-r*0.5), fill='white', width=w)
        draw.line((cx+r, cy, cx+r, cy-r*0.5), fill='white', width=w)
        
    elif "unity" in filename:
        # Draw Unity-like icon
        # Background
        draw.rounded_rectangle((10, 10, size-10, size-10), radius=int(size*0.15), fill=(34, 44, 55))
        
        # Cube arrows
        cx, cy = size/2, size/2
        off = size * 0.2
        
        # Top
        draw.polygon([
            (cx, cy - off*1.8),
            (cx + off, cy - off),
            (cx, cy),
            (cx - off, cy - off)
        ], fill='white')
        
        # Right
        draw.polygon([
            (cx + off*0.2, cy + off*0.2),
            (cx + off*1.2, cy - off*0.4),
            (cx + off*0.8, cy + off*0.8),
            (cx - off*0.2, cy + off*1.4)
        ], fill='white')
        
        # Left (mirrored roughly)
        draw.polygon([
            (cx - off*0.2, cy + off*0.2),
            (cx - off*1.2, cy - off*0.4),
            (cx - off*0.8, cy + off*0.8),
            (cx + off*0.2, cy + off*1.4)
        ], fill='white')
        
    img.save(png_path)
    print(f"Generated approximation for: {filename} -> {png_path}")

if __name__ == "__main__":
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    
    convert_simple_svg_to_png(
        os.path.join(assets_dir, "unity.svg"),
        os.path.join(assets_dir, "icon_unity.png")
    )
    
    convert_simple_svg_to_png(
        os.path.join(assets_dir, "unreal_engine.svg"),
        os.path.join(assets_dir, "icon_ue5.png")
    )
