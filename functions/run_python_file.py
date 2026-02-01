import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
    valid_abs_file_path = os.path.commonpath([abs_working_dir, abs_file_path]) == abs_working_dir
    
    if not valid_abs_file_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    
    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    
    command = ["python", abs_file_path]
    if args:
            command.extend(args)
    
    try:
        completed_process = subprocess.run(
            command, 
            cwd=abs_working_dir, 
            capture_output=True, 
            timeout=30, 
            text=True
            )
        
        output = []
        if not completed_process.stdout and not completed_process.stderr:
            output.append("No output produced")
        if completed_process.returncode != 0:
            output.append(f"Process exited with code {completed_process.returncode}")
        if completed_process.stdout:
            output.append(f"STDOUT:\n{completed_process.stdout}")
        if completed_process.stderr:
            output.append(f"STDERR:\n{completed_process.stderr}")
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    return "\n".join(output)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a Python file within the working directory and return its output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of string arguments to pass to the Python script",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    ),
)
