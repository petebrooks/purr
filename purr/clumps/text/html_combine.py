import os
import htmlmin
import typer
from concurrent.futures import ProcessPoolExecutor
from markdownify import markdownify as md
from bs4 import BeautifulSoup

app = typer.Typer(invoke_without_command=True)


def convert_html_to_markdown(html_content: str) -> str:
    """
    Converts HTML content to Markdown.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.find("body") or html_content
    return md(str(body_content))


def process_file(file_path: str, minify: bool, convert_to_markdown: bool) -> str:
    """
    Processes an individual HTML file - reads, optionally minifies and/or converts to Markdown.
    """
    with open(file_path, "r") as file:
        content = file.read()
        if minify:
            content = htmlmin.minify(content, remove_empty_space=True)
        if convert_to_markdown:
            content = convert_html_to_markdown(content)
        return content


def combine_files(
    input_dir: str,
    output_dir: str,
    max_size: int,
    buffer_size: int,
    minify: bool,
    convert_to_markdown: bool,
):
    """
    Combines HTML files from a directory into single files of a maximum size, with options to minify and/or convert to Markdown.
    """
    output_dir = output_dir or os.getcwd()
    os.makedirs(output_dir, exist_ok=True)

    file_extension = "md" if convert_to_markdown else "html"
    combined_file_path = os.path.join(output_dir, f"combined_1.{file_extension}")
    combined_file = open(combined_file_path, "w")
    current_file_size = 0
    current_file_num = 1

    with ProcessPoolExecutor() as executor:
        future_to_file = {
            executor.submit(
                process_file, os.path.join(subdir, file), minify, convert_to_markdown
            ): file
            for subdir, _, files in os.walk(input_dir)
            for file in files
            if file.endswith(".html")
        }

        for future in future_to_file:
            content = future.result()
            content_size = len(content.encode("utf-8"))

            if current_file_size + content_size > max_size:
                combined_file.close()
                current_file_num += 1
                combined_file_path = os.path.join(
                    output_dir, f"combined_{current_file_num}.{file_extension}"
                )
                combined_file = open(combined_file_path, "w")
                current_file_size = 0

            combined_file.write(content)
            current_file_size += content_size

    combined_file.close()


@app.command()
def main(
    input_directory: str = typer.Argument(..., help="Input directory with HTML files."),
    output_directory: str = typer.Option(
        None, help="Output directory for combined files."
    ),
    max_file_size: int = typer.Option(
        80 * 1024 * 1024, help="Maximum size of combined files."
    ),
    buffer_size: int = typer.Option(1024 * 1024, help="Buffer size for reading files."),
    minify_html: bool = typer.Option(False, "--minify", help="Minify HTML files."),
    convert_to_markdown: bool = typer.Option(
        False, "--convert-md", help="Convert HTML to Markdown."
    ),
):
    """
    Command-line interface to combine, optionally minify, and/or convert HTML files to Markdown.
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
