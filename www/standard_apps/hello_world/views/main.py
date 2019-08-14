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
from flask import request,render_template
from .. import AppRootDirectory
from .. import AppConfig
from . import application
#==============================================================================

# Flask Routes
#------------------------------------------------------------------------------

# STANDARD ROUTES +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@application.route('/', methods = ['GET'])
def route_page_index():
	return "Hello World"
	
# STANDARD ROUTES #############################################################

#==============================================================================