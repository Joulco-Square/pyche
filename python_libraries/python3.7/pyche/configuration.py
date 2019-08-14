# -*- encoding: utf-8 -*-
"""
 * Copyright (C) Joulco Square PTY LTD - All Rights Reserved
 * Unauthorized copying of this file, via any medium is strictly prohibited
 * Proprietary and confidential
 * Written by Willem Grobler <willem@joulco2.com>, July 2019
 *
"""

import os
import json,logging

def ReadJSONFile(FileName):
	with open(FileName) as f:
		JSONFile = json.load(f)
	return JSONFile

class _Flask(object):
	DATABASE_HOST = ''
	DATABASE_DB = ''
	DATABASE_USER = ''
	DATABASE_PASSWD = ''	
	DEBUG = ''
	TESTING = ''
	SECRET_KEY = ''		
	NAME = ''
	SHORTNAME = ''
	DESCRIPTION = ''

class _Database(object):
	HOST = ''
	DB = ''
	USER = ''
	PASSWD = ''
	isSet = False

class _Custom(object):
	Data = {}

class ConfigLoader:
	def __init__(self):
		self.Base = {}
		self.Flask = _Flask()
		self.Database = _Database()
		self.Custom = _Custom()
		
		self.app_dir = ''
		
		self.ERROR = False		
		
	def SetAppDir(self,app_dir):
		self.app_dir = app_dir
		
	def LoadConfig(self):
		ConfigFilePath_ThisServerJSON = self.app_dir + '/ThisServerConfig.json'
		ConfigFilePath_ServerJSON = self.app_dir + '/ServerConfig.json'
		ConfigFilePath_ThisAppJSON = self.app_dir + '/ThisAppConfig.json'
		ConfigFilePath_AppJSON = self.app_dir + '/AppConfig.json'
	
		if os.path.isfile(ConfigFilePath_ThisServerJSON):
			ConfigJSON_Server = ReadJSONFile(ConfigFilePath_ThisServerJSON)
			print(' * Custom Server config loaded for app ')
		elif os.path.isfile(ConfigFilePath_ServerJSON):
			ConfigJSON_Server = ReadJSONFile(ConfigFilePath_ServerJSON)
			print(' * Default server config loaded for app')
		else:
			self.ERROR = True
			
		if os.path.isfile(ConfigFilePath_ThisAppJSON):
			print(' * Custom App config loaded for app ')
			ConfigJSON_App = ReadJSONFile(ConfigFilePath_ThisAppJSON)
		elif os.path.isfile(ConfigFilePath_AppJSON):
			ConfigJSON_App = ReadJSONFile(ConfigFilePath_AppJSON)
			print(' * Default App config loaded for app')
		else:
			self.ERROR = True

		if not self.ERROR:			
			self.Flask.DEBUG = ConfigJSON_Server['FlaskConfig']['Debug']
			self.Flask.TESTING = ConfigJSON_Server['FlaskConfig']['Testing']
			self.Flask.SECRET_KEY = ConfigJSON_Server['FlaskConfig']['SecretKey']
			
			#LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
			#LOGGING_LOCATION = Base.DIR_WSGI + '/logs/app.log'
			#LOGGING_LEVEL = logging.DEBUG
			
			self.Flask.NAME = ConfigJSON_App['FlaskConfig']['Name']
			self.Flask.SHORTNAME = ConfigJSON_App['FlaskConfig']['ShortName']
			self.Flask.DESCRIPTION = ConfigJSON_App['FlaskConfig']['Description']

			if 'DatabaseConfig' in ConfigJSON_Server:
				self.Flask.DATABASE_HOST = ConfigJSON_Server['DatabaseConfig'][0]['Host']
				self.Flask.DATABASE_DB = ConfigJSON_Server['DatabaseConfig'][0]['Database']
				self.Flask.DATABASE_USER = ConfigJSON_Server['DatabaseConfig'][0]['User']
				self.Flask.DATABASE_PASSWD = ConfigJSON_Server['DatabaseConfig'][0]['Password']
				self.Database.HOST = ConfigJSON_Server['DatabaseConfig'][0]['Host']
				self.Database.DB = ConfigJSON_Server['DatabaseConfig'][0]['Database']
				self.Database.USER = ConfigJSON_Server['DatabaseConfig'][0]['User']
				self.Database.PASSWD = ConfigJSON_Server['DatabaseConfig'][0]['Password']
				self.Database.isSet = True
			else:
				self.Database.HOST = ''
				self.Database.DB = ''
				self.Database.USER = ''
				self.Database.PASSWD = ''
				self.Database.isSet = False
				
			if 'Custom' in ConfigJSON_App:
				for item in ConfigJSON_App['Custom']:
					self.Custom.Data[item] = ConfigJSON_App['Custom'][item]















