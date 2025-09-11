#source .venv/bin/activate   in cli to activate virtual environment
import sys
import os
from dotenv import load_dotenv
load_dotenv()
the_key=os.environ.get("GEMINI_API_KEY")
from google import genai

def main(): #REMINDER: sys.argv is structured as a list
    if len(sys.argv) != 2 or len(sys.argv[1]) < 3: 
        print('Usage: uv run main.py "<YOUR_PROMPT_HERE>"\nProgram accepts one string as prompt\nShortest string accepted is "to?"')
        sys.exit(1)

        
    client = genai.Client(api_key=the_key)
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=sys.argv[1]
                                              
    )
    print(response.text)
    print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
    print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
    


if __name__ == "__main__":
    main()


