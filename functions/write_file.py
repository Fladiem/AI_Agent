import os
import sys
from google import genai
from google.genai import types
    
#EC == Error Catch, go back to other functions and resolve errors in established format <Error: *>

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes string data to a file specified by file_path. Constrained to the current working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path relative to the working directory that will be written to. If the file does not exist it will be created. If the file exists its current contents will be overwritten.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The string data that is to be written to the file specified by file_path."
            )
        },
    ),
)

def write_file(working_directory, file_path, content):
    if not isinstance(working_directory, str) or not isinstance(file_path, str) or not isinstance(content, str):
        print('Error: all arguments for write_file() must be strings.')
        return 'Error: all arguments for write_file() must be strings.'
    absolute_workdir = os.path.abspath(working_directory)
    basic_path = os.path.join(working_directory, file_path)
    absolute_path = os.path.abspath(basic_path)
    #print(absolute_path)
    
    if absolute_workdir not in absolute_path:
        print(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if os.path.isfile(absolute_path):
        with open(absolute_path, "w") as f:
            f.write(content)
            print(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)' #LLM will need success strings as well as error strings.
    elif not os.path.exists(absolute_path):
        if not os.path.exists(absolute_workdir):
            os.makedirs(absolute_workdir)
        with open(absolute_path, "w") as ff:
            ff.write(content)
            print(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


    
               
        


#write_file("calculatorZZ", "loremssZ.txt", "Mike Wazowskyyyyy")
#EC: Need to catch errors for these arguments being an integer, .join does not accept integers



