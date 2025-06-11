import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
	user_prompt, is_verbose = get_arguments()

	client = get_client()
	response = get_response(user_prompt, client)

	if is_verbose:
		print_verbose(user_prompt, response)

	print(response.text)

def print_verbose(user_prompt, response):
	meta = response.usage_metadata
	
	message = ""
	message += f"User prompt: {user_prompt}\n"
	message += f"Prompt tokens: {meta.prompt_token_count}\n"
	message += f"Response tokens: {meta.candidates_token_count}\n"
	print(message)

def get_response(user_prompt, client):
	messages = [
		types.Content(role="user", parts=[types.Part(text=user_prompt)]),
	]

	response = client.models.generate_content(
		model='gemini-2.0-flash-001', 
		contents=messages,
	)
	return response

def get_arguments():
	parser = argparse.ArgumentParser(description="A simple script using argparse.") 
	parser.add_argument("user_prompt", help="The name of the user.") 
	parser.add_argument("--verbose", action="store_true", help="set if response should be verbose")
	args = parser.parse_args()
	
	# print(args)
	# print(args.user_prompt)
	# print(args.verbose)

	return (args.user_prompt, args.verbose)

# def get_sys_argv_user():
# 	if len(sys.argv) >= 2:
# 		user_prompt = sys.argv[1]
# 	else:
# 		raise SystemExit(1)
# 	return user_prompt

def get_client():
	load_dotenv()
	api_key = os.environ.get("GEMINI_API_KEY")
	client = genai.Client(api_key=api_key)
	return client

main()