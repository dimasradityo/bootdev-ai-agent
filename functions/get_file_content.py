import os

import config
from functions.utils import is_valid_dir, return_absolute_path


def get_file_content(working_directory: str, file_path: str) -> str:
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

        # Raise error if file path is not a file
        if not os.path.isfile(file_path_abs):
            raise Exception(
                f'Error: File not found or is not a regular file: "{file_path}"'
            )

        # opening and reading up to max chars of the file
        with open(file_path_abs) as file:
            content = file.read(config.MAX_CHARS)
            # After reading the first MAX_CHARS...
            if file.read(1):
                content += f'[...File "{file_path_abs}" truncated at {config.MAX_CHARS} characters]'
            return content
    except Exception as e:
        return f"Error: {e}"
