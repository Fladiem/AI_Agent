#source .venv/bin/activate   in cli to activate virtual environment
import sys
import os
from dotenv import load_dotenv
load_dotenv()
the_key=os.environ.get("GEMINI_API_KEY")
from google import genai   #For basic functionality
from google.genai import types #Facilitates storage and use of conversations for LLM
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file

def call_function(function_call_part, verbose=False):
    if verbose == True:
        print(f'calling function:{function_call_part.name}({function_call_part.args})')
    else:
        print(f' - Calling function: {function_call_part.name}')
    
    kwargs = dict(function_call_part.args)
    kwargs.setdefault("working_directory", "./calculator")
    #print(kwargs, type(function_call_part.args))
    function_dict = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file
    }
    func_call = function_dict[function_call_part.name](**kwargs)


    if function_dict.get(function_call_part.name) == None:
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"error": f"Unknown function: {function_call_part.name}"},
        )
    ],
)
    else:
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"result": func_call},
        )
    ],
)

def main(): #REMINDER: sys.argv is structured as a list
    if len(sys.argv) < 2 or len(sys.argv[1]) < 3: 
        print('Usage: uv run main.py "<YOUR_PROMPT_HERE>"\nProgram accepts one string as prompt\nShortest string accepted is "to?"')
        sys.exit(1)
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Write or overwrite files
- Execute Python files with optional arguments

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file   
        ]
    )
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=sys.argv[1])])
    ]
    
    client = genai.Client(api_key=the_key)
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,   #messages was previously sys.argv[1]
        config=types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=system_prompt
        )                                       
    )
    verbose_switch = False
    if len(sys.argv) > 2:
        if sys.argv[2] == "--verbose":
            verbose_switch = True
            print(f'User prompt: {sys.argv[1]}')
            print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
            print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
    print(response.text)
    call = response.function_calls[0] #function_calls is a list, so its lone entry, an object of the class Types, must first be accessed.
    #print("eee", response.function_calls)
    
    if response.function_calls != []:
        try:
            func_result = call_function(call, verbose_switch)
            if verbose_switch:
                print(f'-> {func_result.parts[0].function_response.response}')
            #print(f'Calling function: {call.name}({call.args})')
        except Exception as ee:
            return "Error: function call does not have ().parts[0].function_response.response)"

if __name__ == "__main__":
    main()


