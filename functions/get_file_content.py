"""Functions to get the contents of files on the disk."""

from pathlib import Path

MAX_CHARS = 10_000


def get_file_content(working_directory: str, file_path: str) -> str:
    """Return the contents of a file up to the first 10_000 characters.

    Args:
        working_directory: The location permitted to be searched.
        file_path: The path to the file in question.

    Returns:
        The contents of a file truncated to the first 10_000 characters.
    """
    working_dir_path = Path(working_directory).resolve()
    if not working_dir_path.exists() or not working_dir_path.is_dir():
        return f'Error: "{working_directory} is not a valid directory"'
    path = Path(file_path) if Path(file_path).is_absolute() else working_dir_path / file_path
    path = path.resolve()
    if not path.is_relative_to(working_dir_path):
        return f'Error: Cannot access "{file_path}" as it is outside the permitted working directory'
    if not path.exists() or not path.is_file():
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with path.open(mode="r", encoding="utf-8") as file:
            file_content_string = file.read(MAX_CHARS)

        if len(file_content_string) == MAX_CHARS:
            file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'
    except Exception as e:  # noqa: BLE001
        return f'Error reading file "{file_path}": {e}'
    else:
        return file_content_string
