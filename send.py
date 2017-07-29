import vk_api, requests
from PIL import Image

dir = ''
cover_name = 'cover.png'
template = 'template.png'

def file_input_number(name):
	file_name = dir + name
	file = open(file_name, 'r')
	input = file.readline()
	file.close()
	return int(input)

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

def send():
	vk = auth()

	id_group=file_input_number('group_id')
	im1 = Image.open(dir + template)
	(dx, dy) = im1.size
	url = vk.method('photos.getOwnerCoverPhotoUploadServer', {'group_id': id_group,'crop_x2':dx,'crop_y2':dy})['upload_url']
	photo = {'photo': open(dir+cover_name, 'rb')}
	r = requests.post(url, files=photo)
	vk.method('photos.saveOwnerCoverPhoto', {'hash': r.json()['hash'], 'photo': r.json()['photo']})

if(__name__ == "__main__"): send()