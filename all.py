# -*- coding: UTF-8 -*-
import threading, time, os

from comments import comments
from reposts import reposts
from subscribers import subscribers
from results import results
from letters import letters
from draw import draw
from send import send

dir = '/home/user/newcover/cover/files/'

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

def main():

	file_output("all_pid", str(os.getpid()))
	file_output("all_time", 			str(time.localtime()[3])+" "+str(time.localtime()[4]))
	while 1:
			# init threads
			# join threads to the main thread
			t1 = threading.Thread(target=comments)
			t2 = threading.Thread(target=reposts)
			t1.start()
			t2.start()
			t1.join()
			t2.join()
			# comments()
			# print("comments ok", time.time() - last_time)
			# reposts()
			# print("reposts ok", time.time() - last_time)
			subscribers()
			#print("subscribers ok")
			results()
			print("results ok")
			letters()
			draw()
			print("draw ok")

			if(time.localtime()[5] < 55): time.sleep(55 - time.localtime()[5])
			send()
			print("send ok", time.localtime()[3], time.localtime()[4])
			
if(__name__ == "__main__"): main()
