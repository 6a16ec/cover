import time, vk_api, shutil, wget, os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from pycbrf.toolbox import ExchangeRates
from letters import letters
dir = '/home/user/newcover/cover/files/'
cover_name = 'cover.png'
template = 'template.png'

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

	
def resolution(name, name_res, width, height):
	img = Image.open(dir+name)
	resized_img = img.resize((width, height), Image.ANTIALIAS)
	resized_img.save(dir+name_res)

	
def circle(name, name_res):
	image = Image.open(name) 
	width = image.size[0] 
	height = image.size[1] 
	image_new = Image.new("RGBA", (width,height), (0,0,0,0))
	draw = ImageDraw.Draw(image_new) 

	x0 = width / 2
	y0 = height / 2
	r  = min(x0, y0)

	pix = image.load() 
	for i in range(width):
		for j in range(height):
			transp = 1
			if((i - x0)*(i - x0) + (j - y0)*(j - y0) > r*r):
				transp = 0
			draw.point((i, j), (pix[i, j][0]*transp, pix[i, j][1]*transp, pix[i, j][2]*transp, 255*transp))

	image_new.save(name_res, "PNG")
	del draw

def paste(name_main, name_paste, x, y):
	main  = Image.open(name_main)
	paste = Image.open(name_paste)
	main.paste(paste, (x, y),  paste)
	main.save(name_main)

def avatar_paste(id, x, y, r, vk):
	if(id != -1):

		link = vk.method('users.get', {'user_ids': id, 'fields': 'photo_100'})[0]['photo_100']

		if(link != 'https://vk.com/images/camera_100.png'):
			file_name = wget.download(link, dir)
			circle(file_name, dir+"avatar.png")
			resolution("avatar.png", "avatar.png", r, r)
			paste(dir+cover_name, dir+"avatar.png", x, y)
			os.remove(dir+"avatar.png")
			os.remove(file_name)
		else:
			resolution("camera.png", "avatar.png", r, r)
			paste(dir+cover_name, dir+"avatar.png", x, y)
			os.remove(dir+"avatar.png")
	else:
		resolution("error.png", "avatar.png", r, r)
		paste(dir+cover_name, dir+"avatar.png", x, y)
		os.remove(dir+"avatar.png")



def draw():

	vk = auth()

	results = file_input("results")
	coordinates = file_input("results_information")
	i = 0
	while i < len(results):

		item = results[i].split(' ')[0]
		id_user = int(results[i].split(' ')[1])
		if(item == "error"): id_user = -1;

		x_avatar = int(coordinates[i].split(' ')[1])
		y_avatar = int(coordinates[i].split(' ')[2])
		r_avatar = int(coordinates[i].split(' ')[12])
		avatar_paste(id_user, x_avatar, y_avatar, r_avatar, vk)
		i+=1

if(__name__ == "__main__"): draw()
