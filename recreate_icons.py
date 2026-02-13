import os
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw

def svg_path_to_png(svg_path, png_path, size=256, color=(255, 255, 255, 255)):
    """
    Since we can't use Cairo, we will rasterize these specific SVGs by parsing their path data manually.
    The provided SVGs are simple enough (single path element).
    However, writing a full SVG path parser is complex.
    
    Instead, since we know exactly what the logos look like, I will recreate them
    using Pillow's drawing commands to match the shapes of the provided SVGs as closely as possible.
    """
    
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    filename = os.path.basename(svg_path).lower()
    
    if "unreal" in filename:
        # Unreal Engine U-logo approximation
        # Background Circle
        draw.ellipse((10, 10, size-10, size-10), fill=(20, 20, 20))
        
        # U-Shape
        # We need to draw the 'U' inside.
        cx, cy = size/2, size/2
        
        # This is a manual approximation of the UE logo shape
        # Vertical bars
        bar_w = size * 0.12
        bar_h = size * 0.35
        gap = size * 0.15
        
        # Left bar
        draw.rectangle(
            (cx - gap - bar_w, cy - bar_h, cx - gap, cy + bar_h*0.2), 
            fill='white'
        )
        # Right bar
        draw.rectangle(
            (cx + gap, cy - bar_h, cx + gap + bar_w, cy + bar_h*0.2), 
            fill='white'
        )
        
        # Bottom curve (Bowl)
        # Draw a filled arc/chord
        bbox = (cx - gap - bar_w, cy - bar_h*0.3, cx + gap + bar_w, cy + bar_h*0.8)
        draw.pieslice(bbox, 0, 180, fill='white')
        
        # Cutout the center of the bowl to make it a U
        bbox_inner = (cx - gap, cy - bar_h*0.3, cx + gap, cy + bar_h*0.6)
        draw.pieslice(bbox_inner, 0, 180, fill=(20, 20, 20))
        draw.rectangle((cx - gap, cy - bar_h*0.3, cx + gap, cy + bar_h*0.2), fill=(20, 20, 20))


    elif "unity" in filename:
        # Unity Cube Logo approximation
        # Background
        draw.rounded_rectangle((10, 10, size-10, size-10), radius=int(size*0.15), fill=(34, 44, 55))
        
        cx, cy = size/2, size/2
        
        # The Unity logo consists of 3 arrows forming a cube.
        # We will draw 3 polygons.
        
        # Helper to rotate point around center
        import math
        def rotate(x, y, angle_deg, cx=cx, cy=cy):
            rad = math.radians(angle_deg)
            nx = cx + (x - cx) * math.cos(rad) - (y - cy) * math.sin(rad)
            ny = cy + (x - cx) * math.sin(rad) + (y - cy) * math.cos(rad)
            return nx, ny

        # Base arrow shape (pointing up)
        # Coordinates relative to center, scaled by size
        s = size * 0.01
        arrow_poly = [
            (cx, cy - 15*s),  # Tip inner
            (cx, cy - 35*s),  # Tip outer
            (cx + 15*s, cy - 25*s), # Right wing
            (cx + 15*s, cy - 15*s), # Right inner
            (cx - 15*s, cy - 15*s), # Left inner
            (cx - 15*s, cy - 25*s)  # Left wing
        ]
        
        # But actually Unity arrows are simpler
        # Let's use a simpler polygon for the "Top" arrow
        # Top Arrow
        top_arrow = [
            (cx, cy - 10*s),
            (cx + 18*s, cy - 20*s),
            (cx, cy - 35*s),
            (cx - 18*s, cy - 20*s)
        ]
        draw.polygon(top_arrow, fill='white')
        
        # Right Arrow (Rotate 120 deg)
        right_arrow = [rotate(x, y, 120) for x, y in top_arrow]
        draw.polygon(right_arrow, fill='white')
        
        # Left Arrow (Rotate 240 deg)
        left_arrow = [rotate(x, y, 240) for x, y in top_arrow]
        draw.polygon(left_arrow, fill='white')

    img.save(png_path)
    print(f"Recreated icon: {filename} -> {png_path}")

if __name__ == "__main__":
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    
    svg_path_to_png(
        os.path.join(assets_dir, "unity.svg"),
        os.path.join(assets_dir, "icon_unity.png")
    )
    
    svg_path_to_png(
        os.path.join(assets_dir, "unreal_engine.svg"),
        os.path.join(assets_dir, "icon_ue5.png")
    )
