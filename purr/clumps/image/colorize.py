import typer
from rich import print
from PIL import Image, ImageColor, ImageOps, ImageChops
import os
import glob
import colorsys

app = typer.Typer(invoke_without_command=True)

def within_tolerance(color1, color2, tolerance):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    return abs(r1 - r2) <= tolerance and abs(g1 - g2) <= tolerance and abs(b1 - b2) <= tolerance

def colorize_image(image_path: str, color: str, output_dir: str, ignore_colors: list, tolerance: int):
    try:
        with Image.open(image_path) as image:
            grayscale = ImageOps.grayscale(image)
            colored = ImageOps.colorize(grayscale, color, "black")

            image = image.convert('RGB')
            colored = colored.convert('RGB')

            width, height = image.size
            for x in range(width):
                for y in range(height):
                    pixel_color = image.getpixel((x, y))
                    if any(within_tolerance(pixel_color, ImageColor.getcolor(ignore_color, "RGB"), tolerance) for ignore_color in ignore_colors):
                        colored.putpixel((x, y), pixel_color)

            new_path = os.path.join(output_dir, os.path.basename(image_path))
            colored.save(new_path)
            print(f'Successfully colorized {image_path} and saved to {new_path}')
    except Exception as e:
        print(f'Failed to colorize {image_path}: {e}')

@app.callback()
def colorize(
    files: str,
    color: str,
    ignore_colors: list = typer.Option(
        [],
        '--ignore', '-i',
        help='List of colors to ignore'
    ),
    tolerance: int = typer.Option(
        10,
        '--tolerance', '-t',
        help='Tolerance range for ignoring colors'
    ),
    output: str = typer.Option(
        None,
        '--output', '-o',
        help='Output directory for colorized images'
    )
):
    if output is None:
        output = os.path.join(os.path.dirname(files), 'colorized')
    if not os.path.exists(output):
        os.makedirs(output)

    file_paths = glob.glob(files) if '*' in files else files.split(',')

    for file_path in file_paths:
        if not file_path.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'tiff')):
            print(f'Warning: {file_path} is not a recognized image file format.')
            continue

        if color.startswith('#'):
            color = '#' + color.lstrip('#')
            rgb = ImageColor.getcolor(color, "RGB")
            color = f'rgb({rgb[0]},{rgb[1]},{rgb[2]})'

        colorize_image(file_path, color, output, ignore_colors, tolerance)

if __name__ == "__main__":
    app()
