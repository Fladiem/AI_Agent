import os
import sys
from google import genai
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    if not isinstance(working_directory,str) or not isinstance(directory,str):
        print('Error: get_files_info.py only works with string values as arguments. Try "."')
        sys.exit(1) 
    directory_path = os.path.join(working_directory, directory)
    #print(os.path.abspath(working_directory))
    #print(os.path.abspath(directory_path))
    string_out = []
    if directory == ".":
        string_out.append('Result for current directory:\n') 
    else:
        string_out.append(f'Result for "{directory_path}":\n') #### setup if: '.' use working_dir name, else use dir_path

    if not os.path.abspath(directory_path).startswith(os.path.abspath(working_directory)):
        print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        #raise SystemExit(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    
    if os.path.isdir(directory_path) == True:
        for file in os.listdir(directory_path):
            file_path = f'{directory_path}/{file}'
            file_size = os.path.getsize(file_path)
            string_out.append(f'- {file}: file_size={file_size} bytes, is_dir={os.path.isdir(file_path)}\n')
            
        string_out = ''.join(string_out)
        print(string_out.strip('\n'))
        #print(str(string_out).startswith("Result for"))
    else:
        print(f'Error: "{directory_path}" is not a directory')
        return f'Error: "{directory_path}" is not a directory'
        #raise SystemExit(f'Error: "{directory_path}" is not a directory')
    return string_out.strip('\n')
        
#get_files_info("calculator", "bin")
    