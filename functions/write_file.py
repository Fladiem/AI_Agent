import os
import sys
    
#EC == Error Catch, go back to other functions and resolve errors in established format <Error: *>

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



