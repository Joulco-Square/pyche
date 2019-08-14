#!/usr/bin/python3
import sys

from pyche import wsgi

MyPycheConfig = wsgi.PycheConfig()
MyWSGI = wsgi.PycheWSGI()

config_filename = "hello_world"
MyPycheConfig.change_ConfigFilesDir('/var/www/pyche/www/config_files/')

MyPycheConfig.LoadConfig(config_filename)

mod_wsgi_config = MyPycheConfig.get_mod_wsgi_config()

MyWSGI.load_server_config(MyPycheConfig.get_ServerConfig())
MyWSGI.load_mod_wsgi_config(MyPycheConfig.get_mod_wsgi_config())

application = MyWSGI.get_app()