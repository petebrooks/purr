from setuptools import setup, find_packages

setup(
    name="purr",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "typer>=0.4.0"
    ]
)
