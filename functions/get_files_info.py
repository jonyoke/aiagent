import os

def get_files_info(working_directory, directory="."):
    rel_path = os.path.join(working_directory, directory)
    abs_path = os.path.abspath(rel_path)
    print(abs_path)

    if not os.path.abspath(working_directory) in abs_path:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(abs_path):
        return f'Error: "{directory}" is not a directory'
    

    result = "Result for current directory:\n"
    print(os.listdir(abs_path))
    for item in os.listdir(abs_path):
        item_rel_path = os.path.join(rel_path, item)
        result += f"{item}: files_size={os.path.getsize(item_rel_path)}bytes, is_dir={os.path.isdir(item_rel_path)}\n"

    return result
