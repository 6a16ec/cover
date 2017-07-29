dir = ''

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

def results():
	results = ""
	actions = file_input("results_config") 
	for action in actions:

		count = file_input_number("count"+"_"+action[:-1])
		result = file_input("results"+"_"+action[:-1])

		i = 0

		while i < count:
			try:
				if(int(result[i].split(" ")[1]) != 0): results += result[i]
				else: results += "error 0 0\n"

			except:
				results += "error 0 0\n"
			i += 1


	file_output("results", results)
	
if(__name__ == "__main__"): main()