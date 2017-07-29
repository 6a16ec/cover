import os

dir = os.getcwd() + "/"

scripts = ["all.py", "comments.py", "reposts.py", "likers.py", "subscribers.py", "results.py", "draw.py", "send.py", "protection.py"]

def file_input(name):
	file_name = dir + name
	file = open(file_name, 'r')
	input = file.readlines()
	file.close()
	return input

def file_input_number(name):
	file_name = dir + name
	file = open(file_name, 'r')
	input = file.readline()
	file.close()
	return int(input)

def file_output(name, output):
	file_name = dir + name
	file = open(file_name, 'w')
	file.write(output)
	file.close()

def ReplaceDirInFiles():
	for script in scripts:
		text, text_new = file_input(script), ""
		for string in text:
			if("dir =" in string):
				text_new += "dir = '"+dir+"files/'\n"
			else:
				text_new += string
		file_output(script, text_new)


if(__name__ == "__main__"): ReplaceDirInFiles()

