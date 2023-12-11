import os
import htmlmin
import typer

app = typer.Typer(invoke_without_command=True)


def combine_html_files(
    input_dir: str,
    output_dir: str = None,
    max_size: int = 80 * 1024 * 1024,
    buffer_size: int = 1024 * 1024,
):
    """
    Combines and minifies HTML files from a given directory into single files of a maximum size.

    Args:
        input_dir (str): Directory containing HTML files to be combined.
        output_dir (str): Directory where combined HTML files will be saved. Defaults to the current working directory.
        max_size (int): Maximum size in bytes of each combined HTML file. Defaults to 80MB.
        buffer_size (int): Buffer size in bytes for reading HTML files. Defaults to 1MB.
    """

    # Set default output directory to the current working directory if not specified
    if output_dir is None:
        output_dir = os.getcwd()

    current_file_size = 0
    current_file_num = 1
    os.makedirs(output_dir, exist_ok=True)

    # Initialize the first output file
    current_file_path = os.path.join(output_dir, f"combined_{current_file_num}.html")
    current_file = open(current_file_path, "w")

    for subdir, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(subdir, file)

                with open(file_path, "r") as f:
                    content = f.read()
                    minified_content = htmlmin.minify(content, remove_empty_space=True)
                    minified_size = len(minified_content.encode("utf-8"))

                    # If the addition of the new content exceeds max_size, create a new output file
                    if current_file_size + minified_size > max_size:
                        current_file.close()
                        current_file_num += 1
                        current_file_path = os.path.join(
                            output_dir, f"combined_{current_file_num}.html"
                        )
                        current_file = open(current_file_path, "w")
                        current_file_size = 0

                    current_file.write(minified_content)
                    current_file_size += minified_size

    # Close the last output file
    current_file.close()


@app.command()
def main(
    input_directory: str = typer.Argument(
        ..., help="The input directory containing HTML files to combine."
    ),
    output_directory: str = typer.Option(
        None, help="The output directory where the combined HTML file will be saved."
    ),
    max_file_size: int = typer.Option(
        80 * 1024 * 1024, help="Maximum size of each combined HTML file."
    ),
    buffer_size: int = typer.Option(
        1024 * 1024, help="Buffer size for reading HTML files."
    ),
):
    """
    Command-line interface to combine and minify HTML files.

    This script combines multiple HTML files into a single file, minifying them in the process.
    """
    combine_html_files(input_directory, output_directory, max_file_size, buffer_size)


if __name__ == "__main__":
    app()
