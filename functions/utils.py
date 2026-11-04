import os


def return_absolute_path(working_dir: str, target: str) -> tuple[str, str]:
    # working dir absolute path
    working_dir_abs = os.path.abspath(working_dir)

    # target absolute filepath
    file_path_abs = os.path.normpath(os.path.join(working_dir_abs, target))

    return working_dir_abs, file_path_abs


def is_valid_dir(working_dir: str, target: str) -> bool:
    # check if file path is valid input
    if not isinstance(target, str) or len(target) == 0:
        raise Exception(f'Error: "{target}" is not a directory')

    # check if file path dir falls within absolute working directory path
    return os.path.commonpath([working_dir, target]) == working_dir
