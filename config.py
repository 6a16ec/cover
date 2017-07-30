#-#-# configuration file #-#-#
add_widget = "" # not correct
add_other_widget = "" # not correct

# information for vk
phone_number_or_email = ''
password = ''
group_id = ''
#People who do not need to be considered. Through a space.(optional)
exceptions = ''

## widgets ##
most_popular_comment = 'on'		# 'on' or 'off' 
most_popular_comments_count = '1'	# the number of such elements
add_widget += "comment" 


most_active_commentator = 'on'		# 'on' or 'off' 
most_active_commentators_count = '1'	# the number of such elements
add_widget += "commentator" 

most_active_reposter = 'on'		# 'on' or 'off' 
most_active_reposters_count = '1'	# the number of such elements
add_widget += "repost" 

most_active_liker = 'on'		# 'on' or 'off' 
most_active_likers_count = '1'		# the number of such elements
add_widget += "liker" 
array_size = 100 # whaaaaaaaaat!!!??!?!?!!?

last_subscriber = 'on'			# 'on' or 'off' 
last_subscribers_count = '1'		# the number of such elements
add_widget += "subscriber" 

time = 'on'			# 'on' or 'off' 
add_other_widget += "time" 

# monitoring config
monitoring_time = '24' # number of hours (write '-1' to monitoring this day)
number_of_posts = '50'





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


def main():

	ReplaceDirInFiles()	
	
	file_output("files/account", phone_number_or_email+'\n'+password+'\n')
	file_output("files/group_id", group_id)
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

