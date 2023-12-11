import os
import htmlmin
import typer
from concurrent.futures import ProcessPoolExecutor
from markdownify import markdownify as md
from bs4 import BeautifulSoup
from tqdm import tqdm

app = typer.Typer(invoke_without_command=True)


def convert_html_to_markdown(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.find("body") or html_content
    return md(str(body_content))


def process_file(file_path: str, minify: bool, markdown: bool) -> str:
    with open(file_path, "r") as file:
        content = file.read()
        if minify:
            content = htmlmin.minify(content, remove_empty_space=True)
        if markdown:
            content = convert_html_to_markdown(content)
        return content


def combine_files(
    input_dir: str,
    output_dir: str,
    max_size: int,
    buffer_size: int,
    minify: bool,
    markdown: bool,
):
    output_dir = output_dir or os.getcwd()
    os.makedirs(output_dir, exist_ok=True)

    file_extension = "md" if markdown else "html"
    combined_file_path = os.path.join(output_dir, f"combined_1.{file_extension}")
    combined_file = open(combined_file_path, "w")
    current_file_size = 0
    current_file_num = 1

    file_paths = [
        (os.path.join(subdir, file), minify, markdown)
        for subdir, _, files in os.walk(input_dir)
        for file in files
        if file.endswith(".html")
    ]

    with ProcessPoolExecutor() as executor, tqdm(
        total=len(file_paths), desc="Processing Files", unit="file"
    ) as progress:
        futures = [
            executor.submit(process_file, *file_info) for file_info in file_paths
        ]

        for future in futures:
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
            progress.update(1)

    combined_file.close()


@app.callback()
def html_combine(
    input_directory: str = typer.Argument(..., help="Input directory with HTML files."),
    output_directory: str = typer.Option(
        None, help="Output directory for combined files."
    ),
    max_file_size: int = typer.Option(
        80 * 1024 * 1024, help="Maximum size of combined files."
    ),
    buffer_size: int = typer.Option(1024 * 1024, help="Buffer size for reading files."),
    minify_html: bool = typer.Option(False, "--minify", help="Minify HTML files."),
    markdown: bool = typer.Option(
        False, "--markdown", "--md", help="Convert HTML to Markdown."
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
        markdown,
    )


if __name__ == "__main__":
    app()
