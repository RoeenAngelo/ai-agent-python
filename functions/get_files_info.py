import os

def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)

    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    
    contents = os.listdir(target_dir)

    contents_string = []
    try:
        # Iterate over each item in the directory
        for content in contents:
            filepath = os.path.join(target_dir, content)
            
            # Determine if it's a directory
            is_dir = os.path.isdir(filepath)
            
            # Get the file size. For directories, size varies by OS, 
            # often representing the size of the directory entry itself.
            try:
                file_size = os.path.getsize(filepath)
            except OSError:
                file_size = 0 # Handle cases where size might be inaccessible

            # Format the output string for the item
            item_info = f"- {content}: file_size={file_size} bytes, is_dir={is_dir}"
            contents_string.append(item_info)
            
    except OSError as e:
        return f"Error accessing directory '{target_dir}': {e}"
    
    return "\n".join(contents_string)