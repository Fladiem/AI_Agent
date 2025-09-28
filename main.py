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
        print('Usage: uv run main.py "<YOUR_PROMPT_HERE>"\nProgram accepts one string as prompt\nAdd "--verbose" after prompt for more detail.')
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
    client = genai.Client(api_key=the_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=sys.argv[1])])
    ]
    
    calls_list = []
    verbose_switch = False
    
    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        verbose_switch = True

    iterations = 0   #initializing counter for while loop
    try:
        while iterations < 20:
            iterations += 1

            response = client.models.generate_content(
                model='gemini-2.0-flash-001', 
                contents=messages,   #messages was previously sys.argv[1]
                config=types.GenerateContentConfig(
                    tools=[available_functions], 
                    system_instruction=system_prompt
                )                                       
            )

    #(LLMstuff.content.parts[0].text)
            if response.candidates != []:
                for LLMstuff in response.candidates: #Adds responses to messages list
                
                    messages.append(LLMstuff.content) 
            #.parts[0].function_response.response  #4444   
            if response.function_calls:
                try:
                    call = response.function_calls #function_calls is a list, so its lone entry, an object of the class Types, must first be accessed.
                    for execution in call:
                        #print("execution:", execution)   
                        calls_list.append([execution.name, execution.args])
                        func_result = call_function(execution, verbose_switch)
                        #print('func result:', func_result)
                        messages.append(types.Content(role="user", parts=[
                            types.Part(
                                function_response=types.FunctionResponse(
                                    name=execution.name,
                                    response=func_result.parts[0].function_response.response
                                )
                            )
                        ]))
                        if verbose_switch == True: ## This is handled in call_function
                            print(f'-> {func_result.parts[0].function_response.response}')
                    #print(f"message1: Role: {messages[-2].role} Part: {messages[-2].parts}")
                    #print(f"message2: Role: {messages[-1].role} Part: {messages[-1].parts}")
                        
                except Exception as ee:
                    print(f"Error: {ee}), {calls_list}")  #4444
                    pass
            
            else:
                if response.text:
                    if verbose_switch:
                        print(f'User prompt: {sys.argv[1]}')
                        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
                        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
                        #if verbose_switch and calls_list != []:
                            #print(f'-> all calls: {calls_list}') #Print all calls before response generation.
                    print("Final response:\n", response.text)
                    #previous location of verbose_switch
                    
                    break
    except Exception as eee:
        print(f'Loop error: {eee}')
        pass    
# uv run main.py "show me the contents of lorem.txt" --verbose
# uv run main.py "show me the contents of README.md" --verbose
# uv run main.py "explain how the calculator renders the result to the console." --verbose
if __name__ == "__main__":
    main()


