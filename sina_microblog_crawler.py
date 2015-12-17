#!/usr/bin/python
# -*-coding:utf8-*-
__author__ = 'phenix'

from microblogpy.auth import OAuthHandler
from microblogpy.api import API
from microblogpy.binder import bind_api
from microblogpy.error import microblogpError
import threading
import thread
import microblogpy.mysql_db as mysql
import time
import os
import logging.config
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
	reload(sys)
	sys.setdefaultencoding(default_encoding)


class SinaMicroblogCrawler():
	"""
	爬取sina微博数据
	"""

	def __init__(self, consumer_key, consumer_secret):
		self.consumer_key, self.consumer_secret = consumer_key, consumer_secret

	def getAtt(self, key):
		try:
			return self.obj.__getattribute__(key)
		except Exception, e:
			print e
			return ''

	def getAttValue(self, obj, key):
		try:
			return obj.__getattribute__(key)
		except Exception, e:
			print e
			return ''

	def auth(self):
		"""
		用于获取sina微博  access_token 和access_secret
		"""
		if len(self.consumer_key) == 0:
			print "Please set consumer_key"
			return
		
		if len(self.consumer_key) == 0:
			print "Please set consumer_secret"
			return
		
		self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
		auth_url = self.auth.get_authorization_url()
		print 'Please authorize: ' + auth_url
		verifier = raw_input('PIN: ').strip()
		self.auth.get_access_token(verifier)
		self.api = API(self.auth)
		

	def setToken(self, token, tokenSecret):
		"""
		通过oauth协议以便能获取sina微博数据
		"""
		self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
		self.auth.setToken(token, tokenSecret)
		self.api = API(self.auth)

	def get_userprofile(self, id):
		"""
		获取用户基本信息,全部以字符串存储
		"""
		global ids_num
		try:
			user = self.api.get_user(id)
		except BaseException as e:
			log.error('Error occured when access userprofile user_id:{0} - Error:{1}'.format(id, e))
			if str(e).find('401') > 0 or str(e).find('403') > 0:
				time.sleep(1800)
			return None
		try:
			self.obj = user
			uid = '\'' + id + '\''
			screen_name = '\'' + self.getAtt("screen_name") + '\''
			name = '\'' + self.getAtt("name") + '\''

			province = self.getAtt("province")
			city = self.getAtt("city")

			location = '\'' + self.getAtt("location") + '\''
			description = '\'' + self.getAtt("description") + '\''
			url = '\'' + self.getAtt("url") + '\''
			profile_image_url = '\'' + self.getAtt("profile_image_url") + '\''
			domain = '\'' + self.getAtt("domain") + '\''
			gender = '\'' + self.getAtt("gender") + '\''

			followers_count = str(self.getAtt("followers_count"))
			friends_count = str(self.getAtt("friends_count"))
			statuses_count = str(self.getAtt("statuses_count"))
			favourites_count = str(self.getAtt("favourites_count"))

			created_at = '\'' + str(self.getAtt("created_at")) + '\''
			allow_all_act_msg = '\'' + str(self.getAtt("allow_all_act_msg")) + '\''
			geo_enabled = '\'' + str(self.getAtt("geo_enabled")) + '\''
			verified = '\'' + str(self.getAtt("verified")) + '\''
			sql = 'insert into users values(' + \
				uid + ',' + \
				screen_name + ',' + \
				name + ',' + \
				province + ',' + \
				city + ',' + \
				location + ',' + \
				description + ',' + \
				url + ',' + \
				profile_image_url + ',' + \
				domain + ',' + \
				gender + ',' + \
				followers_count + ',' + \
				friends_count + ',' + \
				statuses_count + ',' + \
				favourites_count + ',' + \
				created_at + ',' + \
				allow_all_act_msg + ',' + \
				geo_enabled + ',' + \
				verified + ')'
		except:
			log.error('Error occured when get a user insert sqlString')
			return None
		mutex.acquire()
		try:
			db.insert(sql)
			ids_num += 1
			self.get_status(max_user_num)
			mutex.release()
		except BaseException as e:
			mutex.release()
			log.error('Error occured when insert userprofile user_id:{0} - Error:{1}'.format(id, e))
			return None
		return 'get successfully'

	def get_latest_microblog(self, user_id, count):
		"""
		获取用户最新发表的count条数据
		"""
		try:
			timeline = self.api.user_timeline(count=count, user_id=user_id, feature=1)
		except Exception as e:
			log.error("Error occured when access status use user_id:{0} - Error:{1}".format(user_id, e))
			# print threading.currentThread(), e
			return None
		for line in timeline:
			try:
				self.obj = line
				mid = self.getAtt("mid")
				created_at = self.getAtt("created_at")
				text = self.getAtt("text")
				source = self.getAtt("source")
				uid = user_id
				sql = 'INSERT INTO microblog VALUES (' + \
					'\'' + str(mid) + '\'' + ',' + \
					'\'' + str(created_at) + '\'' + ',' + \
					'\'' + text + '\'' + ',' + \
					'\'' + source + '\'' + ',' + \
					'\'' + str(uid) + '\'' + ')'
			except:
				log.error('Error occured when get a microblog insert sqlString')
			mutex.acquire()
			try:
				db.cursor.execute('SET NAMES utf8mb4')
				db.insert(sql)
				mutex.release()
			except:
				mutex.release()
				log.info(str(mid) + '\t' + str(created_at) + '\t' + str(text) + '\t' + str(source) + '\t' + str(uid))
				continue
		return 'get successfully'

	def friends_ids(self, id):
		"""
		获取用户关注列表id
		"""
		next_cursor, cursor = 1, 0
		ids = []
		while(0 != next_cursor):
			try:
				fids = self.api.friends_ids(user_id=id, cursor=cursor)
			except BaseException as e:
				log.error("Error occured in reptile id:{0} - Error:{1}".format(id, e))
				return ids
			self.obj = fids
			ids.extend(self.getAtt("ids"))
			cursor = next_cursor = self.getAtt("next_cursor")
		return ids

	def get_status(self, max_user_num):
		if max_user_num > 1000:
			a = max_user_num / 1000
		else:
			a = max_user_num / 10
		if ids_num % a == 0:
			f = ids_num / (max_user_num * 1.0)
			print(format(f, '.2%'))
	
	def manage_access(self):
		"""
		管理应用访问API速度,适时进行沉睡
		"""
		info = self.api.rate_limit_status()
		self.obj = info
		sleep_time = round((float)(self.getAtt("reset_time_in_seconds"))/self.getAtt("remaining_hits"), 2) \
		if self.getAtt("remaining_hits") else self.getAtt("reset_time_in_seconds")
		print self.getAtt("remaining_hits"), self.getAtt("reset_time_in_seconds"), self.getAtt("hourly_limit"), self.getAtt("reset_time")
		print "sleep time:", sleep_time, 'pid:', os.getpid()
		time.sleep(sleep_time + 1.5)


def reptile(SinaMicroblogCrawler):
	global need_view_users
	global viewed_users
	while need_view_users:
		mutex.acquire()
		try:
			id = need_view_users.pop()
			if str(id) in viewed_users:
				continue
			else:
				viewed_users[str(id)] = 1
		except:
			mutex.release()
			raise Exception('user id get error')
		mutex.release()
		SinaMicroblogCrawler.manage_access()
		return_ids = SinaMicroblogCrawler.friends_ids(str(id))
		need_view_users.extend(return_ids)
		user_profile = SinaMicroblogCrawler.get_userprofile(str(id))
		if user_profile is None:
			continue
		SinaMicroblogCrawler.get_latest_microblog(count=100, user_id=str(id))
		if ids_num > max_user_num:
			thread.exit()


def get_connection_2_mysql(config_file):
	return mysql.MySQLTools(config_file)


def get_need_view_users():
	need_view_users = []
	sql = 'SELECT uid FROM sinauser'
	result = db.query(sql)
	for row in range(500):
		need_view_users.append(result[row][0])
	return need_view_users


def get_viewed_users():
	viewed_users = {}
	sql = 'SELECT uid FROM users'
	result = db.query(sql)
	for row in result:
		viewed_users[row[0]] = 1
	return viewed_users


def run_crawler(consumer_key, consumer_secret, key, secret):
	try:
		print threading.currentThread().name, 'start'
		SinaMicroblogCrawler = SinaMicroblogCrawler(consumer_key, consumer_secret)
		SinaMicroblogCrawler.setToken(key, secret)
		reptile(SinaMicroblogCrawler)
	except Exception as e:
		log.error("Error occured in run_crawler tid:{0} - Error:{1}".format(threading.currentThread().name, e))
		raise Exception(threading.currentThread().name + 'end')


if __name__ == "__main__":
	logging.config.fileConfig("logging.conf")
	log = logging.getLogger('logger_SinaMicroblogCrawler')
	db = get_connection_2_mysql('mysql.ini')
	need_view_users = get_need_view_users()
	viewed_users = get_viewed_users()
	ids_num = len(viewed_users)
	max_user_num = 10000000
	threads = []
	# 实例化所有线程
	with open('appkey_test.txt') as f:
		for i in f.readlines():
			j = i.strip().split('\t')
			t = threading.Thread(target=run_crawler, args=(j[0], j[1], j[2], j[3]))
			threads.append(t)
	mutex = threading.RLock()
	# 开始所有线程
	for t in threads:
		t.start()
	# 等待所有结束线程
	for t in threads:
		t.join()
	db.close_connect()
