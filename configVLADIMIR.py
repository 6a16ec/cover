#-#-# configuration file #-#-#
add_widget = "" # not correct
add_other_widget = "" # not correct

# information for vk
phone_number_or_email = '89307166797'
password = 'nigerok'
api_key = '30baf5175778d3092278afa12d08117ee7b20d4b8c58c0bf687921f840043fde7bb382cc38004c8bfdbbb'
group_id = '83678526'
#People who do not need to be considered. Through a space.(optional)
exceptions = ''

## widgets ##
most_popular_comment = 'off'		# 'on' or 'off'
most_popular_comments_count = '0'	# the number of such elements
add_widget += "comment"


most_active_commentator = 'off'		# 'on' or 'off'
most_active_commentators_count = '0'	# the number of such elements
add_widget += "commentator"

most_active_reposter = 'off'		# 'on' or 'off'
most_active_reposters_count = '0'	# the number of such elements
add_widget += "repost"

most_active_liker = 'off'		# 'on' or 'off'
most_active_likers_count = '0'		# the number of such elements
add_widget += "liker"
array_size = '1000' # whaaaaaaaaat!!!??!?!?!!?

last_subscriber = 'off'			# 'on' or 'off'
last_subscribers_count = '0'		# the number of such elements
add_widget += "subscriber"

time = 'on'			# 'on' or 'off' 
add_other_widget += "time 1425 90 /home/user/cover/files/RobotoCondensed-Regular.ttf 255 255 255 47\n"
 
add_other_widget += "temperature 1475 39 /home/user/cover/files/RobotoCondensed-Regular.ttf 255 255 255 30 Vladimir,RU\n"
# monitoring config
monitoring_time = '24' # number of hours (write '-1' to monitoring this day)
number_of_posts = '50'





import os

dir = os.getcwd() + "/"

scripts = ["all.py", "comments.py", "reposts.py", "likers.py", "subscribers.py", "results.py", "draw.py", "letters.py", "send.py", "protection.py"]

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


def main():

	ReplaceDirInFiles()	
	
	file_output("files/account", phone_number_or_email+'\n'+password+'\n')
	file_output("files/group_id", group_id)
	file_output("files/api_key", api_key)
	file_output("files/monitoring_time", monitoring_time)
	file_output("files/number_of_posts", number_of_posts)
	file_output("files/exceptions", exceptions)
	file_output("files/results_information", add_widget)
	file_output("files/widget", add_other_widget)
	file_output("files/array_size", array_size)

	widgets = ""
	if(most_popular_comment == "on"): 
		widgets += 'comments\n'
	file_output("files/count_comments", most_popular_comments_count)

	if(most_active_commentator == "on"): 
		widgets += 'commentators\n'
	file_output("files/count_commentators", most_active_commentators_count)

	if(most_active_reposter == "on"): 
		widgets += 'reposts\n'
	file_output("files/count_reposts", most_active_reposters_count)

	if(most_active_liker == "on"): 
		widgets += 'likes\n'
	file_output("files/count_likes", most_active_likers_count)

	if(last_subscriber == "on"): 
		widgets += 'subscribers\n'
	file_output("files/count_subscribers", last_subscribers_count)


	file_output("files/results_config", widgets)

	
	
	
	
	



if(__name__ == "__main__"): main()

