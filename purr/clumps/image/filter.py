import typer
import glob
from PIL import Image, UnidentifiedImageError
from rich import print
from typing import List

app = typer.Typer(invoke_without_command=True)

def check_square(image_path: str) -> bool:
    try:
        with Image.open(image_path) as image:
            return image.width == image.height, True
    except UnidentifiedImageError:
        return False, False

@app.callback()
def filter_images(
    paths: List[str],
    square: bool = typer.Option(False, "--square", "-s", help="Return only square images"),
    nonsquare: bool = typer.Option(False, "--nonsquare", "-n", help="Return only non-square images")
):
    """
    Filter image files by square/non-square based on the given options.
    """
    if square and nonsquare:
        print("[bold red]Error:[/bold red] Both --square and --nonsquare options cannot be present together.")
        raise typer.Exit(code=1)

    filtered_images = []
    for path in paths:
        for image_path in glob.glob(path):
            is_square, is_image = check_square(image_path)
            if is_image and ((square and is_square) or (nonsquare and not is_square)):
                filtered_images.append(image_path)

    print(' '.join(filtered_images))

if __name__ == "__main__":
    app()
