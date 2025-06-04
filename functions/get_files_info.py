"""Functions to allow the LLM to query the disk for file information."""

from pathlib import Path


def get_files_info(working_directory: str, directory: str | None = None) -> str:
    """List the contents of a directory and see the file's metadata.

    Args:
        working_directory: The location where the files are stored.
        directory: The directory to list the file contents of. This must be
            located within the working directory.

    Returns:
        A string that represents the contents of the directory.
    """
    working_dir_path = Path(working_directory).resolve()
    if not working_dir_path.exists() or not working_dir_path.is_dir():
        return f'Error: "{working_directory} is not a valid directory"'
    if not directory:
        directory = "."
    dir_path = working_dir_path / directory
    dir_path = dir_path.resolve()
    if not dir_path.is_relative_to(working_dir_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not dir_path.is_dir():
        return f'Error: "{directory}" is not a directory'

    contents = ""
    for child in dir_path.iterdir():
        is_dir = child.is_dir()
        file_size = child.stat().st_size
        if is_dir:
            file_size = 0
        contents += f"- {child.name}: file_size={file_size} bytes, is_dir={is_dir}\n"

    return contents
