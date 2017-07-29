import time, vk_api, shutil, wget, os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from pycbrf.toolbox import ExchangeRates

dir = ''
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




def kurs():
	file = open(dir + 'widget', 'r')
	r = len(file.readlines())
	file.close()
	file = open(dir + 'widget', 'r')
	massiv_kurs=[]
	i = 0
	while i < r:
		line = file.readline()
		massiv_widget = line.split()
		if (massiv_widget[0] == 'curs'):
			massiv_kurs.append(massiv_widget)
		i += 1
	return massiv_kurs
def time_widget():
	file = open(dir + 'widget', 'r')
	r = len(file.readlines())
	file.close()
	file = open(dir + 'widget', 'r')
	i=0
	while i<r:
		line=file.readline()
		massiv_widget=line.split()
		if(massiv_widget[0]=='time'):
			return massiv_widget
		i+=1
	return -1
def temperature():
	file = open(dir + 'widget', 'r')
	r = len(file.readlines())
	file.close()
	file = open(dir + 'widget', 'r')
	i = 0
	while i < r:
		line = file.readline()
		massiv_widget = line.split()
		if (massiv_widget[0] == 'temperature'):
			return massiv_widget
		i += 1
	return -1

def exchange_rate(value):
	rates = ExchangeRates()
	return (rates[value].value)
	
def letters():
	vk = auth()
	im1 = Image.open(dir + 'template.png')
	draw = ImageDraw.Draw(im1)
	massiv_valute=kurs()
	i=0
	#ciclom probegaus po massivu s valutami i otrisovavayu ih
	while i<len(massiv_valute):
		yacheika_massiv_valute=massiv_valute[i]
		shrift = yacheika_massiv_valute[3]
		colors = yacheika_massiv_valute[4:7]
		size_letter = int(yacheika_massiv_valute[7])
		font = ImageFont.truetype(shrift, size_letter)
		draw.text((int(yacheika_massiv_valute[1]), int(yacheika_massiv_valute[2])), str(exchange_rate(yacheika_massiv_valute[8]))[0:5], font=font, fill=(int(colors[0]), int(colors[1]), int(colors[2])))
		i+=1
	i=0
	massiv_temperature=temperature()
	if massiv_temperature != -1:
		s_city = massiv_temperature[8]
		city_id = 0
		appid = '7c7bf0724021959ee264734a91ee67bc'
		try:
			res = requests.get("http://api.openweathermap.org/data/2.5/find",
							   params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
			data = res.json()
			cities = ["{} ({})".format(d['name'], d['sys']['country'])
					  for d in data['list']]
			city_id = data['list'][0]['id']
		except Exception as e:
			print("Exception (find):", e)
			pass
		try:
			res = requests.get("http://api.openweathermap.org/data/2.5/weather",
							   params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
			data = res.json()
			temperature_stroka=str(data['main']['temp'])
			shrift = massiv_temperature[3]
			colors = massiv_temperature[4:7]
			size_letter = int(massiv_temperature[7])
			font = ImageFont.truetype(shrift, size_letter)
			draw.text((int(massiv_temperature[1]), int(massiv_temperature[2])), temperature_stroka,
					  font=font, fill=(int(colors[0]), int(colors[1]), int(colors[2])))
		except Exception as e:
			print("Exception (weather):", e)
			pass
	#vremya
	massiv_time = time_widget()
	if massiv_time!=-1:
		shrift = massiv_time[3]
		colors = massiv_time[4:7]
		size_letter = int(massiv_time[7])
		font = ImageFont.truetype(shrift, size_letter)
		time_now=datetime.now()
		time_date=datetime.strftime(time_now, "%H:%M")
		state = str(int(time_date[0:2])%24) if time_date[3:5]!='59' else str((int(time_date[0:2])+1)%24)
		time_date=state+':'+str((int(time_date[3:5])+1)%60).rjust(2,'0')
		draw.text((int(massiv_time[1]), int(massiv_time[2])), time_date,
			  font=font, fill=(int(colors[0]), int(colors[1]), int(colors[2])))
	file = open(dir + 'results', 'r')
	r = len(file.readlines())
	file.close()
	coordinates = open(dir + 'results_information', 'r')
	file = open(dir + 'results', 'r')
	i = 0
	while i < r:
		line = file.readline()
		spisok = line.split()
		d = vk.method('users.get', {'user_ids': spisok[1]})
		line = coordinates.readline()
		coordinates_spisok = line.split()
		shrift = coordinates_spisok[7]
		colors = coordinates_spisok[8:11]
		size_letter = int(coordinates_spisok[11])
		font = ImageFont.truetype(shrift, size_letter)
		# formiruyo vid stroki v zavisimosti ot flashka
		string_of_best='hoi'
		if coordinates_spisok[13]=='1' :
			string_of_best=d[0]['first_name'] + ' ' + d[0]['last_name']
		if coordinates_spisok[13]=='2' :
			string_of_best=d[0]['first_name'] + '\n' + d[0]['last_name']
		if coordinates_spisok[13]=='0' :
			string_of_best=d[0]['first_name']
		draw.text((int(coordinates_spisok[3]), int(coordinates_spisok[4])), string_of_best, font=font, fill=(int(colors[0]), int(colors[1]), int(colors[2])))
		if spisok[0] != 'subscriber':
			draw.text((int(coordinates_spisok[5]), int(coordinates_spisok[6])), spisok[2], font=font,fill=(int(colors[0]), int(colors[1]), int(colors[2])))
		i += 1
	im1.save(dir + 'cover.png')
	coordinates.close()
	file.close()

	
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
	link = vk.method('users.get', {'user_ids': id, 'fields': 'photo_100'})[0]['photo_100']
	file_name = wget.download(link, dir)
	print(" ")
	print(file_name)
	circle(file_name, dir+"avatar.png")
	resolution("avatar.png", "avatar.png", r, r)
	paste(dir+cover_name, dir+"avatar.png", x, y)
	os.remove(dir+"avatar.png")
	os.remove(file_name)

def draw():

	vk = auth()
	letters()

	results = file_input("results")
	coordinates = file_input("results_information")
	i = 0
	while i < len(results):

		id_user = int(results[i].split(' ')[1])

		x_avatar = int(coordinates[i].split(' ')[1])
		y_avatar = int(coordinates[i].split(' ')[2])
		r_avatar = int(coordinates[i].split(' ')[12])
		avatar_paste(id_user, x_avatar, y_avatar, r_avatar, vk)
		i+=1

if(__name__ == "__main__"): main()