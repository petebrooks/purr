import glob
import os
import send2trash
from PIL import Image
import typer
from rich.table import Table
from typing import List

app = typer.Typer(invoke_without_command=True)

@app.callback()
def main(
    image_paths: List[str],
    output_dir: str = "split",
    delete: bool = False,
    min_width: int = typer.Option(None, "--min-width", "-mw", help="Minimum width of image to process"),
    allow_non_square: bool = typer.Option(False, "--allow-non-square", "-ns", help="Allow non-square images to be processed"),
):
    """
    Split the image into four equal quadrants and save them as separate images.
    """
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Status", style="dim", width=12)
    table.add_column("Message", justify="left")

    image_files = []
    for image_path in image_paths:
        if '*' in image_path or '?' in image_path:
            image_files.extend(glob.glob(image_path))
        else:
            image_files.append(image_path)

    for image_file in image_files:
        if not os.path.isfile(image_file):
            table.add_row("[bold red]Error", f"Invalid image file: {image_file}")
            continue

        with Image.open(image_file) as image:
            if min_width is not None and image.width < min_width:
                table.add_row("[bold yellow]Skipped", f"{image_file} (width {image.width} < min width {min_width})")
                continue

            if not allow_non_square and image.width != image.height:
                table.add_row("[bold yellow]Skipped", f"{image_file} (is not square)")
                continue

            image_format = image.format
            output_format = image_format.lower()
            base_name = os.path.splitext(os.path.basename(image_file))[0]
            existing_files = glob.glob(os.path.join(output_dir, f'{base_name}.*.{output_format}'))

            if existing_files:
                table.add_row("[bold yellow]Skipped", f'Split images already exist for {image_file}. Skipping...')
                continue

            # Get the width and height of the image
            width, height = image.size

            # Calculate the quadrant dimensions
            quadrant_width = width // 2
            quadrant_height = height // 2

            # Split the image into four quadrants
            top_left = image.crop((0, 0, quadrant_width, quadrant_height))
            top_right = image.crop((quadrant_width, 0, width, quadrant_height))
            bottom_left = image.crop((0, quadrant_height, quadrant_width, height))
            bottom_right = image.crop((quadrant_width, quadrant_height, width, height))

            # Create the output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)

            # Save the split images with the input image format
            top_left.save(os.path.join(output_dir, f'{base_name}.top_left.{output_format}'), format=image_format)
            top_right.save(os.path.join(output_dir, f'{base_name}.top_right.{output_format}'), format=image_format)
            bottom_left.save(os.path.join(output_dir, f'{base_name}.bottom_left.{output_format}'), format=image_format)
            bottom_right.save(os.path.join(output_dir, f'{base_name}.bottom_right.{output_format}'), format=image_format)

            table.add_row("[bold green]Success", f"Split {image_file}")

            # Delete the original image file
            if delete:
                table.add_row("[bold lavender]Deleted", f"Moving {image_file} to recycle bin")
                send2trash.send2trash(image_file)

if __name__ == "__main__":
    app()
