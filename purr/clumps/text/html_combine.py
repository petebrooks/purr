import os
import sys
import htmlmin


def combine_html_files(input_dir, output_dir=None, max_size=80 * 1024 * 1024):
    if output_dir is None:
        output_dir = os.getcwd()

    current_file_size = 0
    current_file_num = 1
    os.makedirs(output_dir, exist_ok=True)
    current_file = open(
        os.path.join(output_dir, f"combined_{current_file_num}.html"), "w"
    )

    for subdir, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(subdir, file)

                with open(file_path, "r") as f:
                    content = f.read()
                    minified_content = htmlmin.minify(content, remove_empty_space=True)

                    # Check the size after minification
                    minified_size = len(minified_content.encode("utf-8"))

                    # Check and create a new file if size exceeds max_size
                    if current_file_size + minified_size > max_size:
                        current_file.close()
                        current_file_num += 1
                        current_file = open(
                            os.path.join(
                                output_dir, f"combined_{current_file_num}.html"
                            ),
                            "w",
                        )
                        current_file_size = 0

                    current_file.write(minified_content)
                    current_file_size += minified_size

    current_file.close()


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(
            "Usage: python combine_html.py <input-directory-path> [output-directory-path]"
        )
    else:
        output_dir = sys.argv[2] if len(sys.argv) == 3 else None
        combine_html_files(sys.argv[1], output_dir)
