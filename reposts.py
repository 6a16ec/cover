import time, vk_api

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

def reposts():

	vk = auth()
	monitoring_hours = file_input_number('monitoring_time')
	if(monitoring_hours == -1):
		monitoring_seconds = time.localtime()[3]*60*60 + time.localtime()[4]*60 + time.localtime()[5]
	else:
		monitoring_seconds = monitoring_hours*60*60
	number_of_posts = file_input_number('number_of_posts')
	# variables for calculations
	array_id = []
	array_count = []
	max = 0
	id = 0


	#receipt of all posts for the past 24 hours
	posts = vk.method('newsfeed.get', {'filters': 'post', 'return_banned': 0, 'start_time': time.time() - monitoring_seconds, 'source_ids': file_input_number('group_id')*(-1), 'count': number_of_posts})

	for post in posts['items']:
		already = 0
		#getting the number of comments
		count_reposts =  post['reposts']['count']
		#getting id of a post
		post_id = post['post_id']
		while(already < count_reposts):
			#view all comments
			reposts = vk.method('wall.getReposts', {'owner_id': file_input_number('group_id')*(-1), 'post_id': post_id, 'count': 1000, 'offset': already})
			
			already += len(reposts['items'])
			if(len(reposts['items']) == 0): break
			for repost in reposts['items']:
				#id writer
				from_id = repost['from_id']
				#if writer is exist we increase the counter, otherwise we create writer
				exist = 0
				j = 0
				while (j < len(array_id)):
					if(array_id[j] == from_id):
						exist = 1
						array_count[j] += 1
						break
					j += 1 
				if(exist == 0):
					array_id.append(from_id)
					array_count.append(1)
			#print(post_id, len(reposts['items']), "really", count_reposts)



	#find maximum comments
	j = 0
	output = ''
	count = file_input_number('count_reposts')
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

		output += "repost"
		output += ' '
		output += str(id)
		output += ' '
		output += str(max)
		output += '\n'
		j += 1
		array_count[last_i] = 0
		max = 0
		id = 0
	file_output('results_reposts', output)