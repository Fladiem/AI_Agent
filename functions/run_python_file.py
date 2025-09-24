
import os
import subprocess
from google import genai
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs Python files and returns their output as well as their exit code if it is not 0. Constrained to working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of a python file, relative to the working directory. This is the file that will be run.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Provides additional optional command line arguments for the Python file that will be run.")
        },
    ),
)


def run_python_file(working_directory, file_path, args=[]):
    if not isinstance(working_directory, str) or not isinstance(file_path, str):
        #print('Error: first two arguments for run_python_file must be strings.')
        return 'Error: first two arguments for run_python_file must be strings.'
    #absolute_workdir = os.path.abspath(working_directory)
    #basic_path = os.path.join(working_directory, file_path)
    #absolute_path = os.path.abspath(basic_path) #### This seems to be a more accurate structure to accomplish the intended outcome
    #print(f'{absolute_workdir}\n{basic_path}\n{absolute_path}')    #####Apply to other functions

    absolute_path = os.path.abspath(os.path.join(working_directory, file_path)) ####Actually, use this structure
    
    try:


        if not absolute_path.startswith(os.path.abspath(working_directory)):
            #print (f'Error: Cannot run "{file_path}" as it is outside the permitted working directory')
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.exists(absolute_path):
            #print(f'Error: "{file_path}" not found.')
            return f'Error: File "{file_path}" not found.'
        elif absolute_path[-3:] != ".py":
            #print(f'Error: {file_path} is not a Python file.')
            return f'Error: {file_path} is not a Python file.'
    

    #capture_output=True
    #stdout=True, stderr=True
       
        if args == []:
            file_out = subprocess.run(f"python3 {working_directory}/{file_path}",capture_output=True, shell=True, timeout=30, text=True)
            #print(file_out)
        else:
            args = " ".join(args)
            file_out = subprocess.run(f"python3 {working_directory}/{file_path} {args}", capture_output=True, shell=True, timeout=30, text=True)
        #print(file_out)
    
        if file_out == None:
            return "No output produced"
        elif file_out.returncode == 0:
            #print(f'STDOUT: {file_out.stdout}\nSTDERR: {file_out.stderr}')
            return f'STDOUT: {file_out.stdout}\nSTDERR: {file_out.stderr}'
        else:
            #print(f'STDOUT: {file_out.stdout}\nSTDERR: {file_out.stderr}\nProcess exited with code {file_out.returncode}')
            return f'STDOUT: {file_out.stdout}\nSTDERR: {file_out.stderr}\nProcess exited with code {file_out.returncode}'
        
    except Exception as e:
        #print(f'Error: executing python file: {e}')
        return f'Error: executing python file: {e}'

    
    
    #print(os.path.abspath(file_path))

run_python_file("calculator", "main", ["5 + 4"])