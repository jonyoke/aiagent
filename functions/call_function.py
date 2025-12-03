#import os
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file

WORKING_DIRECTORY = "./calculator"

def call_function(function_call_part, verbose=False):
    #What are we doing?
    if verbose: print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else: print(f" - Calling function: {function_call_part.name}")

    args = function_call_part.args
    args["working_directory"] = WORKING_DIRECTORY
    function_result = "ERROR NO FUNCTION WAS CALLED, FAILURE IN call_function"

    match function_call_part.name:
        case "get_files_info":
            function_result = get_files_info(**args)
        case "get_file_content":
            function_result = get_file_content(**args)
        case "run_python_file":
            function_result = run_python_file(**args)
        case "write_file":
            function_result = write_file(**args)
        case _:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"error": f"Unknown function: {function_call_part.name}"},
                    )
                ],
            )
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )














schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the current working directory itself.",
            ),
        },
    ),
)

schema_get_file_content  = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the contents of the specified file (up to 10000 characters), constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file to read contents from, relative to the working directory.",
            ),
        },
        required=["file_path"]
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the specified python file, with the specified arguments, constrained to the working directory. If no arguments are given, do not pass any arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the python file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="A list of strings which are arguments that will be passed to the python file you are running. If not provided will default to an empty list, and not pass any arguments to the python file.",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="A single argument string to pass as an argument to the Python file.",
                ),
            ),
        },
        required=["file_path"],
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write a string of contents to the specified file, constrained to the working directory. This will overwrite an existing file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file to write contents to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The string of contents to write.",
            ),
        },
        required=["file_path", "content"]
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)