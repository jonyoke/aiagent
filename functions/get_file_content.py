import os

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    rel_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(rel_path)
    print(abs_path)


    if not os.path.abspath(working_directory) in abs_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    

    try:
        with open(abs_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
    except Exception as e:
        return f'Error: Could not read file because - {e}'
    
    if len(file_content_string) == MAX_CHARS:
        print('file was truncated')
        file_content_string += f'...File "{file_path}" truncated at {MAX_CHARS} characters'

    return file_content_string