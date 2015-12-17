# -*- coding:utf-8 -*-
__author__ = 'phenix'

import MySQLdb
import ConfigParser
import csv
import sys

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
	reload(sys)
	sys.setdefaultencoding(default_encoding)


class MySQLTools(object):
	def __init__(self, config_file_path):
		config = ConfigParser.ConfigParser()
		config.read(config_file_path)
		db_host = config.get("db", "db_host")
		db_port = config.getint("db", "db_port")
		db_user = config.get("db", "db_user")
		db_password = config.get("db", "db_password")
		db_name = config.get("db", "db_name")
		db_charset = config.get("db", "db_charset")
		self.conn = MySQLdb.connect(host=db_host, port=db_port, user=db_user, passwd=db_password, db=db_name,
									charset=db_charset)
		self.cursor = self.conn.cursor()

	def query(self, sql):
		self.cursor.execute(sql)
		return self.cursor.fetchall()

	def insert(self, sql):
		self.cursor.execute(sql)
		self.conn.commit()

	def update(self, sql):
		self.cursor.execute(sql)
		self.conn.commit()

	def close_connect(self):
		self.conn.close()


