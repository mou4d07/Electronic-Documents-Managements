import sys
import os
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

def convert_tif_to_jpg(tif_path, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Build the output file path
    base_name = os.path.splitext(os.path.basename(tif_path))[0]
    jpg_output_path = os.path.join(output_dir, base_name + ".jpg")

    # Skip if already converted
    if os.path.exists(jpg_output_path):
        print(f"⏭️ Skipped (already exists): {jpg_output_path}")
        return

    try:
        # Open and convert image
        with Image.open(tif_path) as img:
            # Convert image mode if necessary (some TIFs are 'RGBA' or 'P')
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.save(jpg_output_path, "JPEG", quality=90)
            print(f"✅ Converted: {tif_path} → {jpg_output_path}")
    except Exception as e:
        print(f"❌ Error converting {tif_path}: {e}")

def batch_convert_tifs(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.lower().endswith((".tif", ".tiff")):
            tif_path = os.path.join(input_dir, filename)
            convert_tif_to_jpg(tif_path, output_dir)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python tif_to_jpg_folder.py <input_dir> <output_dir>")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    batch_convert_tifs(input_dir, output_dir)
