import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

if len(sys.argv) >= 2:
	user_prompt = sys.argv[1]
else:
	exit(1)

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
	contents=messages,
)

meta = response.usage_metadata
usage_message = f"Prompt tokens: {meta.prompt_token_count}\nResponse tokens: {meta.candidates_token_count}"

print(response.text)
print(usage_message)
