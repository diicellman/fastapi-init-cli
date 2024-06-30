from typer.testing import CliRunner
from fastapi_init_cli.main import app

runner = CliRunner()


def test_init_command():
    result = runner.invoke(app, ["init", "--name", "test_project"])
    assert result.exit_code == 0
    assert "FastAPI project 'test_project' created successfully!" in result.stdout
