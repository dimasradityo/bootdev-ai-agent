import os

from functions.utils import is_valid_dir, return_absolute_path


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        # get absolute paths for working dir and target
        working_dir_abs, target_dir_abs = return_absolute_path(
            working_directory, directory
        )

        # check if target is valid directory
        if not is_valid_dir(working_dir_abs, target_dir_abs):
            raise Exception(
                f'Cannot list "{directory}" as it is outside the permitted working directory'
            )

        # iterating and returning details of target dir
        file_info: list[str] = []
        for filename in os.listdir(target_dir_abs):
            filepath = os.path.join(target_dir_abs, filename)
            is_dir = os.path.isdir(filepath)
            file_size = os.path.getsize(filepath)
            file_info.append(
                f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}"
            )
        return "\n".join(file_info)
    except Exception as e:
        return f"Error: listing files: {e}"
