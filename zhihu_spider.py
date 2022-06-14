from zhihu_main import zhihu_login

from flask_cors import *
from flask import Flask,render_template,request,Response,redirect,url_for
from calendar import c
from tokenize import cookie_re
from click import password_option
import json
import os

#构造函数
app = Flask(__name__)

username = ''
password = ''

#index.html
@app.route('/', methods=['GET','POST'])
def index():
	if request.method == 'POST':
		global username, password
		username = request.form['username']
		password = request.form['password']
		os.popen('chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\temp"')  # 调用cmd命令窗口启动浏览器 
		global spider
		global cookie
		spider = zhihu_login(username, password)
		cookie = spider.entry()
		return redirect(url_for('success'))
	return render_template('index.html')

@app.route('/success')
def success():
	return render_template('success.html', login_cookie=cookie.items())

@app.route('/search', methods=['GET','POST'])
def search():
	if request.method == 'POST':
		name = request.form['name']
		global spider
		spider = zhihu_login(username, password)
		infolist = spider.getinfo(name)
		followingslist = spider.getfollowings(name, 1, 10)
		followerslist = spider.getfollowers(name, 1, 10)
		answerlist, commentlist = spider.getactivities(name)
		lists = zip(answerlist, commentlist)
		return render_template('result.html', entries1 = infolist, entries2 = followingslist, entries3 = followerslist, entries4 = lists)#entries4 = answerlist, entries5 = commentlist)
	return render_template('search.html')

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

if __name__ == "__main__":
	#初始化,设置ip,debug=True可调试模式
	app.run(host='127.0.0.1', port=5000, debug=True)
	CORS(app, supports_credentials=True) #实现前后端分离