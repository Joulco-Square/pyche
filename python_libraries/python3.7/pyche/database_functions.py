# -*- encoding: utf-8 -*-
"""
 * Copyright (C) Joulco Square PTY LTD - All Rights Reserved
 * Unauthorized copying of this file, via any medium is strictly prohibited
 * Proprietary and confidential
 * Written by Willem Grobler <willem@joulco2.com>, July 2019
 *
"""

import psycopg2
import json
import time
from datetime import datetime

class PostgreDB(object):
	def __init__(self):
		self.db_status = 'CLOSED'
		self.this_db = ''
		self.DATABASE_HOST = ''
		self.DATABASE_NAME = ''
		self.DATABASE_USER = ''
		self.DATABASE_PASSWD = ''

	def set_database_config(self,host,db_name,user,password):
		self.DATABASE_HOST = host
		self.DATABASE_NAME = db_name
		self.DATABASE_USER = user
		self.DATABASE_PASSWD = password

	def CheckConnection(self):
		try:
			self._connect()
			return True
		except:
			return False

	def _connect(self):
		if self.db_status == 'CLOSED':
			self.this_db = psycopg2.connect(host=self.DATABASE_HOST,user=self.DATABASE_USER,password=self.DATABASE_PASSWD,database=self.DATABASE_NAME)
			db_status = 'OPEN'
	
	def _disconnect(self):
		if self.db_status == 'OPEN':
			self.this_db.close()
			self.db_status = 'CLOSED'

	def call_sql(self,sql_query):
		self._connect()
		
		cursor=self.this_db.cursor()
		cursor.execute(sql_query)
		output = self.sql_result_to_dict(cursor)
		return output

	def call_sql_commit(self,sql_query):
		self._connect()
		
		cursor=self.this_db.cursor()
		cursor.execute(sql_query)
		#output = sql_result_to_dict(cursor)
		#return output	
		self.this_db.commit()
		return True	

	def check_table_exists(self,schema_name,table_name):
		sql_query = "SELECT EXISTS (SELECT 1 FROM   information_schema.tables WHERE  table_schema = '" + schema_name + "' AND    table_name = '" + table_name + "');"
		output = self.call_sql(sql_query)
		try:
			isValid = True
			TableExists = output['1']['exists']
		except:
			isValid = False
			TableExists = False
		return [isValid,TableExists]

	def sql_result_to_dict(self,cursor):
		col_names = []	
		for item in cursor.description:
			col_names.append(item[0])
	
		output = {}
		counter = 0
		for row in cursor.fetchall():
			counter += 1
			output[str(counter)] = {}
			for x in range(len(col_names)):
				output[str(counter)][col_names[x]] = row[x]
		return output

	def duplicate_table(self,existing_table,new_table):
		sql_query = 'create table ' + new_table +' (like ' + existing_table + ' including all)'
		isValid = self.call_sql_commit(sql_query)
		return isValid

	def sql_insert_json(self,schema_name,table_name,data_json):		
		keys = []
		values = ''
		for key in data_json:
			keys.append(key)
			if type(data_json[key]) is float:
				values += str(data_json[key])
			elif type(data_json[key]) is int:
				values += str(data_json[key])
			elif type(data_json[key]) is str:
				if data_json[key] == 'postgresql_current_timestamp':
					values += 'current_timestamp'
				else:
					values += "'" + data_json[key] + "'"		
			elif type(data_json[key]) is dict or type(data_json[key]) is list:
				values += "'" + json.dumps(data_json[key]) + "'"
			elif type(data_json[key]) is bool:
				if data_json[key]:
					values += 'true'
				else:
					values += 'false'
			elif type(data_json[key]) is datetime:
				#values +=  "TIMESTAMP '" + data_json[key].strftime('%Y-%m-%d %H:%M:%S.%f') + "'"
				values +=  " '" + data_json[key].strftime('%Y-%m-%d %H:%M:%S.%f') + "'::timestamp AT TIME ZONE 'Africa/Johannesburg'"				
			else:
				print('unknown format')
				print(type(data_json[key]))
			values += ","
		values = values[:-1]
		sql_query = 'INSERT INTO ' + schema_name + '."' + table_name + '"(' + ','.join(keys) + ") VALUES (" + values + ")";
		self._connect()
		cursor=self.this_db.cursor()
		cursor.execute(sql_query)
		self.this_db.commit()
		return True	
	
	def sql_update_json(self,schema_name,table_name,where_col,where_val,data_json):
		set_string = ''
		for key in data_json:
			set_string += str(key) + '='
			if type(data_json[key]) is float:
				set_string += str(data_json[key])
			elif type(data_json[key]) is int:
				set_string += str(data_json[key])
			elif type(data_json[key]) is str:
				if data_json[key] == 'postgresql_current_timestamp':
					set_string += 'current_timestamp'
				else:
					set_string += "'" + data_json[key] + "'"		
			elif type(data_json[key]) is dict or type(data_json[key]) is list:
				set_string += "'" + json.dumps(data_json[key]) + "'"
			elif type(data_json[key]) is bool:
				if data_json[key]:
					set_string += 'true'
				else:
					set_string += 'false'
			else:
				print('unknown format')
				print(type(data_json[key]))
			set_string += ","
		set_string = set_string[:-1]
		sql_query = 'UPDATE ' + schema_name + '.' + table_name + ' SET ' + set_string + ' WHERE ' + where_col + "='" + where_val + "';";
		self._connect()
		cursor=self.this_db.cursor()
		cursor.execute(sql_query)
		self.this_db.commit()
		return True	

	def database_get_latest_entry(self,schema_name,table_name,order_by_column):
		isValid = True
		sql_query = "SELECT * FROM " + schema_name + '.' + table_name + " ORDER BY " + order_by_column + " DESC LIMIT 1;"
		output = self.call_sql(sql_query)
		if output == {}:
			isValid = False
		return [isValid,output]

	def database_get_x_latest_entries(self,schema_name,table_name,order_by_column,X):
		isValid = True
		sql_query = "SELECT * FROM " + schema_name + '.' + table_name + " ORDER BY " + order_by_column + " DESC LIMIT " + str(X) + ";"
		output = self.call_sql(sql_query)
		if output == {}:
			isValid = False
		return [isValid,output]

	def database_get_x_latest_entries_where(self,schema_name,table_name,order_by_column,X,where_col,where_val):
		isValid = True
		sql_query = "SELECT * FROM " + schema_name + '.' + table_name + " WHERE " + where_col + " = FALSE" + " ORDER BY " + order_by_column + " DESC LIMIT " + str(X) + ";"
		output = self.call_sql(sql_query)
		if output == {}:
			isValid = False
		return [isValid,output]
		
	def database_get_entries_between(self,schema_name,table_name,order_by_column,where_col,start,end):
		isValid = True
		
		start_time = datetime.fromtimestamp(start).strftime('%Y-%m-%d %H:%M:%S')
		end_time = datetime.fromtimestamp(end).strftime('%Y-%m-%d %H:%M:%S')
		
		sql_query = "SELECT * FROM " + schema_name + '.' + table_name + " WHERE " + where_col +  " BETWEEN '" + start_time + "'::timestamp AND '" + end_time + "'::timestamp" + " ORDER BY " + order_by_column + ";"
		output = self.call_sql(sql_query)
		if output == {}:
			isValid = False
		return [isValid,output]

	def get_tables_in_schema(self,schema_name):
		isValid = True
		sql_query = "select table_name from information_schema.tables where table_schema = '" + schema_name + "'"
		sql_output = self.call_sql(sql_query)
		if sql_output == {}:
			isValid = False
			output = sql_output
		else:
			output = []
			for entry in sql_output:
				output.append(sql_output[entry]['table_name'])
		return [isValid,output]

	def database_delete_entry(self,schema_name,table_name,where_col,where_val):
		isValid = True
		sql_query = "DELETE FROM " + schema_name + '.' + table_name + " WHERE " + where_col +  " = '" + where_val + "';"
		self._connect()
		cursor=self.this_db.cursor()
		cursor.execute(sql_query)
		self.this_db.commit()
		return True










