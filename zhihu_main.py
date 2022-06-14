from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WAIT
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from urllib.request import urlretrieve
from click import password_option
from selenium import webdriver
from re import I
import cv2
import time
import random
import httpx
import os


'''
	模拟浏览器登录知乎
'''
class zhihu_login:
	#初始化
	def __init__(self, username = '0', password = '0'):
		print('          ___           ___                       ___           ___      ')
		print('         /\  \         /\__\          ___        /\__\         /\__\     ')
		print('         \:\  \       /:/  /         /\  \      /:/  /        /:/  /     ')
		print('          \:\  \     /:/__/          \:\  \    /:/__/        /:/  /      ')
		print('           \:\  \   /::\  \ ___      /::\__\  /::\  \ ___   /:/  /  ___  ')
		print('     _______\:\__\ /:/\:\  /\__\  __/:/\/__/ /:/\:\  /\__\ /:/__/  /\__\ ')
		print('     \::::::::/__/ \/__\:\/:/  / /\/:/  /    \/__\:\/:/  / \:\  \ /:/  / ')
		print('      \:\~~\~~          \::/  /  \::/__/          \::/  /   \:\  /:/  /  ')
		print('       \:\  \           /:/  /    \:\__\          /:/  /     \:\/:/  /   ')
		print('        \:\__\         /:/  /      \/__/         /:/  /       \::/  /    ')
		print('         \/__/         \/__/                     \/__/         \/__/     ')
		print('      ___           ___                       ___           ___           ___      ')     
		print('     /\  \         /\  \          ___        /\  \         /\  \         /\  \     ')
		print('    /::\  \       /::\  \        /\  \      /::\  \       /::\  \       /::\  \    ')
		print('   /:/\ \  \     /:/\:\  \       \:\  \    /:/\:\  \     /:/\:\  \     /:/\:\  \   ')
		print('  _\:\~\ \  \   /::\~\:\  \      /::\__\  /:/  \:\__\   /::\~\:\  \   /::\~\:\  \  ')
		print(' /\ \:\ \ \__\ /:/\:\ \:\__\  __/:/\/__/ /:/__/ \:|__| /:/\:\ \:\__\ /:/\:\ \:\__\ ')
		print(' \:\ \:\ \/__/ \/__\:\/:/  / /\/:/  /    \:\  \ /:/  / \:\~\:\ \/__/ \/_|::\/:/  / ')
		print('  \:\ \:\__\        \::/  /  \::/__/      \:\  /:/  /   \:\ \:\__\      |:|::/  /  ')
		print('   \:\/:/  /         \/__/    \:\__\       \:\/:/  /     \:\ \/__/      |:|\/__/   ')
		print('    \::/  /                    \/__/        \::/__/       \:\__\        |:|  |     ')
		print('     \/__/                                   ~~            \/__/         \|__|     ')

		self.username = username		#用户名/手机号
		self.password = password		#密码
		self.followingNum = 0 			#关注人数
		self.followerNum = 0 			#粉丝人数
		
		#selenium driver配置调试模式
		#selenium启动谷歌浏览器
		chrome_options = webdriver.ChromeOptions()
		#开启浏览器debug模式
		#os.system(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\temp"')
		chrome_options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
		#self.chrome_driver = webdriver.Chrome(executable_path = r'C:\Program Files\Google\Chrome\Application\chromedriver.exe', options=chrome_options)
		self.chrome_driver = webdriver.Chrome(options=chrome_options)

		self.wait = WAIT(self.chrome_driver, 3)
		self.url = 'https://www.zhihu.com/'
		self.bg_img_path = 'bg.png'				#滑动验证-背景图片
		self.slider_img_path = './slider.png'	#滑动验证-滑块图片

	#登录入口
	def entry(self):
		print('\n################# LogIn #################')
		self.chrome_driver.get(self.url)
		try:
			if self.wait.until(EC.presence_of_element_located((By.ID, 'Popover15-toggle'))):
				print('[$] Login successful!')
				cookie = self.save_cookie()
				return cookie
		except:
			#切换到密码登录
			self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(@class,"SignFlow-tabs")]/div[2]'))).click()
			#输入用户名
			input_username = self.chrome_driver.find_element(by=By.NAME, value='username')
			input_username.clear()
			input_username.send_keys(self.username)
			#输入密码
			input_password = self.chrome_driver.find_element(by=By.NAME, value='password')
			input_password.clear()
			input_password.send_keys(self.password)
			#点击登录按钮
			self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/main/div/div/div/div/div[1]/div/div[1]/form/button'))).click()
			time.sleep(1)

			#进行滑动验证
			if self.slide_vertify():
				print('[$] Login successful!')
				cookie = self.save_cookie()
				return cookie
			else:
				#最多五次重新登录
				for i in range(4):
					if self.slide_vertify():
						print('[$] Login successful! (tries:%d)' % (i+2))
						cookie = self.save_cookie()
						return cookie
					print('[$] Login falied! (tries:%d)' % (i+2))
				print('[$] Stop login!')
				return

	#滑动验证
	def slide_vertify(self):
		slider_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="yidun_slider"]')))
		#下载并替换 滑动验证-背景图片
		self.bg_img_url = self.wait.until(EC.presence_of_element_located((By.XPATH, '//img[@class="yidun_bg-img"]'))).get_attribute('src')
		urlretrieve(self.bg_img_url, self.bg_img_path)
		#下载并替换 滑动验证-滑块图片
		self.slider_img_url = self.wait.until(EC.presence_of_element_located((By.XPATH, '//img[@class="yidun_jigsaw"]'))).get_attribute('src')
		urlretrieve(self.slider_img_url, self.slider_img_path)
		distance = self.get_distance(self.bg_img_path, self.slider_img_path)
		distance += 10 		#实际移动距离需要向右偏移10px
		tracks = self.get_tracks(distance)
		self.mouse_move(slider_button, tracks)
		try:
			element = self.wait.until(EC.presence_of_element_located((By.ID,'Popover15-toggle')))
		except:
			return False
		else:
			return True

	#保存cookie
	def save_cookie(self):
		cookie = {}
		for item in self.chrome_driver.get_cookies():
			cookie[item['name']] = item['value']
		# print('[$] Get cookie successful!')
		# #输出cookie
		# print('[$] cookies:')
		# for i in cookie:
		# 	print('\t%s:\t%s' % (i, cookie[i]))
		return cookie

	#鼠标滑动
	def mouse_move(self, slide, tracks):
		#鼠标点击滑块并按住不动
		ActionChains(self.chrome_driver).click_and_hold(slide).perform()
		#按轨迹滑动
		for track in tracks:
			ActionChains(self.chrome_driver).move_by_offset(track, 0).perform()
		ActionChains(self.chrome_driver).release(slide).perform()

	#获取滑动距离
	def get_distance(self, bg_img_path='./bg.png', slider_img_path='./slider.png'):
		#滑动验证-背景图片 处理
		bg_img = cv2.imread(bg_img_path, 0)				#读入灰度图片
		bg_img = cv2.GaussianBlur(bg_img, (3, 3), 0)		#高斯模糊去噪
		bg_img = cv2.Canny(bg_img, 50, 150)				#Canny算法进行边缘检测
		#滑动验证-滑块图片 处理
		#同上
		slider_img = cv2.imread(slider_img_path, 0)
		slider_img = cv2.GaussianBlur(slider_img, (3, 3), 0)
		slider_img = cv2.Canny(slider_img, 50, 150)
		#寻找最佳匹配
		res = cv2.matchTemplate(bg_img, slider_img, cv2.TM_CCOEFF_NORMED)
		#最小值，最大值，并得到最小值, 最大值的索引
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		top_left = max_loc[0]		#横坐标
		
		return top_left

	#获取滑动轨迹
	def get_tracks(self, distance):
		tracks = []
		v = 0
		t = 0.2				#单位时间
		current = 0 		#滑块当前位移
		distance += 10 		#多移动10px，然后回退
		while current < distance:
			if current < distance * 5 / 8:
				a = random.randint(1, 3)
			else:
				a = -random.randint(2, 4)
			v0 = v 			#初速度
			track = v0 * t + 0.5 * a * (t ** 2)		#单位时间的滑动距离
			tracks.append(round(track))				#加入轨迹
			current += round(track)
			v = v0 + a * t
		#回退到大致位置
		for i in range(5):
			tracks.append(-random.randint(1, 3))
		
		return tracks

	#########################################################################
	
	#获取基本信息
	def getinfo(self, uid):
		print('\n################# Get Info #################')
		infolist = {}
		url = f'https://www.zhihu.com/people/{uid}'		#目标用户主页url
		print('[$] url:%s' % url)
		self.chrome_driver.get(url)
		try:
			self.chrome_driver.find_element(by=By.XPATH, value='//*[@id="ProfileHeader"]/div/div[2]/div/div[2]/div[3]/button').click()
		except:
			print('[$] pass')
		
		#等待页面加载完成
		time.sleep(3)

		current_window = self.chrome_driver.current_window_handle		#获取当前窗口handle name
		all_window = self.chrome_driver.window_handles 					#返回当前会话中所有窗口的句柄
		#通过遍历判断要切换的窗口
		for window in all_window:
			if window != current_window:
				self.chrome_driver.switch_to.window(window) 			#将定位焦点切换到指定的窗口，包含所有可切换焦点的选项

		#获取用户的各种信息
		#名字
		try:
			username = self.chrome_driver.find_element(by=By.XPATH, value='//*[@id="ProfileHeader"]/div/div[2]/div/div[2]/div[1]/h1/span[1]').get_attribute('innerHTML')
		except:
			username = ""
		infolist['username'] = username
		#介绍
		try:
			introduce = self.chrome_driver.find_element(by=By.XPATH, value='//*[@id="ProfileHeader"]/div/div[2]/div/div[2]/div[1]/h1/span[2]').get_attribute('innerHTML')
		except:
			introduce = ""
		infolist['introduce'] = introduce
		#居住地
		try:
			address = self.chrome_driver.find_element(by=By.XPATH, value='//*[@id="ProfileHeader"]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div').get_attribute('innerHTML')
		except:
			address = ""
		address = address.replace('<span>', '').replace('</span>', '')
		infolist['address'] = address
		#所在行业
		try:
			industry = self.chrome_driver.find_element(by=By.XPATH, value='//*[@id="ProfileHeader"]/div/div[2]/div/div[2]/div[2]/div/div/div[2]/div').get_attribute('innerText')
		except:
			industry = ""
		infolist['industry'] = industry
		#职业经历
		try:
			profession = self.chrome_driver.find_element(by=By.XPATH, value='//*[@id="ProfileHeader"]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/div').get_attribute('innerText')
		except:
			profession = ""
		infolist['profession'] = profession
		#教育经历
		try:
			education = self.chrome_driver.find_element(by=By.XPATH, value='//*[@id="ProfileHeader"]/div/div[2]/div/div[2]/div[2]/div/div/div[4]/div').get_attribute('innerText')
		except:
			education = ""
		infolist['education'] = education
		#个人简介
		try:
			introduce = self.chrome_driver.find_element(by=By.XPATH, value='//*[@id="ProfileHeader"]/div/div[2]/div/div[2]/div[2]/div/div/div[5]/div').get_attribute('innerText')
		except:
			introduce = ""
		infolist['introduce'] = introduce

		#获得关注人数和粉丝人数
		try:
			self.followingNum = int(self.chrome_driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/main/div/div[2]/div[2]/div[3]/div/a[1]/div/strong').get_attribute('title'))
		except:
			try:
				self.followingNum = int(self.chrome_driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/main/div/div[2]/div[2]/div[2]/div/a[1]/div/strong').get_attribute('title'))
			except:
				self.followingNum = int(self.chrome_driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/main/div/div[2]/div[2]/div[1]/div/a[1]/div/strong').get_attribute('title'))
		#粉丝人数
		try:
			self.followerNum = int(self.chrome_driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/main/div/div[2]/div[2]/div[3]/div/a[2]/div/strong').get_attribute('title'))
		except:
			try:
				self.followerNum = int(self.chrome_driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/main/div/div[2]/div[2]/div[2]/div/a[2]/div/strong').get_attribute('title'))
			except:
				self.followerNum = int(self.chrome_driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/main/div/div[2]/div[2]/div[1]/div/a[2]/div/strong').get_attribute('title'))

		#输出信息
		print('[$] Basic Information:')
		for i in infolist:
			print('\t%s:\t%s' % (i, infolist[i].replace('\n', '; ')))
		print('\tfollowingNum:\t%d' % self.followingNum)
		print('\tfollowerNum:\t%d' % self.followerNum)

		return infolist

	#获取关注人信息
	def getfollowings(self, uid, pnum, num=10):
		print('\n################# Get Followings #################')
		url = f'https://www.zhihu.com/people/{uid}'
		print('[$] url:%s' % url)
		self.chrome_driver.get(url)
		followingslist = []

		#pnum为页数，遍历所有页面
		for pid in range(1, pnum + 1):
			url = f'https://www.zhihu.com/people/{uid}/following/?page={pid}'
			print('[$] url:%s' % url)
			self.chrome_driver.get(url)
			
			#等待页面加载完成
			time.sleep(3)

			self.drop_scroll()
			self.switch_window_back()
			if int(self.followingNum) < 10:
				num = int(self.followingNum)
			elif int(self.followingNum) == 0:
				return followingslist

			for i in range(0, num):
				following = {}
				#获取following信息
				xpath1 = f'/html/body/div[1]/div/main/div/div[2]/div[1]/div/div[3]/div/div[2]/div[{i+1}]/div/div/div[2]/h2/span/div/span/div/div/a' 
				xpath2 = f'/html/body/div[1]/div/main/div/div[2]/div[1]/div/div[3]/div/div[2]/div[{i+1}]/div/div/div[2]/div/div/div[2]'
				following_name = self.chrome_driver.find_element(by=By.XPATH, value=xpath1).get_attribute('innerText')
				following['following_name'] = following_name
				following_ID = self.chrome_driver.find_element(by=By.XPATH, value=xpath1).get_attribute('href').split('/')[-1]
				following['following_ID'] = following_ID
				try:
					following_info = self.chrome_driver.find_element(by=By.XPATH, value=xpath2).get_attribute('innerText')
					following_info = following_info.replace('回答', '回答; ')
					following_info = following_info.replace('文章', '文章; ')
					following['following_info'] = following_info
				except:
					following_info = ''
					following['following_info'] = following_info
				followingslist.append(following)
		#输出信息
		l = 1
		print('[$] Top10 Followings Information:')
		for i in followingslist:
			print('\tNo_%d:' % l)
			l += 1
			for k in i:
				print('\t\t%s:%s' % (k, i[k]))

		return followingslist

	# #获取粉丝信息
	def getfollowers(self, uid, pnum, num=10):
		print('\n################# Get Followers #################')
		url = f'https://www.zhihu.com/people/{uid}'
		print('[$] url:%s' % url)
		self.chrome_driver.get(url)
		followerslist = []

		#pnum为页数，遍历所有页面
		for pid in range(1, pnum + 1):
			url = f'https://www.zhihu.com/people/{uid}/followers/?page={pid}'
			print('[$] url:%s' % url)
			self.chrome_driver.get(url)

			#等待页面加载完成
			time.sleep(3)

			self.drop_scroll()
			self.switch_window_back()
			if int(self.followerNum) < 10:
				num = int(self.followerNum)
			elif int(self.followerNum) == 0:
				return followerslist

			for i in range(0,num):
				follower = {}
				#获取follower信息
				xpath1 = f'/html/body/div[1]/div/main/div/div[2]/div[1]/div/div[3]/div/div[2]/div[{i+1}]/div/div/div[2]/h2/span/div/span/div/div/a' 
				xpath2 = f'/html/body/div[1]/div/main/div/div[2]/div[1]/div/div[3]/div/div[2]/div[{i+1}]/div/div/div[2]/div/div/div'    
				follower_name = self.chrome_driver.find_element(by=By.XPATH, value=xpath1).get_attribute('innerText')
				follower['follower_name'] = follower_name
				follower_ID = self.chrome_driver.find_element(by=By.XPATH, value=xpath1).get_attribute('href').split('/')[-1]
				follower['follower_ID'] = follower_ID
				try:
					follower_info = self.chrome_driver.find_element(by=By.XPATH, value=xpath2).get_attribute('innerText')
					follower_info = follower_info.replace('回答', '回答; ')
					follower['follower_info'] = follower_info
				except:
					follower_info = ''
					follower['follower_info'] = follower_info
				followerslist.append(follower)
		#输出信息
		l = 0
		print('[$] Top10 Followers Information:')
		for i in followerslist:
			print('\tNo_%d:' % l)
			l += 1
			for k in i:
				print('\t\t%s:%s' % (k, i[k]))

		return followerslist
	
	#获取动态信息
	def getactivities(self, uid):
		print('\n################# Get Activities #################')
		url = f'https://www.zhihu.com/people/{uid}/answers'
		print('[$] url:%s' % url)
		self.chrome_driver.get(url)
		answerlist = []
		commentlist = []

		#等待页面加载完成
		time.sleep(3)
		
		self.drop_scroll()
		self.switch_window_back()

		#获取回答数
		answers_num = int(self.chrome_driver.find_element(by=By.XPATH, value='//*[@id="ProfileMain"]/div[1]/ul/li[2]/a/span').get_attribute('innerText').replace(',', ''))
		print('[$] answers num：%d' % answers_num)
		if answers_num > 10:
			num = 10
		else:
			num = answers_num
		#回答前十条
		print('[$] Top10 Answers:')
		for i in range(num):
			print('[$] No.%d' % int(i+1))
			data1, data2 = self.answer(i+1)
			answerlist.append(data1)
			commentlist.append(data2)

		return answerlist, commentlist
		print(answerlist)
		print(commentlist)

	#回答
	def answer(self, num):
		answers = {}

		button_test = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ProfileMain"]/div[1]/ul/li[2]/a')))
		ActionChains(self.chrome_driver).click(button_test).perform()

		#打开评论区
		try:
			button_comment = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="Profile-answers"]/div[2]/div[{num}]/div/div/div[2]/div[2]/button[1]')))
			ActionChains(self.chrome_driver).click(button_comment).perform()
		except:
			try:
				button_comment = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="Profile-answers"]/div[2]/div[{num}]/div/div/div[2]/div[3]/button[1]')))
				ActionChains(self.chrome_driver).click(button_comment).perform()
			except:
				button_comment = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="Profile-answers"]/div[2]/div[{num}]/div/div/div[2]/div[3]/div/button[1]')))
				ActionChains(self.chrome_driver).click(button_comment).perform()
		#阅读全文
		try:
			button_all = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="Profile-answers"]/div[2]/div[{num}]/div/div/div[2]/div[1]/button')))
			ActionChains(self.chrome_driver).click(button_all).perform()
		except:
			try:
				button_all_ = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="Profile-answers"]/div[2]/div[{num}]/div/div/div[2]/div[2]/button')))
				ActionChains(self.chrome_driver).click(button_all_).perform()
			except:
				time.sleep(1)
		time.sleep(1)

		#发帖时间
		try:
			xpath1 = f'//*[@id="Profile-answers"]/div[2]/div[{num}]/div/div/div[2]/div[2]/div/a/span'
			answers_time = self.chrome_driver.find_element(by=By.XPATH, value=xpath1).get_attribute('innerText')
			answers['time'] = answers_time[4:]
		except:
			xpath1_ = f'//*[@id="Profile-answers"]/div[2]/div[{num}]/div/div/div[2]/div[2]/div[2]/a/span'
			answers_time = self.chrome_driver.find_element(by=By.XPATH, value=xpath1_).get_attribute('innerText')
			answers['time'] = answers_time[4:]
		
		#发帖内容
		try:
			xpath2 = f'//*[@id="Profile-answers"]/div[2]/div[{num}]/div/div/div[2]/div[1]/span'
			answers_content = self.chrome_driver.find_element(by=By.XPATH, value=xpath2).get_attribute('innerText').replace('\u200b', '').replace('\n', ' ')
			answers['content'] = answers_content
		except:
			answers_content = ""
			answers['content'] = answers_content
		
		#点赞次数
		try:
			xpath3 = f'//*[@id="Profile-answers"]/div[2]/div[{num}]/div/div/div[2]/div[3]'
			answers_agree = self.chrome_driver.find_element(by=By.XPATH, value=xpath3).get_attribute('innerText').replace('\u200b', '').replace('\n', ' ').split(' ')
			answers['agree'] = answers_agree[2]
		except:
			answers_agree = ['0']
			answers['agree'] = answers_agree
		if answers['agree'] == '':
			answers['agree'] = '0'

		#评论次数
		try:
			xpath4 = f'//*[@id="Profile-answers"]/div[2]/div[{num}]/div/div/div[3]/div/div[1]/div[1]/h2'
			answers_com = self.chrome_driver.find_element(by=By.XPATH, value=xpath4).get_attribute('innerText').split(' ')
			answers['commentnum'] = answers_com[0]
		except:
			answers_com = ['error']
			answers['commentnum'] = answers_com[0]
				
		for i in answers:
			print('\t%s:%s' % (i, answers[i]))

		num_com = 10
		if answers_com[0] == '还没有评论' or answers_com[0] == 'error':
			return
		elif num_com > int(answers_com[0]):
			num_com = int(answers_com[0])
		
		comments = self.answers_comment(num, num_com)

		return answers, comments
		
	def answers_comment(self, num, num_com):
		#前十条评论
		comments_all = []
		for i in range(num_com):
			comments = {}
			#评论人ID、评论人昵称
			try:
				xpath = f'//*[@id="Profile-answers"]/div[2]/div[{num}]/div/div/div[3]/div/div[2]/div[1]/ul[{i+1}]/li/div/div/div[1]/span[2]/a'
				ID = self.chrome_driver.find_element(by=By.XPATH, value=xpath).get_attribute('href').split('/')[-1]
				name = self.chrome_driver.find_element(by=By.XPATH, value=xpath).get_attribute('innerText')
				comments['ID'] = ID
				comments['name'] = name
			except:
				try:
					xpath_ = f'//*[@id="Profile-answers"]/div[2]/div[{num}]/div/div/div[3]/div/div[2]/div[1]/ul[{i+1}]/li[1]/div/div/div[1]/span[2]/a'
					ID = self.chrome_driver.find_element(by=By.XPATH, value=xpath_).get_attribute('href').split('/')[-1]
					name = self.chrome_driver.find_element(by=By.XPATH, value=xpath_).get_attribute('innerText')
					comments['ID'] = ID
					comments['name'] = name
				except:
					try:
						xpath = f'//*[@id="Profile-answers"]/div[2]/div[{num}]/div/div/div[3]/div/div[2]/div/ul/li/div/div/div[1]/span[2]/a'
						ID = self.chrome_driver.find_element(by=By.XPATH, value=xpath_).get_attribute('href').split('/')[-1]
						name = self.chrome_driver.find_element(by=By.XPATH, value=xpath_).get_attribute('innerText')
						comments['ID'] = ID
						comments['name'] = name
					except:
						try:
							xpath = f'//*[@id="Profile-answers"]/div[2]/div[{num}]/div/div/div[3]/div/div[2]/div/ul[{i+1}]/li/div/div/div[1]/span[2]/a'
							ID = self.chrome_driver.find_element(by=By.XPATH, value=xpath_).get_attribute('href').split('/')[-1]
							name = self.chrome_driver.find_element(by=By.XPATH, value=xpath_).get_attribute('innerText')
							comments['ID'] = ID
							comments['name'] = name
						except:
							try:
								xpath = f'//*[@id="Profile-answers"]/div[2]/div[{num}]/div/div/div[3]/div/div[2]/div/ul[{i+1}]/li[1]/div/div/div[1]/span[2]/a'
								ID = self.chrome_driver.find_element(by=By.XPATH, value=xpath_).get_attribute('href').split('/')[-1]
								name = self.chrome_driver.find_element(by=By.XPATH, value=xpath_).get_attribute('innerText')
								comments['ID'] = ID
								comments['name'] = name
							except:
								time.sleep(1)
			
			#评论时间
			try:
				xpath1 = f'//*[@id="Profile-answers"]/div[2]/div[{num}]/div/div/div[3]/div/div[2]/div/ul[{i+1}]/li[1]/div/div/div[1]/span[3]'
				stime = self.chrome_driver.find_element(by=By.XPATH, value=xpath1).get_attribute('innerText')
				comments['time'] = stime
			except:
				try:
					xpath1_ = f'//*[@id="Profile-answers"]/div[2]/div[{num}]/div/div/div[3]/div/div[2]/div/ul[{i+1}]/li/div/div/div[1]/span[3]'
					stime = self.chrome_driver.find_element(by=By.XPATH, value=xpath1_).get_attribute('innerText')
					comments['time'] = stime
				except:
					time.sleep(1)

			#评论内容
			try:
				xpath2 = f'//*[@id="Profile-answers"]/div[2]/div[{num}]/div/div/div[3]/div/div[2]/div/ul[{i+1}]/li[1]/div/div/div[2]/div[1]/div'
				content = self.chrome_driver.find_element(by=By.XPATH, value=xpath2).get_attribute('innerText').replace('\n', ' ')
				comments['conten'] = content
			except:
				try:
					xpath2_ = f'//*[@id="Profile-answers"]/div[2]/div[{num}]/div/div/div[3]/div/div[2]/div/ul[{i+1}]/li/div/div/div[2]/div[1]/div'
					content = self.chrome_driver.find_element(by=By.XPATH, value=xpath2_).get_attribute('innerText').replace('\n', ' ')
					comments['conten'] = content
				except:
					time.sleep(1)

			#点赞次数
			try:
				xpath3 = f'//*[@id="Profile-answers"]/div[2]/div[{num}]/div/div/div[3]/div/div[2]/div/ul[{i+1}]/li[1]/div/div/div[2]/div[2]'
				agree = self.chrome_driver.find_element(by=By.XPATH, value=xpath3).get_attribute('innerText').replace('\u200b', '').split('\n')[1]
				comments['agree'] = agree
			except:
				try:
					xpath3_ = f'//*[@id="Profile-answers"]/div[2]/div[{num}]/div/div/div[3]/div/div[2]/div/ul[{i+1}]/li/div/div/div[2]/div[2]'
					agree = self.chrome_driver.find_element(by=By.XPATH, value=xpath3_).get_attribute('innerText').replace('\u200b', '').split('\n')[1]
					comments['agree'] = agree
				except:
					time.sleep(1)
	
			if comments != {}:
				comments_all.append(comments)
		t = 1
		for i in comments_all:
			print('\tNo_%d:' % t)
			t += 1
			for k in i:
				print('\t\t%s:%s' % (k, i[k]))
		print('\treal_get_comment:%d' % (t-1))

		return comments_all

	#将浏览器的指令移回到新标签页
	def switch_window_back(self):
		windows = self.chrome_driver.window_handles
		self.chrome_driver.switch_to.window(windows[0])

	#滑条拖到底，加载全部信息
	def drop_scroll(self):
		for x in range(1, 11, 2):
			j = x / 10
			js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight * %f' % j
			self.chrome_driver.execute_script(js) 

	#关闭浏览器
	def close(self):
		self.chrome_driver.close()

#test
if __name__ == '__main__':
	os.popen('chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\temp"')
	spider = zhihu_login('', '')
	#name = 'tombkeeper'		#CTF
	name = 'wu-lin-guang-3'		#世纪佳缘CEO
	spider.entry()
	spider.getinfo(name)
	spider.getfollowings(name, 1, 10)
	spider.getfollowers(name, 1, 10)
	spider.getactivities(name)
	spider.close()