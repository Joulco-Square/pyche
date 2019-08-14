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
from flask import request,render_template, url_for
from .. import AppRootDirectory
from .. import AppConfig
from . import application
#==============================================================================

# Additional Modules Required
#------------------------------------------------------------------------------
import json
from datetime import datetime
import time
#==============================================================================

# Flask Routes
#------------------------------------------------------------------------------

# META DATA ROUTES +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@application.route('/favicon.ico')
def route_metadata_favicon():
	return application.send_static_file('icons/favicon.ico')
	
@application.route('/site.webmanifest')
def route_metadata_webmanifest():
	output = {}	
	output['name'] = "short_name"
	output['theme_color'] = "#ffffff"
	output['background_color'] = "#ffffff"
	output['display'] = "standalone"	
	output['icons'] = []
	
	new_icon = {}
	new_icon['src']=url_for('static',filename='icons/android-chrome-192x192.png')	
	new_icon['sizes'] = "192x192"
	new_icon['type'] = "image/png"
	output['icons'].append(new_icon)
	
	new_icon = {}
	new_icon['src']=url_for('static',filename='icons/android-chrome-512x512.png')	
	new_icon['sizes'] = "512x512"
	new_icon['type'] = "image/png"
	output['icons'].append(new_icon)	
	return output
# METAL DATA ROUTES ###########################################################


# PYCHE APP ROUTES ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@application.route('/pyche_app/status')
def route_system_status():
	output = {}
	output['STATUS'] = 'ONLINE'
	return json.dumps(output)

@application.route('/pyche_app/name')
def route_system_name():
	output = {}
	output['APP_NAME'] = AppConfig.Flask.NAME
	return json.dumps(output)
	
@application.route('/pyche_app/shortname')
def route_system_shortname():
	output = {}
	output['APP_SHORTNAME'] = AppConfig.Flask.SHORTNAME	
	return json.dumps(output)
	
@application.route('/pyche_app/description')
def route_system_description():
	output = {}
	output['APP_DESCRIPTION'] = AppConfig.Flask.DESCRIPTION
	return json.dumps(output)	
	
@application.route('/pyche_app/timestamp')
def route_system_timestamp():
	output = {}
	output['TIMESTAMP'] = str(time.time())
	return json.dumps(output)
	
# PYCHE APP ROUTES ############################################################

# SYSTEM ROUTES +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@application.context_processor
def inject_now():
	context_processor_json = {}
	context_processor_json['utc_timestamp'] = datetime.utcnow()
	context_processor_json['ThisURL'] = AppConfig.Flask.SERVER_URL
	context_processor_json['TemplateFunc'] = functions.Template()
	return context_processor_json
	
# SYSTEM ROUTES ###############################################################

# GOOGLE ROUTES +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
google_site_verification_code = '1234'
@application.route('/google' + google_site_verification_code + '.html')
def route_system_google_site_verification():
	output = 'google-site-verification: google'
	output += google_site_verification_code
	output += '.html'
	return output
# GOOGLE ROUTES #############################################################

#==============================================================================
