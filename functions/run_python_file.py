"""YOLO!"""

import subprocess  # noqa: S404
from pathlib import Path


def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    """Have an LLM run code on your machine!

    What could go wrong?

    Args:
        working_directory: The location permitted to be searched.
        file_path: The path to the file in question.
        args: Additional command line arguments to supply to the command.

    Returns:
        Results of executing the code, or any errors that may occur.
    """
    working_dir_path = Path(working_directory).resolve()
    if not working_dir_path.exists() or not working_dir_path.is_dir():
        return f'Error: "{working_directory} is not a valid directory"'
    path = Path(file_path) if Path(file_path).is_absolute() else working_dir_path / file_path
    path = path.resolve()
    if not path.is_relative_to(working_dir_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not path.exists():
        return f'Error: File "{file_path}" not found.'
    if not path.name.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    commands = ["python", path]
    if args:
        commands.extend(args)

    try:
        result = subprocess.run(commands, text=True, cwd=path.parent, timeout=30, capture_output=True)  # noqa: S603
    except Exception as e:  # noqa: BLE001
        return f"Error: executing Python file: {e}"
    else:
        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        return "\n".join(output) if output else "No output produced."
