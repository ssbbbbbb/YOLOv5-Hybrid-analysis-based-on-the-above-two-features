from PIL import Image
import os

def overlay_images(base_image_path, overlay_image_path, output_path, transparency):
    """
    Overlay an image (with reduced transparency) onto another image.

    :param base_image_path: Path to the base image (background)
    :param overlay_image_path: Path to the overlay image
    :param output_path: Path to save the result
    :param transparency: Transparency level for the overlay image (0 to 255)
    """
    # Open the base image
    base_image = Image.open(base_image_path).convert("RGBA")

    # Open the overlay image
    overlay_image = Image.open(overlay_image_path).convert("RGBA")

    # Resize the overlay image to match the base image size
    overlay_image = overlay_image.resize(base_image.size, Image.LANCZOS)

    # Adjust the overlay image's transparency
    overlay_alpha = overlay_image.split()[3].point(lambda p: p * (transparency / 255.0))
    overlay_image.putalpha(overlay_alpha)

    # Composite the images
    combined = Image.alpha_composite(base_image, overlay_image)

    # Save the resulting image
    combined.save(output_path, format="PNG")

def batch_overlay_images(base_dir, overlay_dir, output_dir, transparency):
    """
    Overlay images from one directory onto images in another directory in order.

    :param base_dir: Directory containing base images
    :param overlay_dir: Directory containing overlay images
    :param output_dir: Directory to save output images
    :param transparency: Transparency level for the overlay image (0 to 255)
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    base_images = sorted(os.listdir(base_dir))
    overlay_files = sorted(os.listdir(overlay_dir))

    for base_file, overlay_file in zip(base_images, overlay_files):
        base_image_path = os.path.join(base_dir, base_file)
        overlay_image_path = os.path.join(overlay_dir, overlay_file)

        if not os.path.isfile(base_image_path) or not os.path.isfile(overlay_image_path):
            continue

        try:
            output_path = os.path.join(output_dir, base_file)
            overlay_images(base_image_path, overlay_image_path, output_path, transparency)
            print(f"Processed: {base_file} with {overlay_file}")
        except Exception as e:
            print(f"Failed to process {base_file} with {overlay_file}: {e}")


# Example usage
base_dir = r"C:\Users\蕭宗賓\Desktop\AI local\work\動態2\2進\vtflooder" # Replace with the path to your base images directory
overlay_dir = r"C:\Users\蕭宗賓\Desktop\AI local\work\動態1\reports\image1\vtflooder"  # Replace with the path to your overlay images directory
output_dir = r"C:\Users\蕭宗賓\Desktop\AI local\work\動態3\image\vtflooder"  # Replace with the path to save output images
transparency = 128  # Set transparency level (0 is fully transparent, 255 is fully opaque)

batch_overlay_images(base_dir, overlay_dir, output_dir, transparency)
