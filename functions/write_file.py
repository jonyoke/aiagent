import os

def write_file(working_directory, file_path, content):
    rel_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(rel_path)
    print(abs_path)

    if not os.path.abspath(working_directory) in abs_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'


    try:
        with open(abs_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f'Error: Could not write to {file_path} because - {e}'
    
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    