import os

from functions.utils import is_valid_dir, return_absolute_path


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
            raise Exception(
                f'Error: Cannot write to "{file_path}" as it is a directory'
            )

        # Writing file
        with open(file_path_abs, mode="w") as file:
            file.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: {e}"
