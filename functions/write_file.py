import os
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
    valid_abs_file_path = os.path.commonpath([abs_working_dir, abs_file_path]) == abs_working_dir
    
    if not valid_abs_file_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if os.path.isdir(abs_file_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    try:    
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)

        with open(abs_file_path, "w", encoding="utf-8") as f:
            f.write(content)
    except OSError as e:
            return f'Error: writing file "{file_path}": {e}'
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write text content to a file within the working directory, creating parent directories if needed",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Path to the file to write, relative to the working directory. "
                    "Parent directories will be created if they do not exist."
                ),
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text content to write to the file (overwrites existing content)",
            ),
        },
        required=["file_path", "content"],
    ),
)