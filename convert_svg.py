import os
import cairosvg

def convert_svg_to_png(svg_path, png_path, size=256):
    try:
        if not os.path.exists(svg_path):
            print(f"Error: {svg_path} not found")
            return

        cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=size, output_height=size)
        print(f"Converted: {svg_path} -> {png_path}")
    except Exception as e:
        print(f"Failed to convert {svg_path}: {e}")

if __name__ == "__main__":
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    
    # Unity
    convert_svg_to_png(
        os.path.join(assets_dir, "unity.svg"),
        os.path.join(assets_dir, "icon_unity.png")
    )
    
    # Unreal
    convert_svg_to_png(
        os.path.join(assets_dir, "unreal_engine.svg"),
        os.path.join(assets_dir, "icon_ue5.png")
    )
