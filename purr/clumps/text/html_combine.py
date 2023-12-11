import os
import htmlmin
import typer
from markdownify import markdownify as md
from bs4 import BeautifulSoup

app = typer.Typer(invoke_without_command=True)


def html_to_markdown(html_content: str) -> str:
    """
    Converts HTML content to Markdown format.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    body = soup.find("body")
    if body:
        return md(str(body))
    return md(html_content)


def combine_files(
    input_dir: str,
    output_dir: str = None,
    max_size: int = 80 * 1024 * 1024,
    buffer_size: int = 1024 * 1024,
    minify: bool = False,
    convert_to_md: bool = False,
):
    """
    Combines files from a given directory into single files of a maximum size, with options to minify and convert to Markdown.
    """
    if output_dir is None:
        output_dir = os.getcwd()

    current_file_size = 0
    current_file_num = 1
    os.makedirs(output_dir, exist_ok=True)
    current_file_path = os.path.join(
        output_dir, f"combined_{current_file_num}.{'md' if convert_to_md else 'html'}"
    )
    current_file = open(current_file_path, "w")

    for subdir, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(subdir, file)

                with open(file_path, "r") as f:
                    content = f.read()
                    if minify:
                        content = htmlmin.minify(content, remove_empty_space=True)
                    if convert_to_md:
                        content = html_to_markdown(content)
                    content_size = len(content.encode("utf-8"))

                    if current_file_size + content_size > max_size:
                        current_file.close()
                        current_file_num += 1
                        current_file_path = os.path.join(
                            output_dir,
                            f"combined_{current_file_num}.{'md' if convert_to_md else 'html'}",
                        )
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
        None, help="The output directory where the combined file will be saved."
    ),
    max_file_size: int = typer.Option(
        80 * 1024 * 1024, help="Maximum size of each combined file."
    ),
    buffer_size: int = typer.Option(1024 * 1024, help="Buffer size for reading files."),
    minify_html: bool = typer.Option(
        False, "--minify", help="Enable minification of HTML files."
    ),
    convert_to_markdown: bool = typer.Option(
        False, "--convert-md", help="Convert HTML files to Markdown format."
    ),
):
    """
    Command-line interface to combine HTML files, with options to minify and convert to Markdown.
    """
    combine_files(
        input_directory,
        output_directory,
        max_file_size,
        buffer_size,
        minify_html,
        convert_to_markdown,
    )


if __name__ == "__main__":
    app()
