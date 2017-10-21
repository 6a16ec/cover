import time, vk_api


dir = '/home/user/cover/files/'

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

def isbanned(stroka):
    vk = auth()
    a=vk.method('users.get', {'user_ids': stroka})[0]
    try:
        b=a['deactivated']
        return -1
    except:
        return 0

def subscribers():
    vk=auth()
    id_group=file_input_number('group_id')
    count = file_input_number('count_subscribers')

    defend_count=count+3
    a = vk.method('groups.getMembers', {'group_id': id_group, 'sort': 'time_desc', 'count':defend_count})['items']
    f = open(dir+'results_subscribers', 'w')
    j=0
    p=0
    while j<defend_count:
        if isbanned(a[j])!=-1 and p<count:
            f.write('subscriber'+' '+str(a[j])+'\n')
            p+=1
        j+=1
    f.close()

if(__name__ == "__main__"): subscribers()