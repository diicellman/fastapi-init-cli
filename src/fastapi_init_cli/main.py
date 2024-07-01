import os
import typer
from typing import Dict, Any

app = typer.Typer()


def create_structure(structure: Dict[str, Any], base_path: str = ""):
    for key, value in structure.items():
        path = os.path.join(base_path, key)
        if isinstance(value, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(value, path)
        elif isinstance(value, str):
            with open(path, "w") as f:
                f.write(value)
        elif isinstance(value, list):
            os.makedirs(path, exist_ok=True)
            for item in value:
                if isinstance(item, str):
                    with open(os.path.join(path, item), "w") as f:
                        f.write("")
                elif isinstance(item, dict):
                    for file_name, content in item.items():
                        with open(os.path.join(path, file_name), "w") as f:
                            f.write(content)


@app.command()
def init(name: str = typer.Option("fastapi_project", help="Name of the project")):
    """Initialize a new FastAPI project with example code"""
    project_structure = {
        name: {
            "app": {
                "api": {
                    "v1": {
                        "endpoints": [
                            {
                                "items.py": """from fastapi import APIRouter, HTTPException
from typing import List, Dict

router = APIRouter()

items = {}

@router.get("/items/", response_model=List[Dict[str, Any]])
async def read_items():
    return [{"id": k, **v} for k, v in items.items()]

@router.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

@router.post("/items/")
async def create_item(item: Dict[str, Any]):
    item_id = max(items.keys() or [0]) + 1
    items[item_id] = item
    return {"id": item_id, **item}
"""
                            },
                            "__init__.py",
                        ],
                    },
                    "__init__.py": "",
                },
                "core": {
                    "config.py": """from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "FastAPI Project"
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
""",
                    "__init__.py": "",
                },
                "db": {
                    "base.py": """from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
""",
                    "session.py": """from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
""",
                    "__init__.py": "",
                },
                "models": [
                    {
                        "item.py": """from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
"""
                    },
                    "__init__.py",
                ],
                "schemas": [
                    {
                        "item.py": """from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    description: str = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True
"""
                    },
                    "__init__.py",
                ],
                "main.py": """from fastapi import FastAPI
from app.api.v1.endpoints import items
from app.core.config import settings

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.include_router(items.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI!"}
""",
                "__init__.py": "",
            },
            "tests": [
                {
                    "test_main.py": """from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FastAPI!"}
"""
                },
                "__init__.py",
            ],
            "requirements.txt": """fastapi==0.68.0
uvicorn==0.15.0
sqlalchemy==1.4.23
pydantic==1.8.2
""",
            "README.md": f"""# {name}

This is a FastAPI project generated using the FastAPI CLI tool.

## Getting Started

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the server:
   ```
   uvicorn app.main:app --reload
   ```

3. Open your browser and go to http://localhost:8000/docs to see the API documentation.

## Project Structure

- `app/`: Main application package
  - `api/`: API endpoints
  - `core/`: Core functionality (config, etc.)
  - `db/`: Database-related code
  - `models/`: SQLAlchemy models
  - `schemas/`: Pydantic schemas
  - `main.py`: Main FastAPI application
- `tests/`: Test files

## Running Tests

To run tests, use the following command:

```
pytest
```
""",
        }
    }

    create_structure(project_structure)
    typer.echo(f"FastAPI project '{name}' created successfully with example code!")


if __name__ == "__main__":
    app()
