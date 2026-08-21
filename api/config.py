import tomllib
from pathlib import Path

toml_content = (Path(__file__).parent / "pyproject.toml").read_text()
toml_content = tomllib.loads(toml_content)

APP = toml_content["project"]["name"]
VERSION = toml_content["project"]["version"]
