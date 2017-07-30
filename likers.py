import vk_api, time, os

dir = ''

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

def group_id():
    file = open(dir+'group_id', 'r')
    group_id = file.readline()
    file.close()
    return int(group_id)

def find(massiv,stroka,last_index):
    o=0
    while o<=last_index:
        if massiv[o][0]==stroka :
            return o
        o=o+1
    return (-1)

def myfind(massiv,stroka,last_index):
    o=0
    while o<=last_index:
        if massiv[o]==str(stroka) :
            return o
        o=o+1
    return (-1)
    
def likers():
    x = 0
    file = open(dir + 'exceptions', 'r')
    line = file.readline()
    massiv_exceptions=line.split()
    file.close()
    f = open(dir + 'array_size', 'r')
    array_size = int(f.read())
    f.close()
    likers = [[0 for i in range(2)] for i in range(array_size)]
    vk=auth()
    id_group = '-'+str(group_id())
    d = vk.method('newsfeed.get',
                  {'filters': 'post', 'return_banned': 1, 'start_time': time.time() - 86400, 'end_time': time.time(),
                   'source_ids': id_group, 'count': 50})['items']
    j = 0
    main_last_index = 0
    while j < len(d):
        if main_last_index>len(d)-10000:
            h=[[0 for i in range(2)] for i in range(10000)]
            likers.extend(h)
        size_likes = vk.method('likes.getList',
                               {'type': 'post', 'owner_id': id_group, 'filter': 'likes', 'friends_only': '0',
                                'offset': '0', 'count': '1000', 'item_id': d[j]['post_id']})['count']
        i = 0
        offset = 0
        while i <= size_likes // 1000:
            h = vk.method('likes.getList',
                          {'type': 'post', 'owner_id': id_group, 'filter': 'likes', 'friends_only': '0',
                           'offset': offset, 'count': '1000', 'item_id': d[j]['post_id']})['items']
            n = 0
            while n < len(h):
                t = find(likers, h[n], main_last_index)
                if t == -1:
                    likers[main_last_index + 1][0] = h[n]
                    likers[main_last_index + 1][1] += 1
                    main_last_index += 1
                else:
                    likers[t][1] += 1
                n = n + 1
            offset = offset + 1000
            i += 1
        j = j + 1
    j = 0
    index_big_elem = 0
    max = 0
    while j <= main_last_index:
        if int(likers[j][1]) > max:
            max = int(likers[j][1])
            index_big_elem = j
        j += 1
    f = open(dir + 'count_likes', 'r')
    n_max=int(f.read())
    n_max=n_max+6
    f.close()
    index_big=[[0 for i in range(2)] for i in range(n_max)]
    j=0
    print(likers)
    #zapolnenie massiva index_big naibolshymi elementami
    while j<n_max :
        max = 0
        i = 0
        big_index=0
        while i <= main_last_index:
            if likers[i][1] > max:
                max = likers[i][1]
                big_index=i
            i += 1
        index_big[j][0]=likers[big_index][0]
        index_big[j][1] = likers[big_index][1]
        likers[big_index][0]=0
        likers[big_index][1] = 0
        j+=1
    f = open(dir+'results_likes', 'w')

    j=0
    p=0
    # zapis v fail resultatov
    while j<len(index_big):
        if p<n_max-6  and myfind(massiv_exceptions,index_big[j][0],2)==-1 and isbanned(index_big[j][0])!=-1:
            f.write('like '+str(index_big[j][0])+' '+str(index_big[j][1])+'\n')
            p+=1
        j=j+1
    f.close()

def file_output(name, output):
	file_name = dir + name
	file = open(file_name, 'w')
	file.write(output)
	file.close()



if(__name__ == "__main__"): likers()
