import time, vk_api
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
dir = '/home/user/newcover/cover/files/'
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
	massiv_kurs = []
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
	i = 0
	while i < r:
		line = file.readline()
		massiv_widget = line.split()
		if (massiv_widget[0] == 'time'):
			return massiv_widget
		i += 1
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
	massiv_valute = kurs()
	i = 0
	# ciclom probegaus po massivu s valutami i otrisovavayu ih
	while i < len(massiv_valute):
		yacheika_massiv_valute = massiv_valute[i]
		shrift = yacheika_massiv_valute[3]
		colors = yacheika_massiv_valute[4:7]
		size_letter = int(yacheika_massiv_valute[7])
		font = ImageFont.truetype(shrift, size_letter)
		draw.text((int(yacheika_massiv_valute[1]), int(yacheika_massiv_valute[2])),
				  str(exchange_rate(yacheika_massiv_valute[8]))[0:5], font=font,
				  fill=(int(colors[0]), int(colors[1]), int(colors[2])))
		i += 1
	i = 0
	massiv_temperature = temperature()
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
			temperature_stroka = str(data['main']['temp'])
			shrift = massiv_temperature[3]
			colors = massiv_temperature[4:7]
			size_letter = int(massiv_temperature[7])
			font = ImageFont.truetype(shrift, size_letter)
			draw.text((int(massiv_temperature[1]), int(massiv_temperature[2])), temperature_stroka,
					  font=font, fill=(int(colors[0]), int(colors[1]), int(colors[2])))
		except Exception as e:
			print("Exception (weather):", e)
			pass
	# vremya
	massiv_time = time_widget()
	if massiv_time != -1:
		shrift = massiv_time[3]
		colors = massiv_time[4:7]
		size_letter = int(massiv_time[7])
		font = ImageFont.truetype(shrift, size_letter)
		time_now = datetime.now()
		time_date = datetime.strftime(time_now, "%H:%M")
		state = str(int(time_date[0:2]) % 24) if time_date[3:5] != '59' else str((int(time_date[0:2]) + 1) % 24)
		time_date = state + ':' + str((int(time_date[3:5]) + 1) % 60).rjust(2, '0')
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
		string_of_best = 'hoi'
		if coordinates_spisok[13] == '1':
			string_of_best = d[0]['first_name'] + ' ' + d[0]['last_name']
		if coordinates_spisok[13] == '2':
			string_of_best = d[0]['first_name'] + '\n' + d[0]['last_name']
		if coordinates_spisok[13] == '0':
			string_of_best = d[0]['first_name']
		draw.text((int(coordinates_spisok[3]), int(coordinates_spisok[4])), string_of_best, font=font,
				  fill=(int(colors[0]), int(colors[1]), int(colors[2])))
		if spisok[0] != 'subscriber':
			draw.text((int(coordinates_spisok[5]), int(coordinates_spisok[6])), spisok[2], font=font,
					  fill=(int(colors[0]), int(colors[1]), int(colors[2])))
		i += 1
	im1.save(dir + 'cover.png')
	coordinates.close()
	file.close()


if(__name__ == "__main__"): reposts()
