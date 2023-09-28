import typer
import subprocess
from pathlib import Path

app = typer.Typer()

@app.command()
def install(clump: str):
    clump_path = Path(f"./clumps/{clump}")
    if not clump_path.joinpath("poetry.lock").exists():
        typer.echo(f"Installing dependencies for the {clump} clump.")
        subprocess.run(["poetry", "install"], cwd=clump_path)
    else:
        typer.echo(f"Dependencies for the {clump} clump are already installed.")

@app.command()
def run(clump: str, script: str, script_args: str = typer.Option(None, "--args", help="Arguments for the script")):
    clump_path = Path(f"./clumps/{clump}")
    if not clump_path.joinpath("poetry.lock").exists():
        typer.echo(f"Dependencies for clump '{clump}' are not installed. Run 'purr install {clump}' first.")
        raise typer.Exit(code=1)

    script_path = clump_path.joinpath(script, "entry.py")
    if script_path.exists():
        if script_args:
            args = ["python", str(script_path)] + script_args.split()
            subprocess.run(args)
        else:
            subprocess.run(["python", str(script_path)])
    else:
        typer.echo(f"Script '{script}' not found in clump '{clump}'")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
