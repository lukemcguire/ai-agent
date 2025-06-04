"""Writing files from an LLM. You're crazy."""

from pathlib import Path


def write_file(working_directory: str, file_path: str, content: str) -> str:
    """Write content to a file on disk.

    Args:
        working_directory: The location permitted to be accessed.
        file_path: The path to the file to be written.
        content: The new file contents

    Returns:
        The number of characters written to the file or an error message if
        unable to write to file.
    """
    working_dir_path = Path(working_directory).resolve()
    if not working_dir_path.exists() or not working_dir_path.is_dir():
        return f'Error: "{working_directory} is not a valid directory"'
    path = Path(file_path) if Path(file_path).is_absolute() else working_dir_path / file_path
    path = path.resolve()
    if not path.is_relative_to(working_dir_path):
        return f'Error: Cannot access "{file_path}" as it is outside the permitted working directory'
    if path.is_dir():
        return f'Error: "{file_path}" is a directory, not a file'
    # create any missing directories
    path.parent.mkdir(parents=True, exist_ok=True)
    # write file
    try:
        with path.open(mode="wt", encoding="utf-8") as file:
            file.write(content)
    except Exception as e:  # noqa: BLE001
        return f'Error writing to file "{file_path}": {e}'
    else:
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
