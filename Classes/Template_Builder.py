import os

def BuildTemplate(shellcode, template, script_dir):
	try:
		rel_path = template
		abs_file_path = os.path.join(script_dir, rel_path)
		with open(abs_file_path, "r") as fr:
			file_data = ''.join(fr.readlines())
			output = file_data.replace("<SHELLCODE>", shellcode)
			return output	
	except IOError:
		print("ERROR: Could not read template file from " + abs_file_path)
		raise


def WriteFile(path, content):
	try:	
		with open(path, "w") as fw:
			fw.write(content)
			fw.close()
	except:
		print("Error: Could not write data to file " + path)
		raise

def BuildCustomTemplate(template, script_dir):
	try:
		rel_path = template
		abs_file_path = os.path.join(script_dir, rel_path)
		with open(abs_file_path, "r") as fr:
			file_data = ''.join(fr.readlines())
			return file_data	
	except IOError:
		print("ERROR: Could not read template file from " + abs_file_path)
		raise
