import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import available_functions

def main():
    
    #system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'
    system_prompt = """
        You are a helpful AI coding agent.
        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
            - List files and directories
            - Read file contents
            - Execute Python files with optional arguments
            - Write or overwrite files
        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """
    print(f"System prompt:\n{system_prompt}\n")

    if len(sys.argv) == 1:
        print("No prompt provided")
        sys.exit(1)
    user_prompt = sys.argv[1]
    verbose = "--verbose" in sys.argv
    if verbose: print(f"User prompt: {user_prompt}")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    #print(f"API Key is: {api_key}")

    client = genai.Client(api_key=api_key)

    model = "gemini-2.0-flash-001"
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt)
    #user_prompt = "Is the sky Blue? Reply with one word."
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
    # THIS IS THE LINE THAT DOES THE THING
    response = client.models.generate_content(model=model, contents=messages, config=config)
    
    print(f"Gemini's response:\n{response.text}\n")
    if verbose: print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    if verbose: print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    function_calls = response.function_calls
    if function_calls == None:
        print("No function calls were made")
    #elif len(function_calls) == 1:
        #print(f"Calling function: {function_calls.name}({function_calls.args})")
    else:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
        





if __name__ == "__main__":
    main()