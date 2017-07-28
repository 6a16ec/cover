import time, vk_api

#direction with all files
dir = '/work/cover/files/'

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

def auth():
	# read data from file
	file = open(dir+'account', 'r')
	login = file.readline()[:-1]
	password = file.readline()[:-1]
	file.close()
	# authorization
	vk = vk_api.VkApi(login = login, password = password)
	vk.auth()
	return vk


def comments():
	vk = auth()
	monitoring_hours = file_input_number('monitoring_time')
	if(monitoring_hours == -1):
		monitoring_seconds = time.localtime()[3]*60*60 + time.localtime()[4]*60 + time.localtime()[5]
	else:
		monitoring_seconds = monitoring_hours*60*60
	number_of_posts = file_input_number('number_of_posts')
	comments_monitoring_seconds = monitoring_seconds
	# variables for calculations
	array_id = []
	array_count = []
	array_likes = []
	max = 0
	id = 0
	output = ''


	#receipt of all posts for the past 24 hours
	posts = vk.method('newsfeed.get', {'filters': 'post', 'return_banned': 0, 'start_time': time.time() - monitoring_seconds, 'source_ids': file_input_number('group_id')*(-1), 'count': number_of_posts})

	for post in posts['items']:
		#getting the number of comments
		count_comments =  post['comments']['count']
		#getting id of a post
		post_id = post['post_id']
		#view all comments
		already = 0
		while(already < count_comments):

			comments = vk.method('wall.getComments', {'owner_id': file_input_number('group_id')*(-1), 'post_id': post_id, 'count': 100, 'offset': already, 'need_likes': 1})

			if(len(comments['items']) == 0): break
			already += len(comments['items'])
			for comment in comments['items']:
				#if comment written last 24 hours/this day
				if(comment['date'] > time.time() - comments_monitoring_seconds):
					#id writer
					from_id = comment['from_id']
					#id writer
					
					count_likes = comment['likes']['count']
					#if writer is exist we increase the counter, otherwise we create writer
					exist = 0
					j = 0
					while (j < len(array_id)):
						if(array_id[j] == from_id):
							exist = 1
							array_count[j] += 1
							if(count_likes > array_likes[j]): array_likes[j] = count_likes
							break
						j += 1
					if(exist == 0 and int(from_id) > 0):
						array_id.append(from_id)
						array_count.append(1)
						array_likes.append(count_likes)



	#find maximum comments
	j = 0
	output = ''
	count = file_input_number('count_commentators')
	while(j < count):
		i = 0
		while(i < len(array_count)):
			if(array_count[i] > max):
				max = array_count[i]
				id = array_id[i]
				last_i = i
			i += 1
		#output data

		if(id == 0): break

		output += "commentator"
		output += ' '
		output += str(id)
		output += ' '
		output += str(max)
		output += '\n'
		j += 1
		array_count[last_i] = 0
		max = 0
		id = 0

	file_output('results_commentators', output)
	

	#find maximum likes
	j = 0
	output = ''
	count = file_input_number('count_comments')
	while(j < count):
		i = 0
		while(i < len(array_likes)):
			if(array_likes[i] > max):
				max = array_likes[i]
				id = array_id[i]
				last_i = i
			i += 1
		#output data
		if(id == 0): break

		output += "comment"
		output += ' '
		output += str(id)
		output += ' '
		output += str(max)
		output += '\n'
		j += 1
		array_likes[last_i] = 0
		max = 0
		id = 0
	file_output('results_comments', output)
