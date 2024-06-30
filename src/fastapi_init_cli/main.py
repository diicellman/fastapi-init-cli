import os
import typer
from typing import Optional

app = typer.Typer()


def create_structure(structure, base_path=""):
    for key, value in structure.items():
        path = os.path.join(base_path, key)
        if isinstance(value, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(value, path)
        elif isinstance(value, list):
            os.makedirs(path, exist_ok=True)
            for item in value:
                open(os.path.join(path, item), "a").close()
        else:
            open(path, "a").close()


@app.command()
def init(
    name: Optional[str] = typer.Option("fastapi_project", help="Name of the project")
):
    """Initialize a new FastAPI project"""
    project_structure = {
        name: {
            "app": {
                "api": {
                    "v1": {
                        "endpoints": ["__init__.py"],
                    },
                    "__init__.py": "",
                },
                "core": {
                    "config.py": "",
                    "__init__.py": "",
                },
                "db": {
                    "base.py": "",
                    "session.py": "",
                    "__init__.py": "",
                },
                "models": ["__init__.py"],
                "schemas": ["__init__.py"],
                "main.py": "",
                "__init__.py": "",
            },
            "tests": ["__init__.py"],
            "requirements.txt": "",
            "README.md": "",
        }
    }

    create_structure(project_structure)
    typer.echo(f"FastAPI project '{name}' created successfully!")


if __name__ == "__main__":
    app()
