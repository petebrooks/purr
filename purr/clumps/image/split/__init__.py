import glob
import os
import send2trash
from PIL import Image
import typer
from rich.table import Table
from rich.console import Console
from typing import List

app = typer.Typer(invoke_without_command=True)

def get_image_files(image_paths: List[str]) -> List[str]:
    image_files = []
    for image_path in image_paths:
        if '*' in image_path or '?' in image_path:
            image_files.extend(glob.glob(image_path))
        else:
            image_files.append(image_path)
    return image_files

def determine_output_dir(image_file: str, output_dir: str) -> str:
    if not os.path.isabs(output_dir):
        if output_dir.startswith("./"):
            output_dir = os.path.join(os.getcwd(), output_dir[2:])
        else:
            output_dir = os.path.join(os.path.dirname(image_file), output_dir)
    return output_dir

def is_blank(image: Image.Image) -> bool:
    extrema = image.convert("RGBA").getextrema()
    return all([e[0] == e[1] for e in extrema])

@app.callback()
def main(
    image_paths: List[str],
    output_dir: str = typer.Option(
        "split",
        "--output", "-o",
        help=(
            "Specify the output directory. "
            "By default, it creates a 'split' directory under the same directory as the input image. "
            "For a relative path, it will be relative to the image file's directory unless prefixed with './', "
            "in which case it will be relative to the current working directory. "
            "Absolute paths are also accepted."
        )
    ),
    delete: bool = typer.Option(
        False,
        "--delete",
        "-D",
        help="Delete the original image file after splitting it."
    ),
    delete_blank: bool = typer.Option(
        False,
        "--delete-blank",
        "-d",
        help="Delete any output split image files that are a solid color or completely transparent."
    ),
    min_width: int = typer.Option(None, "--min-width", "-mw", help="Minimum width of image to process"),
    rows: int = typer.Option(1, "--rows", "-r", help="Number of rows to split the image into"),
    columns: int = typer.Option(1, "--columns", "-c", help="Number of columns to split the image into"),
):
    """
    Split the image into specified rows and columns and save them as separate images.
    """
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Status", style="dim", width=12)
    table.add_column("Message", justify="left")

    console = Console()

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

        output_dir = determine_output_dir(image_file, output_dir)

        with Image.open(image_file) as image:
            if min_width is not None and image.width < min_width:
                table.add_row("[bold yellow]Skipped", f"{image_file} (width {image.width} < min width {min_width})")
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

            # Calculate the dimensions of each cell
            cell_width = width // columns
            cell_height = height // rows

            # Create the output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)

            split_images_paths = []
            for i in range(rows):
                for j in range(columns):
                    # Crop the image according to the cell dimensions
                    left = j * cell_width
                    upper = i * cell_height
                    right = left + cell_width
                    lower = upper + cell_height
                    cell = image.crop((left, upper, right, lower))

                    # Save the split images with the input image format
                    output_path = os.path.join(output_dir, f'{base_name}.{i}_{j}.{output_format}')
                    cell.save(output_path, format=image_format)
                    split_images_paths.append(output_path)

            table.add_row("[bold green]Success", f"Split {image_file}")


            if delete_blank:
                for split_image_path in split_images_paths:
                    with Image.open(split_image_path) as split_image:
                        if is_blank(split_image):
                            os.remove(split_image_path)
                            table.add_row("[bold lavender]Deleted", f"Blank image: {split_image_path}")

            # Delete the original image file
            if delete:
                table.add_row("[bold lavender]Deleted", f"Moving {image_file} to recycle bin")
                send2trash.send2trash(image_file)

    console.print(table)

if __name__ == "__main__":
    app()
