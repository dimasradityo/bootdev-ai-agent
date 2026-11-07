import os

from functions.utils import is_valid_dir, return_absolute_path

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes content to a file relative to the working directory, creating the file and any parent directories if they don't exist, and overwriting it if it does",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to write, relative to the working directory.",
                },
                "content": {
                    "type": "string",
                    "description": "Content to be written to the file and replaces any existing content",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        # get absolute paths for working dir and target
        working_dir_abs, file_path_abs = return_absolute_path(
            working_directory, file_path
        )

        # check if target is valid directory
        if not is_valid_dir(working_dir_abs, file_path_abs):
            raise Exception(
                f'Cannot list "{file_path}" as it is outside the permitted working directory'
            )

        # Creating parent dir if not exists
        os.makedirs(os.path.dirname(file_path_abs), exist_ok=True)

        # Raise error if file path is not a file
        if os.path.isdir(file_path_abs):
            raise Exception(f'Cannot write to "{file_path}" as it is a directory')

        # Writing file
        with open(file_path_abs, mode="w") as file:
            file.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: {e}"
