import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    
    if len(sys.argv) == 1:
        print("No prompt provided")
        sys.exit(1)
    user_prompt = sys.argv[1]
    verbose = "--verbose" in sys.argv
    if verbose: print(f"User prompt: {user_prompt}")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    print(f"API Key is: {api_key}")

    client = genai.Client(api_key=api_key)

    model = "gemini-2.0-flash-001"
    #user_prompt = "Is the sky Blue? Reply with one word."
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
    response = client.models.generate_content(model=model, contents=messages)
    print(response.text)

    if verbose: print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    if verbose: print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
                                        
if __name__ == "__main__":
    main()