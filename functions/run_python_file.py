import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    rel_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(rel_path)
    print(f'Attempting to run {abs_path}')

    if not os.path.abspath(working_directory) in abs_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_path):
        return f'Error: File "{file_path}" not found.'
    
    if not abs_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        command = ["python3", abs_path] + args
        comp_process = subprocess.run(command,cwd=working_directory,capture_output=True,text=True,timeout=30)
        
        output_str = f"STDOUT: {comp_process.stdout}\nSTDERR: {comp_process.stderr}"
        if comp_process.stdout == None and comp_process.stderr == None:
            output_str = "No output produced."
        if comp_process.returncode != 0:
            output_str += f"Process exited with code {comp_process.returncode}"
        return output_str
    except Exception as e:
        f"Error: executing Python file: {e}"
        