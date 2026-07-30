import os
from config import MAX_CHAR_READING

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_path_working = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path_working, file_path))
        valid_target_file = os.path.commonpath([abs_path_working, target_file]) == abs_path_working

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file "{file_path}"'

        with open(target_file, 'r') as f:
            content = f.read(MAX_CHAR_READING)
            if f.read(1):
                content += f'[...File "{target_file}" truncated at {MAX_CHAR_READING} characters]'
        return content


    except Exception as e:
        return f'Error: {e}'