from typer import Typer, Argument
import importlib

app = Typer()

@app.command()
def run(clump: str = Argument(..., help="The clump to use"), script: str = Argument(..., help="The script to run within the clump")):
    module_path = f"purr.clumps.{clump}.{script}.entry"
    try:
        entry_module = importlib.import_module(module_path)
        entry_module.run()
    except ImportError:
        print(f"Invalid clump '{clump}' or script '{script}'. Please choose from existing ones.")

if __name__ == "__main__":
    app()
