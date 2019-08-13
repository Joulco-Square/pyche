# -*- encoding: utf-8 -*-
"""
 * Copyright (C) Joulco Square PTY LTD - All Rights Reserved
 * Unauthorized copying of this file, via any medium is strictly prohibited
 * Proprietary and confidential
 * Written by Willem Grobler <willem@joulco2.com>, July 2019
 *
"""

import sys
import os
import json
import importlib

class PycheWSGI():
	def __init__(self):
		self.server_config = object()
		self.mod_wsgi_config = object()
		self.python_version = []	

	def load_server_config(self,server_config):
		self.server_config = server_config		
	
	def load_mod_wsgi_config(self,mod_wsgi_config):
		self.mod_wsgi_config = mod_wsgi_config

	def get_app(self):
		AppRootDirectory = self.mod_wsgi_config.AppRootDirectory
		APP_NAME = self.mod_wsgi_config.AppName

		sys.path.insert(0,AppRootDirectory)
		self.app_module = importlib.import_module(APP_NAME)

		application = self.app_module.start_flask_app(self.server_config)		
		return application

	def get_app_no_error(self):
		try:
			application = get_app(self)					
			return [True,application]
		except:
			return [False,object()]

	def get_python_version(self):		
		self.python_version.append(sys.version_info[0])
		self.python_version.append(sys.version_info[1])
		
		if self.python_version[0] == 2:
			print('Using python version 2.x')
		else:
			if self.python_version[1] < 5:
				print('Using python version less than 3.5')
			else:	
				print('Using python greater or equal to 3.5')

class PycheConfig():	
	def __init__(self):
		self.config_files_dir = '/var/www/pyche/config_files/'		
		
		self.config_filename = ''
		self.config_data = {}
		
		self.ServerConfig = self.blank_ServerConfig()
		self.BuildServerConfig()
		
		self.mod_wsgi_config = object()
		self.build_mod_wsgi_config()			

	def change_ConfigFilesDir(self,config_files_dir):
		self.config_files_dir = config_files_dir

	def LoadConfig(self,config_filename):
		self.config_filename = config_filename;
		self._load_config()

	def _load_config(self):
		self.config_file_path = self.config_files_dir + self.config_filename + '.json'		
		with open(self.config_file_path) as json_file:  
			self.config_data = json.load(json_file)
		self.BuildServerConfig()
		self.build_mod_wsgi_config()

	def get_ConfigDataJSON(self):
		return self.config_data		

	class blank_ServerConfig(object):
		isValid = False
		DNSConfig = object()
		ErrorConfig = object()
		WSGIConfig = object()

	class blank_DNSConfig(object):	
		SERVER_NAME = ""
		SERVER_ALIAS = ""		
		SERVER_PROTOCOL = ""		
		SERVER_URL = ""

	class blank_ErrorConfig(object):
		ERROR_LOGLEVEL = ""
		ERROR_ERRORLOG = ""
		ERROR_ACCESSLOG = ""

	class blank_WSGIConfig(object):
		NAME = ""
		SHORTNAME = ""
		DESCRIPTION = ""
		DEFAULT_APP = ""
		FALLBACK_APP = ""
		DEVELOPER = ""

	class blank_mod_wsgi_config(object):
		isValid = False
		AppRootDirectory = '/var/www/pyche'
		AppName = 'MyApp'

	def BuildServerConfig(self):
		self.ServerConfig.DNSConfig = self.blank_DNSConfig()
		self.ServerConfig.ErrorConfig = self.blank_ErrorConfig()
		self.ServerConfig.WSGIConfig = self.blank_WSGIConfig()
		if self.config_data != {}:
			self.ServerConfig.isValid = True
			self.ServerConfig.DNSConfig.SERVER_NAME = self.config_data['ServerConfig']['ServerName']		
			self.ServerConfig.DNSConfig.SERVER_ALIAS = self.config_data['ServerConfig']['ServerAlias']		
			self.ServerConfig.DNSConfig.SERVER_PROTOCOL = self.config_data['ServerConfig']['Protocol']		
			self.ServerConfig.DNSConfig.SERVER_URL = self.ServerConfig.DNSConfig.SERVER_PROTOCOL + '://' + self.ServerConfig.DNSConfig.SERVER_NAME
			
			self.ServerConfig.ErrorConfig.ERROR_LOGLEVEL = self.config_data['ErrorConfig']['LogLevel']
			self.ServerConfig.ErrorConfig.ERROR_ERRORLOG = self.config_data['ErrorConfig']['ErrorLog']
			self.ServerConfig.ErrorConfig.ERROR_ACCESSLOG = self.config_data['ErrorConfig']['AccessLog']
			
			self.ServerConfig.WSGIConfig.NAME = self.config_data['WSGIConfig']['Name']
			self.ServerConfig.WSGIConfig.SHORTNAME = self.config_data['WSGIConfig']['ShortName']
			self.ServerConfig.WSGIConfig.DESCRIPTION = self.config_data['WSGIConfig']['Description']
			self.ServerConfig.WSGIConfig.DEFAULT_APP = self.config_data['WSGIConfig']['Default_App']
			self.ServerConfig.WSGIConfig.FALLBACK_APP = self.config_data['WSGIConfig']['Fallback_App']
			self.ServerConfig.WSGIConfig.DEVELOPER = self.config_data['WSGIConfig']['Developer']
		else:
			self.ServerConfig.isValid = False

	def build_mod_wsgi_config(self):
		self.mod_wsgi_config = self.blank_mod_wsgi_config()
		if self.config_data != {}:
			self.mod_wsgi_config.isValid = True
			self.mod_wsgi_config.AppName = self.config_data['WSGIConfig']['Default_App']
			self.mod_wsgi_config.AppRootDirectory = self.config_data['WSGIConfig']['AppDir']
		else:
			self.mod_wsgi_config.isValid = False

	def get_DNSConfig(self):
		return self.ServerConfig.DNSConfig
	def get_ErrorConfig(self):
		return self.ServerConfig.ErrorConfig
	def get_WSGIConfig(self):
		return self.ServerConfig.WSGIConfig
	def get_ServerConfig(self):
		return self.ServerConfig
	def get_mod_wsgi_config(self):
		return self.mod_wsgi_config








