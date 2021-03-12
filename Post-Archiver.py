from datetime import datetime
import requests, json, sys, os, threading, time, re, subprocess

sub = sys.argv[1]
t = sys.argv[2]
limit = int(sys.argv[3])
max_downloads = int(sys.argv[4])
date = datetime.now().strftime('%Y-%m-%d')
headers = {'User-Agent': 'Post Archiver'}
threads = []
extensions = ['.jpg', '.png', '.jpeg', '.gif', '.mp4', '.webm', '.gifv']
links = []
finished_links = []

os.makedirs('r/{}/posts'.format(sub), exist_ok=True)
os.makedirs('logs/{}/'.format(datetime.now().strftime('%Y-%m-%d')), exist_ok=True)

if limit > 100 and limit in [200, 300, 400, 500, 600, 700, 800, 900, 1000]:
	pages = int(limit / 100)
	url1 = 'https://www.reddit.com/r/{}/top.json?sort=top&t={}&limit=100'.format(sub, t)
	sys.stdout.write('\rFetching pages: [1/{}][{}]'.format(str(pages), sub))
	sys.stdout.flush()
	big_json = [requests.get(url1, headers=headers).text]
	for a in range(1,pages):
		sys.stdout.write('\rFetching pages: [{}/{}][{}]'.format(str(a+1), str(pages), sub))
		sys.stdout.flush()
		json1 = requests.get(url1+'&after={}'.format(json.loads(big_json[-1])['data']['after']), headers=headers).text
		big_json.append(json1)
	sys.stdout.write('\n')
	for a in range(1,len(big_json)+1):
		with open('r/{}/{}_{}.json'.format(sub, date, str(a)), 'w') as f:
			f.write(big_json[a-1])

elif limit > 100:
	print('''If you choose to archive more than 100 posts, you must do it in 100-post increments (i.e 200, 300..., not 250, 375...)
You also can\'t get more than 1000 posts due to reddit\'s API limitations''')

else:
	url = 'https://www.reddit.com/r/{}/top.json?sort=top&t={}&limit={}'.format(sub, t, str(limit))
	list_json = requests.get(url, headers=headers).text
	loaded_list_json = json.loads(list_json)
	with open('r/{}/{}_1.json'.format(sub, date), 'w') as f:
		f.write(list_json)

if t.lower() == 'day':
	date = datetime.now().strftime('%Y-%m-%d')
elif t.lower() == 'week':
	date = 'Week_of_' + datetime.now().strftime('%Y-%m-%d')
elif t.lower() == 'month':
	date = datetime.now().strftime('%Y-%m')
elif t.lower() == 'year':
	date = datetime.now().strftime('%Y')
elif t.lower() == 'all':
	date = 'All_Time'

def download(url, id):
	json_file = requests.get(url, headers=headers).text
	with open('r/{}/posts/{}.json'.format(sub, id), 'w') as f:
		f.write(json_file)

def download_image(url, file_name):

	files = os.listdir(f'static/images/{sub}')

	if '.png' not in url and '.jpg' not in url and '.jpeg' not in url:
		
		try:

			path = 'static/images/{}/{}.mp4'.format(sub, file_name)

			out = os.system(f'YTDL.py "{url}" "{path}"')


			if out == 1 and 'giant.gfycat' in url:
				
				url = url.replace('giant.gfycat', 'thumbs2.redgifs')

				path = 'static/images/{}/{}.mp4'.format(sub, file_name)

				os.system(f'YTDL.py "{url}" "{path}"')
			
		except:
			pass
	else:
		with open('static/images/{}/{}'.format(sub, file_name+'.jpg'), 'wb') as file:
			response = requests.get(url, headers=headers)
			file.write(response.content)
		with open('logs/{}/{}.txt'.format(datetime.now().strftime('%Y-%m-%d'), sub), 'a+') as f:
			f.write(f'[{datetime.now()}][downloading][{url}]--->[static/images/{sub}/{file_name}.png]\n')

# sys.stdout.write('\r[{}/{}]'.format(current_num, folder_len))
# sys.stdout.flush()
current_post = 0
try:
	for a in big_json:
		for b in json.loads(a)['data']['children']:

			if b['kind'] != 't3':
				os.system('cls')
				input(b['kind'])

			current_post += 1
			sys.stdout.write('\rFetching posts: [{}/{}][{}]'.format(str(current_post), str(limit), sub))
			sys.stdout.flush()
			json_url = 'https://reddit.com'+b['data']['permalink']+'.json'
			thread_id = b['data']['id']

			t = threading.Thread(target=download, args=(json_url, thread_id,))
			t.start()
			threads.append(t)

			link = b['data']['url'], b['data']['id']
			
			os.makedirs('static/images/{}'.format(sub), exist_ok=True)

			if '/gallery/' in link[0]:
				# os.system('cls')
				# input(b)
				link = b['data']['url'], b['data']['id'], b

			links.append(link)
			time.sleep(0.02)

		if threading.active_count() >= max_downloads:
			for e in threads:
				try:
					e.join()
				except:
					pass

				threads.clear()
	sys.stdout.write('\n')
except NameError as e:
	for a in loaded_list_json['data']['children']:

		

		current_post += 1
		sys.stdout.write('\rFetching posts: [{}/{}][{}]'.format(str(current_post), str(limit), sub))
		sys.stdout.flush()
		json_url = 'https://reddit.com'+a['data']['permalink']+'.json'
		thread_id = a['data']['id']

		t = threading.Thread(target=download, args=(json_url, thread_id,))
		t.start()
		threads.append(t)

		link = a['data']['url'], a['data']['id']
		
		os.makedirs('static/images/{}'.format(sub), exist_ok=True)

		if '/gallery/' in link[0]:
			# print(link[0])
			link = a['data']['url'], a['data']['id'], a

		links.append(link)
		time.sleep(0.02)

for e in threads:
	try:
		e.join()
	except:
		pass

threads.clear()

current_image_link = 0

files = os.listdir(f'static/images/{sub}')
# input(files)

for c in links:

	current_image_link += 1
	sys.stdout.write('\rParsing image links: [{}/{}][{}][{}]'.format(str(current_image_link), str(len(links)), sub, c[1]))
	sys.stdout.flush()
	# if len([fn for fn in files if c[1] in fn]) == 0:
	# 	# print(c)

	
	if len([fn for fn in files if c[1] in fn]) > 0 and ('/a/' not in c[0] and '/gallery/' not in c[0]):
		# print([fn for fn in files if c[1] in fn])
		pass

	elif "imgur.com" in c[0]:
		

		if '/a/' in c[0] or '/gallery/' in c[0]:
			finished_links.append(c)

		elif c[0].endswith(tuple(extensions)):
			if c[0].endswith('.gifv'):
				newurl = c[0].replace(".gifv",".mp4")
				finished_links.append(tuple([newurl, c[1]]))

			else:
				finished_links.append(c)

		else:
			html_page = requests.get(c[0])
			if html_page.status_code == 404:
				pass
				# print('404: skipping')
			else:
				imgur_id = c[0].split('/')[-1]
				# print(c[0])
				try:
					link = re.findall('(?:href|src)="(?:https?:)?(\/\/i\.imgur\.com\/{}\.\S+?)"'.format(imgur_id), html_page.text)[0]
					link = 'https:' + link
					finished_links.append(tuple([link, c[1]]))
				except IndexError:
					
					fixedlink = c[0].split('?')[0]
					
					pass
	
	elif "gfycat.com" in c[0] and not c[0].endswith('.webm'):
		
		gfycat_id = c[0].split('/')[-1]
		link = 'http://giant.gfycat.com/{}.webm'.format(gfycat_id)
		finished_links.append(tuple([link, c[1]]))

	else:

		finished_links.append(c)

sys.stdout.write('\n')

current_image = 0

for x in range(len(finished_links)):
	# print(finished_links[x][1])
	for y in range(len(finished_links)):
		if x != y and finished_links[x][1] == finished_links[y][1]:
			print(finished_links[x][1])


try:
	for d in finished_links:
		current_image += 1
		sys.stdout.write('\rDownloading images: [{}/{}][{}][thread_count: {}]'.format(str(current_image), str(len(finished_links)), sub, threading.active_count()))
		sys.stdout.flush()
		a_imgnumber = 0
		a_threads = []
		donelinks = []
		if '/gallery/' in d[0]:

			os.makedirs('static/images/{}/{}'.format(sub, d[1]), exist_ok=True)

			try:
				for x in d[2]['data']['gallery_data']['items']:

					ext = '.jpg'
					
					a_imgnumber += 1
					g = threading.Thread(target=download_image, args=(d[2]['data']['media_metadata'][x['media_id']]['s']['u'].replace('amp;', ''), '{}/{}'.format(d[1], str(a_imgnumber))))
					a_threads.append(g)
					g.start()
			except:
				input('lkdsfjhsGDkflasfdkhjfklasjhdfasflsakdjfhsadflkasjdfhsafdlkasjdfhslk')

		elif '/a/' in d[0]:

			

			html_page = requests.get(d[0] + '/layout/blog')
			if html_page.status_code == 404:
				with open('logs/{}/{}.txt'.format(datetime.now().strftime('%Y-%m-%d'), sub), 'a+') as f:
					f.write(f'[{datetime.now()}][HTML Error 404][{url}]--->[static/images/{sub}/{d[0]}]\n')
				pass
			else:
				
				imglinks = re.findall(r'\.*?{"hash":"([a-zA-Z0-9]+)".*?"ext":"(\.[a-zA-Z0-9]+)".*?', html_page.text)
				print(imglinks)
				
				if len(imglinks) > 1:

					os.makedirs('static/images/{}/{}'.format(sub, d[1]), exist_ok=True)

					for img in imglinks:
						
						a_imgnumber += 1
						g = threading.Thread(target=download_image, args=('https://i.imgur.com/{}{}'.format(img[0], img[1]), '{}/{}'.format(d[1], str(a_imgnumber))))
						a_threads.append(g)
						g.start()
				else:
					os.makedirs('static/images/{}/{}'.format(sub, d[1]), exist_ok=True)
					temp_id = d[0].split('#')[-0]

					a_imgnumber += 1
					g = threading.Thread(target=download_image, args=('https://i.imgur.com/{}{}'.format(temp_id, '.jpg'), '{}/{}'.format(d[1], str(a_imgnumber))))
					a_threads.append(g)
					g.start()


			pass
			
		else:
			ext = os.path.splitext(d[0])[1]
			t = threading.Thread(target=download_image, args=(d[0], d[1]))
			t.start()
			threads.append(t)

		while threading.active_count() >= max_downloads:
			try:
				threads[0].join()
				threads.pop(0)
			except:
				pass
			sys.stdout.write('\rDownloading images: [{}/{}][{}][thread_count: {}]'.format(str(current_image), str(len(finished_links)), sub, threading.active_count()))
			sys.stdout.flush()

	for e in threads:
		e.join()

except KeyboardInterrupt:
	print('\nCtrl-C Pressed; Finishing current threads then stopping...')
	for e in threads:
		e.join()
	sys.exit()


for b in threads:
	b.join()
	sys.stdout.write('\rDownloading images: [{}/{}][{}][thread_count: {}]'.format(str(current_image), str(len(finished_links)), sub, threading.active_count()))
	sys.stdout.flush()

sys.stdout.write('\n')

# print('All done!')