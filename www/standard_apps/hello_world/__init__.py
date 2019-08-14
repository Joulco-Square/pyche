# -*- encoding: utf-8 -*-
"""
 * Copyright (C) Joulco Square PTY LTD - All Rights Reserved
 * Unauthorized copying of this file, via any medium is strictly prohibited
 * Proprietary and confidential
 * Written by Willem Grobler <willem@joulco2.com>, July 2019
 *
"""
# Standard Modules Required
#------------------------------------------------------------------------------
from flask import Flask
from flask_cors import CORS, cross_origin
import os, time
#==============================================================================

# Set up Flask App with CORS
#------------------------------------------------------------------------------
application = Flask(__name__)
cors = CORS(application, resources={r"/*": {"origins": "*"}})
CORS(application)
#==============================================================================

# Load Configurations for App
#------------------------------------------------------------------------------
AppRootDirectory = os.path.dirname(os.path.realpath(__file__)) + '/'
from pyche import configuration as pyche_app_config
AppConfig = pyche_app_config.ConfigLoader()
AppConfig.SetAppDir(AppRootDirectory)
AppConfig.LoadConfig()	
#==============================================================================

# Set up MyDB
#------------------------------------------------------------------------------
if AppConfig.Database.isSet:
	from pyche import database_functions as pyche_fnc_db
	MyDB = pyche_fnc_db.PostgreDB()
	print('DatabaseConfig loaded')
else:
	print('DatabaseConfig not set')
	MyDB = False
#==============================================================================

# Functions
#------------------------------------------------------------------------------
def start_flask_app(ServerConfig):
	print(' ')
	print(' * Starting Flask Application')
	global application, AppConfig
	
	if AppConfig.ERROR == False:
		if ServerConfig.DNSConfig.SERVER_NAME != "0.0.0.0":
			AppConfig.Flask.SERVER_NAME = ServerConfig.DNSConfig.SERVER_NAME;
		AppConfig.Flask.SERVER_URL = ServerConfig.DNSConfig.SERVER_URL;
		application.config.from_object(AppConfig.Flask)
		application.config['CORS_HEADERS'] = 'Content-Type'
		from . import views
	else:
		application = False
	return application
#==============================================================================