import os
import subprocess
from os.path import isfile

from functions.utils import is_valid_dir, return_absolute_path


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        # get absolute paths for working dir and target
        working_dir_abs, file_path_abs = return_absolute_path(
            working_directory, file_path
        )

        # check if target is valid directory
        if not is_valid_dir(working_dir_abs, file_path_abs):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # check if target is a file and not a dir
        if not os.path.isfile(file_path_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # check if target is a python file
        if not file_path_abs.split(".")[1] == "py":
            return f'Error: "{file_path}" is not a Python file'

        # Preparing command args
        command = ["python", file_path_abs]
        command.extend(args) if args else command

        # Running the subproces
        run_output = subprocess.run(command, capture_output=True, timeout=30, text=True)
        return_code = run_output.returncode
        output_string: list[str] = []

        if return_code != 0:
            output_string.append(f"Process exited with code {return_code}")
        if not run_output.stdout and not run_output.stderr:
            output_string.append(f"No output produced")
        if run_output.stdout:
            output_string.append(f"STDOUT:\n{run_output.stdout}")
        if run_output.stderr:
            output_string.append(f"STDERR:\n{run_output.stderr}")
        return "\n".join(output_string)
    except Exception as e:
        raise Exception(f"Error: executing Python file: {e}")
