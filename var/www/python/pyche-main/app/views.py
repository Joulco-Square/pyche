# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: Private
"""

from flask import url_for, redirect, render_template, flash, g, session
from app import application
#from app import api_functions
#from app import functions
#import json

#-----------------      STATUS  -----------------

@application.route('/status')
def route_status():
        return 'ONLINE'

@application.route('/server_name')
def route_server_name():
        return 'server management'

@application.route('/')
def route_index():
        from time import gmtime, strftime
        return strftime("%Y-%m-%d %H:%M:%S", gmtime())


#-----------------      STATUS  -----------------