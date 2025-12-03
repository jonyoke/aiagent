import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import call_function, available_functions

MAX_AGENT_ITERATIONS = 20

def main():
    system_prompt = """
        You are a helpful AI coding agent.
        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
            - List files and directories using "get_files_info"
            - Read file contents using "get_file_content"
            - Execute Python files with optional arguments using "run_python_file"
            - Write or overwrite files using "write_file"
        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """

    if len(sys.argv) == 1:
        print("No prompt provided")
        sys.exit(1)
    user_prompt = sys.argv[1]
    verbose = "--verbose" in sys.argv
    if verbose: print(f"System prompt:\n{system_prompt}\n")
    if verbose: print(f"User prompt: {user_prompt}")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    model = "gemini-2.0-flash-001"
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt)
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]


    iter = 0
    agent_finished = False
    while iter < MAX_AGENT_ITERATIONS and not agent_finished:
        iter += 1
        #Ask the Agent to do things in a loop
        # This first call is the one that sends messages to the agent and receives a response
        response = client.models.generate_content(model=model, contents=messages, config=config)
    
        print(f"\n****************\nITERATION {iter}\n****************\n")
        print(f"Gemini's response text:\n{response.text}\n")
        if verbose: print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        if verbose: print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if response.candidates is None:
            print("No candidates exist")
            agent_finished = True
        else:
            for candidate in response.candidates:
                messages.append(candidate.content)

        function_calls = response.function_calls
        function_call_response_texts = []
        if function_calls == None:
            print("No function calls were made")
            agent_finished = True
        else:
            for function_call in response.function_calls:
                # THIS IS THE LINE THAT DOES THE THING
                call_function_output = call_function(function_call, verbose)
            
                if call_function_output is None:
                    raise Exception("Error: call_function returned None")
                elif not hasattr(call_function_output, "parts"):
                    raise Exception("Error: call_function_output does not have 'parts'")
                elif len(call_function_output.parts) == 0:
                    raise Exception("Error: call_function_output.parts has length = 0")
                elif not hasattr(call_function_output.parts[0], "function_response"):
                    raise Exception("Error: call_function_output.parts[0] does not have 'function.response'")
                elif not hasattr(call_function_output.parts[0].function_response, "response"):
                    raise Exception("Error: call_function_output.parts[0].function_response does not have 'response'")
                elif "result" not in call_function_output.parts[0].function_response.response:
                    raise Exception("'result' call_function_output.parts[0].function_response.response")
                else:
                    #function_call_responses.append(call_function_output.parts[0])
                    #if verbose: print(f"-> {call_function_output.parts[0].function_response.response}")
                    function_call_response_text = call_function_output.parts[0].function_response.response['result']
                    if verbose: print(f"-> {function_call_response_text}")
                    function_call_response_texts.append(function_call_response_text)
            function_call_response_texts_str = "\n".join(function_call_response_texts)
            messages.append(types.Content(role="user", parts=[types.Part(text=function_call_response_texts_str)]))

        print(f"Current list of messages for iteration {iter}:")
        for message in messages:
            print(f"{message.role}: {message.parts[0].text}")
                
            

        





if __name__ == "__main__":
    main()