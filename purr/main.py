import typer
import subprocess
from pathlib import Path
from typing import List

app = typer.Typer()

# @app.command()
# def install(clump: str):
#     clump_path = Path(f"./clumps/{clump}")
#     if not clump_path.joinpath("poetry.lock").exists():
#         typer.echo(f"Installing dependencies for the {clump} clump.")
#         subprocess.run(["poetry", "install"], cwd=clump_path)
#     else:
#         typer.echo(f"Dependencies for the {clump} clump are already installed.")

def run_clump_script(clump: str, script: str, script_args: List[str]):
    clump_path = Path(f'./purr/clumps/{clump}')
    script_path = clump_path.joinpath(script, 'entry.py')

    print(script_args)
    if '--help' in script_args:
        # Run the script with '--help' to capture its auto-generated help messages
        result = subprocess.run(['python', str(script_path), '--help'], capture_output=True, text=True)
        typer.echo(result.stdout)
        return
    if script_path.exists():
        args = ['python', str(script_path)] + script_args
        subprocess.run(args)
    else:
        typer.echo(f'Script "{script}" not found in clump "{clump}"')
        raise typer.Exit(code=1)

def create_dynamic_command(clump_app, script, clump):
    @clump_app.command(name=script)
    def dynamic_command(args_list: List[str]):
        """
        Execute the script with the following arguments.
        """
        run_clump_script(clump, script, args_list)

def discover_clumps():
    clump_dir = Path('./purr/clumps/')
    return [item.name for item in clump_dir.iterdir() if item.is_dir()]

def discover_scripts(clump):
    clump_path = Path(f'./purr/clumps/{clump}')
    return [item.name for item in clump_path.iterdir() if item.is_dir()]

for clump in discover_clumps():
    clump_app = typer.Typer(name=clump)
    app.add_typer(clump_app, name=clump)

    for script in discover_scripts(clump):
        create_dynamic_command(clump_app, script, clump)

if __name__ == '__main__':
    app()


