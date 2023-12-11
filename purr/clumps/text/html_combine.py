import os
import htmlmin
import typer

app = typer.Typer(invoke_without_command=True)

def combine_html_files(
    input_dir: str,
    output_dir: str = None,
    max_size: int = 80 * 1024 * 1024,
    buffer_size: int = 1024 * 1024,
    minify: bool = False,
):
    """
    Combines HTML files from a given directory into single files of a maximum size, with an option to minify.

    Args:
        input_dir (str): Directory containing HTML files to be combined.
        output_dir (str): Directory where combined HTML files will be saved. Defaults to the current working directory.
        max_size (int): Maximum size in bytes of each combined HTML file. Defaults to 80MB.
        buffer_size (int): Buffer size in bytes for reading HTML files. Defaults to 1MB.
        minify (bool): Whether to minify HTML files. Defaults to False.
    """
    if output_dir is None:
        output_dir = os.getcwd()

    current_file_size = 0
    current_file_num = 1
    os.makedirs(output_dir, exist_ok=True)
    current_file_path = os.path.join(output_dir, f"combined_{current_file_num}.html")
    current_file = open(current_file_path, "w")

    for subdir, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(subdir, file)

                with open(file_path, "r") as f:
                    content = f.read()
                    if minify:
                        content = htmlmin.minify(content, remove_empty_space=True)
                    content_size = len(content.encode("utf-8"))

                    if current_file_size + content_size > max_size:
                        current_file.close()
                        current_file_num += 1
                        current_file_path = os.path.join(output_dir, f"combined_{current_file_num}.html")
                        current_file = open(current_file_path, "w")
                        current_file_size = 0

                    current_file.write(content)
                    current_file_size += content_size

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
    minify_html: bool = typer.Option(
        False, "--minify", help="Enable minification of HTML files."
    )
):
    """
    Command-line interface to combine HTML files.

    This script combines multiple HTML files into a single file, with an option to minify them in the process.
    """
    combine_html_files(input_directory, output_directory, max_file_size, buffer_size, minify_html)

if __name__ == "__main__":
    app()
