#source .venv/bin/activate   in cli to activate virtual environment
import sys
import os
from dotenv import load_dotenv
load_dotenv()
the_key=os.environ.get("GEMINI_API_KEY")
from google import genai   #For basic functionality
from google.genai import types #Facilitates storage and use of conversations for LLM
from functions.get_files_info import schema_get_files_info

def main(): #REMINDER: sys.argv is structured as a list
    if len(sys.argv) < 2 or len(sys.argv[1]) < 3: 
        print('Usage: uv run main.py "<YOUR_PROMPT_HERE>"\nProgram accepts one string as prompt\nShortest string accepted is "to?"')
        sys.exit(1)
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
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
    if len(sys.argv) > 2:
        if sys.argv[2] == "--verbose":
            print(f'User prompt: {sys.argv[1]}')
            print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
            print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
    print(response.text)
    calls = response.function_calls[0] #function_calls is a list, so its lone entry, an object of the class Types, must first be accessed.
    
    if response.function_calls != []:
        print(f'Calling function: {calls.name}({calls.args})')


if __name__ == "__main__":
    main()


