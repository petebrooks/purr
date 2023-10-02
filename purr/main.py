import typer
import importlib
from pathlib import Path

app = typer.Typer()

# def discover_clumps():
#     clump_dir = Path('./purr/clumps/')
#     return [item.name for item in clump_dir.iterdir() if item.is_dir() and not item.name.startswith('__')]

# def discover_scripts(clump):
#     clump_path = Path(f'./purr/clumps/{clump}')
#     return [item.name for item in clump_path.iterdir() if item.is_dir() and not item.name.startswith('__')]

# def import_script(clump, script):
#     module_path = f"clumps.{clump}.{script}.entry"
#     # import module with name = script
#     module = importlib.import_module(module_path)

#     return getattr(module, "main", None)

# def create_command(clump, script):
#     script_main = import_script(clump, script)
#     if script_main:
#         cmd = typer.Command(script_main, name=script)
#         return cmd
#     return None

import clumps.image.mirror.entry as mirror
import clumps.image.split as split
image_app = typer.Typer(name="image")
image_app.add_typer(mirror.app, name="mirror")
image_app.add_typer(split.app, name="split")
app.add_typer(image_app)

if __name__ == "__main__":
    app()
