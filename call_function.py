import json
from collections.abc import Callable

from config import WORKING_DIR
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import schema_write_file, write_file

available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file,
]

# The tool_call argument is one of the tool-call objects from message.tool_calls. The three things we care about are:

# tool_call.function.name: the name of the function (a string)
# tool_call.function.arguments: the arguments, as a JSON string
# tool_call.id: a unique ID for this call (we'll need it when we send the result back)


def call_function(tool_call, verbose: bool = False) -> dict:
    # parsing the tool call output objects
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments or "{}")

    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    # determine which of the functions to call based on the tool call output
    function_map: dict[str, Callable[..., str]] = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    # Return error if tool called an unkown function
    if function_name not in function_map:
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": f"Error: Unknown function: {function_name}",
        }

    # Hard code working directory to prevent LLMs from working outside as intended
    function_args["working_directory"] = WORKING_DIR

    # Call the function and store output in variable
    result: str = function_map[function_name](**function_args)

    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result,
    }
