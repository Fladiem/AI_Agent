
import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    if not isinstance(working_directory, str) or not isinstance(file_path, str):
        #print('Error: first two arguments for run_python_file must be strings.')
        return 'Error: first two arguments for run_python_file must be strings.'
    absolute_workdir = os.path.abspath(working_directory)
    basic_path = os.path.join(working_directory, file_path)
    absolute_path = os.path.abspath(basic_path) #### This seems to be a more accurate structure to accomplish the intended outcome
    #print(f'{absolute_workdir}\n{basic_path}\n{absolute_path}')    #####Apply to other functions
    
    try:


        if absolute_workdir not in absolute_path:
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
        else:
            args = " ".join(args)
            file_out = subprocess.run(f"python3 {working_directory}/{file_path} {args}", capture_output=True, shell=True, timeout=30, text=True)
    
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

#run_python_file("calculator", "main", ["5 + 4"])