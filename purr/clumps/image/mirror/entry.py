import typer
import glob
import os
from PIL import Image

# app = typer.Typer()

def mirror_image(image_path: str, output_dir: str):
    img = Image.open(image_path)
    img_width, img_height = img.size
    new_img = Image.new("RGB", (img_width * 2, img_height))
    new_img.paste(img, (0, 0))
    new_img.paste(img.transpose(Image.FLIP_LEFT_RIGHT), (img_width, 0))

    basename = os.path.basename(image_path)
    filename, ext = os.path.splitext(basename)
    output_path_left = os.path.join(output_dir, f"{filename}_left{ext}")

    new_img.save(output_path_left)

    new_img = Image.new("RGB", (img_width * 2, img_height))
    new_img.paste(img.transpose(Image.FLIP_LEFT_RIGHT), (0, 0))
    new_img.paste(img, (img_width, 0))

    output_path_right = os.path.join(output_dir, f"{filename}_right{ext}")
    new_img.save(output_path_right)

def main(paths: list[str], output: str = typer.Option(None, "-o", "--output", help="Output directory.")):
    """
    Mirror an image.

    :param paths: The path to the source image.
    :param output: The directory where the mirrored image will be saved.
    """
    print('Running the mirror script!')
    # for path in paths:
    #     for image_path in glob.glob(path):
    #         if output:
    #             output_dir = output
    #         else:
    #             output_dir = os.path.join(os.path.dirname(image_path), "output")

    #         if not os.path.exists(output_dir):
    #             os.makedirs(output_dir)

    #         mirror_image(image_path, output_dir)

if __name__ == "__main__":
    typer.run(main)
