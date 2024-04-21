from pathlib import Path

def resource_path(*args) -> Path:
    return Path.cwd().joinpath(*args)