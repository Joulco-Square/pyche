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

class Base(object):
	def ReadJSONFile(FileName):
		with open(FileName) as f:
			JSONFile = json.load(f)
		return JSONFile

	ERROR = False
	ConfigJSON_App = {}
	ConfigJSON_Server = {}

	DIR_CONFIG = os.path.dirname(os.path.realpath(__file__))	
	DIR_APP =  os.path.dirname(DIR_CONFIG)
	
	ConfigFilePath_ThisServerJSON = DIR_APP + '/ThisServerConfig.json'
	ConfigFilePath_ServerJSON = DIR_APP + '/ServerConfig.json'
	ConfigFilePath_AppJSON = DIR_APP + '/AppConfig.json'

	if os.path.isfile(ConfigFilePath_ThisServerJSON):
		ConfigJSON_Server = ReadJSONFile(ConfigFilePath_ThisServerJSON)
		print(' * Custom Server config loaded for app ')
	elif os.path.isfile(ConfigFilePath_ServerJSON):
		ConfigJSON_Server = ReadJSONFile(ConfigFilePath_ServerJSON)
		print(' * Default server config loaded for app')
	else:
		ERROR = True
		
	if os.path.isfile(ConfigFilePath_AppJSON):
		ConfigJSON_App = ReadJSONFile(ConfigFilePath_AppJSON)
	else:
		ERROR = True

class Flask(Base):
	if Base.ERROR == False:
		DATABASE_HOST = Base.ConfigJSON_Server['DatabaseConfig'][0]['Host']
		DATABASE_DB = Base.ConfigJSON_Server['DatabaseConfig'][0]['Database']
		DATABASE_USER = Base.ConfigJSON_Server['DatabaseConfig'][0]['User']
		DATABASE_PASSWD = Base.ConfigJSON_Server['DatabaseConfig'][0]['Password']
		
		DEBUG = Base.ConfigJSON_Server['FlaskConfig']['Debug']
		TESTING = Base.ConfigJSON_Server['FlaskConfig']['Testing']
		SECRET_KEY = Base.ConfigJSON_Server['FlaskConfig']['SecretKey']
		
		#LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
		#LOGGING_LOCATION = Base.DIR_WSGI + '/logs/app.log'
		#LOGGING_LEVEL = logging.DEBUG
		
		NAME = Base.ConfigJSON_App['FlaskConfig']['Name']
		SHORTNAME = Base.ConfigJSON_App['FlaskConfig']['ShortName']
		DESCRIPTION = Base.ConfigJSON_App['FlaskConfig']['Description']

class Database(object):
	if Base.ERROR == False:
		HOST = Base.ConfigJSON_Server['DatabaseConfig'][0]['Host']
		DB = Base.ConfigJSON_Server['DatabaseConfig'][0]['Database']
		USER = Base.ConfigJSON_Server['DatabaseConfig'][0]['User']
		PASSWD = Base.ConfigJSON_Server['DatabaseConfig'][0]['Password']
		
class Custom(object):
	Data = {}
	if Base.ERROR == False:
		if 'Custom' in Base.ConfigJSON_App:
			for item in Base.ConfigJSON_App['Custom']:
				Data[item] = Base.ConfigJSON_App['Custom'][item]















