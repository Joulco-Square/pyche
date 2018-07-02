# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: NONE
"""

from flask import Flask

application = Flask(__name__)

#Configuration of application, see configuration.py, choose one and uncomment.
#application.config.from_object('configuration.ProductionConfig')
application.config.from_object('app.configuration.DevelopmentConfig')
#application.config.from_object('configuration.TestingConfig')

from app import views