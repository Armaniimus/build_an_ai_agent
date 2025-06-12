import os
import subprocess
def get_files_info(working_directory, directory=None):
	try:
		absolute_working_directory = os.path.abspath(working_directory)
		joined_path = os.path.join(working_directory, directory)
		absolute_directory = os.path.abspath(joined_path)

		if not os.path.isdir(absolute_working_directory):
			return f'Error: "{working_directory}" is not a directory'
		elif not os.path.isdir(absolute_directory):
			return f'Error: "{directory}" is not a directory'
		elif not absolute_directory.startswith(absolute_working_directory):
			return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
		
		contents = os.listdir(absolute_directory)

		message = ""
		for c in contents:
			tmp_join = os.path.join(absolute_directory, c)
			file_dir = os.path.abspath(tmp_join)
			
			is_dir = os.path.isdir(file_dir)
			size = os.path.getsize(file_dir)

			if message != "":
				message += "\n"

			message += f"- {c}: file_size={size} bytes, is_dir={is_dir}"

		return message
	except Exception as argument:
		return(f"Error: {argument}")

def get_file_content(working_directory, file_path):
	try:
		absolute_working_directory = os.path.abspath(working_directory)
		joined_path = os.path.join(working_directory, file_path)
		absolute_file = os.path.abspath(joined_path)

		if not os.path.isdir(absolute_working_directory):
			return f'Error: "{working_directory}" is not a directory'
		elif not os.path.isfile(absolute_file):
			return f'Error: File not found or is not a regular file: "{file_path}"'
		elif not absolute_file.startswith(absolute_working_directory):
			return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
		
		MAX_CHARS = 10000
		f = open(absolute_file, "r")
		file_content_string = f.read(MAX_CHARS)
		f.close()

		if len(file_content_string) == MAX_CHARS:
			file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'
		return file_content_string
	except Exception as argument:
		return(f"Error: {argument}")

def write_file(working_directory, file_path, content):
	try:
		absolute_working_directory = os.path.abspath(working_directory)
		joined_path = os.path.join(working_directory, file_path)
		absolute_file = os.path.abspath(joined_path)

		if not os.path.isdir(absolute_working_directory):
			return f'Error: "{working_directory}" is not a directory'
		elif not absolute_file.startswith(absolute_working_directory):
			return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
	
		parentfile = os.path.split(absolute_file)
		if not os.path.exists(parentfile[0]):
			os.makedirs(parentfile[0])
		
		f = open(absolute_file, "w")
		f.write(content)
		f.close()

		return(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
	except Exception as argument:
		return(f"Error: {argument}")

def run_python_file(working_directory, file_path):
	absolute_working_directory = os.path.abspath(working_directory)
	joined_path = os.path.join(working_directory, file_path)
	absolute_file = os.path.abspath(joined_path)

	if not os.path.isdir(absolute_working_directory):
		return f'Error: "{working_directory}" is not a directory'
	elif not os.path.isfile(absolute_file):
		return f'Error: File "{file_path}" not found.'
	elif not absolute_file.startswith(absolute_working_directory):
		return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
	elif not absolute_file.endswith(".py"):
		return f'Error: "{file_path}" is not a Python file.'


	try: 
		subproces = subprocess.run(["python", absolute_file], timeout=30, capture_output=True)

		stdout = f"STDOUT: {subproces.stdout}"
		stderr = f"STDERR: {subproces.stderr}"
		output = f"{stdout}\n{stderr}\n"

		if not subproces.returncode == 0:
			output += f"Process exited with code {subproces.returncode}\n"
		
		if (subproces.stdout + subproces.stderr == b''):
			output += "No output produced.\n"

		return(output)

	except Exception as e:
		return(f"Error: executing Python file: {e}")