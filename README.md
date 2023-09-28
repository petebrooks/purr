# Purr

## Installation

### Prerequisites

- Python 3.7 or higher

### Using Poetry

4. Install dependencies using Poetry.
```bash
poetry install
```

### Add to PATH

Make sure to add the `purr` executable to your system's PATH, or you can use it directly from the repository folder.

## Usage

The general syntax to run a script is:

```bash
purr <clump> <script> [script_args]
```

### Examples

```bash
# Run the 'mirror' script from the 'image' clump with sample.jpg and --east flag
purr image mirror sample.jpg --east
```

### Discovering Clumps and Scripts

The CLI will automatically discover "clumps" (collections of scripts) and individual scripts based on the folder structure under the `./clumps/` directory.

## Development Notes

### Running the App in Development

1. Open a terminal and navigate to the project directory.
2. Activate the Poetry environment.
    ```bash
    poetry shell
    ```
3. Run the application.
    ```bash
    python main.py [arguments]
    ```

### Dependency Management

Dependencies are managed via Poetry. To add a new dependency:

```bash
poetry add <package_name>
```

### Script and Clump Dependencies

If a script or a clump has specific dependencies, consider creating a separate `pyproject.toml` under that clump or script folder for better dependency isolation.

## How to Add New Scripts

1. Create a new folder under the appropriate "clump" inside `./clumps/`.
2. Add an `entry.py` file, which will serve as the entry point for your script.
3. Implement your script in `entry.py`.

### Example folder structure:

```
- clumps/
  - image/
    - mirror/
      - entry.py
```

### Example `entry.py`:

```python
import typer

def main(image_path: str, east: bool = typer.Option(False, '--east')):
    # Your script logic here

if __name__ == '__main__':
    typer.run(main)
```
