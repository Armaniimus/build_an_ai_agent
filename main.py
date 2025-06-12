import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
	user_prompt, is_verbose = get_arguments()
	system_prompt = get_system_prompt()
	available_functions = get_function_schema()

	client = get_client()
	response = get_response(client, user_prompt, system_prompt, available_functions)

	if is_verbose:
		print_verbose(user_prompt, response)

	function_calls = response.function_calls
	if function_calls != None:
		for func in function_calls:
			print(f"Calling function: {func.name}({func.args})")

	else: print(response.text)

def print_verbose(user_prompt, response):
	meta = response.usage_metadata
	
	message = ""
	message += f"User prompt: {user_prompt}\n"
	message += f"Prompt tokens: {meta.prompt_token_count}\n"
	message += f"Response tokens: {meta.candidates_token_count}\n"
	print(message)

def get_response(client, user_prompt, system_prompt, available_functions):
	messages = [
		types.Content(role="user", parts=[types.Part(text=user_prompt)]),
	]

	response = client.models.generate_content(
		model='gemini-2.0-flash-001', 
		contents=messages,
		config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions]),
	)

	return response

def get_arguments():
	parser = argparse.ArgumentParser(description="A simple script using argparse.") 
	parser.add_argument("user_prompt", help="The name of the user.") 
	parser.add_argument("--verbose", action="store_true", help="set if response should be verbose")
	args = parser.parse_args()

	return (args.user_prompt, args.verbose)

def get_client():
	load_dotenv()
	api_key = os.environ.get("GEMINI_API_KEY")
	client = genai.Client(api_key=api_key)
	return client

def get_function_schema():
	schema_get_files_info = types.FunctionDeclaration(
		name="get_files_info",
		description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
		parameters=types.Schema(
			type=types.Type.OBJECT,
			properties={
				"directory": types.Schema(
					type=types.Type.STRING,
					description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
				),
			},
		),
	)

	schema_get_file_content = types.FunctionDeclaration(
		name="get_file_content",
		description="get the contents of a specified file, constrained to the working directory.",
		parameters=types.Schema(
			type=types.Type.OBJECT,
			properties={
				"file_path": types.Schema(
					type=types.Type.STRING,
					description="a path to an specified file, relative to the working directory.",
				),
			},
		),
	)

	schema_write_file= types.FunctionDeclaration(
		name="write_file",
		description="function to write new files inside the working directory, constrained to the working directory.",
		parameters=types.Schema(
			type=types.Type.OBJECT,
			properties={
				"file_path": types.Schema(
					type=types.Type.STRING,
					description="a path to an specified file, relative to the working directory.",
				),
				"content": types.Schema(
					type=types.Type.STRING,
					description="the contents of the changed file or new file",
				),
			},
		),
	)

	schema_run_python_file= types.FunctionDeclaration(
		name="run_python_file",
		description="function run python scripts, constrained to the working directory.",
		parameters=types.Schema(
			type=types.Type.OBJECT,
			properties={
				"file_path": types.Schema(
					type=types.Type.STRING,
					description="a path to an specified file, relative to the working directory.",
				),
			},
		),
	)

	available_functions = types.Tool(
		function_declarations=[
			schema_get_files_info,
			schema_get_file_content,
			schema_write_file,
			schema_run_python_file
		]
	)

	return available_functions

def get_system_prompt():
	return """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

main()