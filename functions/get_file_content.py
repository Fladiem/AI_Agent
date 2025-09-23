import os
import sys
#from func_config import *
from google import genai
from google.genai import types  #Needed for Schema
MAX_CHARACTERS = 10000  #Temporary hardcode to circumvent unittest discovery complications



def get_file_content(working_directory, file_path):
    absolute_path = os.path.abspath(os.path.join(working_directory, file_path))
    #print(os.path.abspath(absolute_path))
    if not absolute_path.startswith(os.path.abspath(working_directory)): ###if not has same effect as ==False
        print(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(absolute_path):
        print(f'Error: File not found or is not a regular file: "{file_path}"')
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    if os.path.isfile(absolute_path):
        
        with open(absolute_path, "r") as f:
            file_content_string = f.read(MAX_CHARACTERS)
            if len(str(file_content_string)) == MAX_CHARACTERS: #If == MAX_CHARACTERS, assume to be truncated
                print(str(file_content_string) + f'...File "{file_path}" truncated at {MAX_CHARACTERS} characters')
                print()
                return str(file_content_string) + f'...File "{file_path}" truncated at {MAX_CHARACTERS} characters'
            else:
                print(str(file_content_string))
                return str(file_content_string)

#get_file_content("calculator", "lorem.txt")