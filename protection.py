import time, os

dir = '/home/user/cover/files/'
work_direction = dir[:-6]

def file_input(name):
	file_name = dir + name
	file = open(file_name, 'r')
	input = file.readline()
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

def main():
	try:
		time_last = file_input("all"+"_time")
		h = int(time_last.split(" ")[0])
		m = int(time_last.split(" ")[1])
		if(h != time.localtime()[3] or time.localtime()[4] - m >= 3):
			pid = file_input_number("all"+"_pid")
			os.system("kill "+str(pid))
			os.system("nohup python3 "+work_direction+"all.py &")
	except:
		os.system("nohup python3 "+work_direction+"all.py &")

	try:
		time_last = file_input("liker"+"_time")
		h = int(time_last.split(" ")[0])
		m = int(time_last.split(" ")[1])
		if(h != time.localtime()[3] or time.localtime()[4] - m >= 3):
			pid = file_input_number("liker"+"_pid")
			os.system("kill "+str(pid))
			os.system("nohup python "+work_direction+"likers.py 1 &")
	except:
		os.system("nohup python "+work_direction+"likers.py 1 &")

if(__name__ == "__main__"):
	while 1:
		main()
		time.sleep(60-time.localtime()[5])
