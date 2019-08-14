import string
import random
from .. import application
from .. import MyDB

import os, json, time
from datetime import datetime
from datetime import timezone

from pyche import toolbox as fnc_toolbox

from flask import url_for, redirect, render_template, flash, g, session, request
import urllib.request

def show_error_page(route,output_type):
	if output_type == 'HTML':
		return render_template('error/'+route)
	elif output_type == 'JSON':
		return '{"ERROR":"ERROR"}'
	else:
		return 'ERROR'

class Template(object):
	@classmethod
	def generate_random_string(placeholder,min_char,max_char):
		allchar = string.ascii_letters + string.punctuation + string.digits
		password = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
		return password





DBCacheDevice = {}
DBCacheDevice_time = 60 * 5
alerts_profiles = {}
AlertRules_Devices = {}

#+++++++++	PUSH DATA	++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#{
def ProcessUpload(UploadJSON):
	try:
		if 'id' not in UploadJSON:
			raise Exception('Missing ID. Hard fail')
		if 'val' not in UploadJSON:
			raise Exception('Missing Value. Hard fail')
		if 'ts' not in UploadJSON:
			UploadJSON['ts'] = str(round(time.time()))
		if 'ot' not in UploadJSON:
			UploadJSON['ot'] = {}
		isValid = PushDataToDB(UploadJSON)
		DBCacheDevice_Update(UploadJSON['id'],UploadJSON['ts'],UploadJSON['val'])
		try:
			ProcessAlert_DeviceID(UploadJSON['id'])
		except:
			print('Error checking alerts')		
	except Exception as e:
		print("type error: " + str(e))
		isValid = False
	except:	
		isValid = False
		print ("EXCEPT: ProcessUpload")	
	return isValid


def PushDataToDB(UploadJSON):
	TableName = TableNameFromID(UploadJSON['id'])
	[isValid,TableExists] = MyDB.check_table_exists('devices',TableName)
	if isValid:
		if not TableExists:
			print('Table does not exist, creating new table called ' + TableName)
			SchemaTableName = 'devices.'+TableName
			MyDB.duplicate_table('devices.sensor_null',SchemaTableName)
		data_json = {}			
		data_json['timestamp'] = 'postgresql_current_timestamp'
		data_json['value'] = UploadJSON['val'] 
		data_json['other'] = UploadJSON['ot']
		MyDB.sql_insert_json('devices',TableName,data_json)
	return isValid
#}
#+++++++++	PUSH DATA	++++++++++++++++++++++++++++++++++++++++++++++++++++++++


#+++++++++	PULL DATA	++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#{
def PullValData_Latest(request_ids,request_values_str):
	DeviceIDs = request_ids.split(',')
	request_values = request_values_str.split(',')
	output_json = {}
	for DeviceID in DeviceIDs:
		received_json = PullDataFromCache_Latest(DeviceID,request_values)
		#received_json = {}
		if received_json == {}:
			[isValid,received_json] = PullDataFromDB_Latest(DeviceID,request_values)
		else:
			isValid = True	
		if isValid:
			output_json[DeviceID] = received_json
	return isValid, output_json

def PullDataFromDB_Latest(DeviceID,request_values):
	received_output = {}	
	TableName = TableNameFromID(DeviceID)
	[isValid,TableExists] = MyDB.check_table_exists('devices',TableName)
	if isValid and TableExists:
		[isValid,db_data] = MyDB.database_get_latest_entry('devices',TableName,'timestamp')
		if isValid:
			received_output = ConvertValDataFromDBForOutput(db_data,request_values)
	return isValid, received_output


def PullValData_LatestX(request_ids,request_values_str,x):
	DeviceIDs = request_ids.split(',')
	request_values = request_values_str.split(',')
	output_json = {}
	for DeviceID in DeviceIDs:
		isValid, received_json = PullDataFromDB_LatestX(DeviceID,request_values,x)
		if isValid:
			output_json[DeviceID] = received_json
	return isValid, output_json

def PullDataFromDB_LatestX(DeviceID,request_values,number_of_entries):
	output = {}
	TableName = TableNameFromID(DeviceID)
	[isValid,TableExists] = MyDB.check_table_exists('devices',TableName)
	if isValid and TableExists:
		[isValid,db_data] = MyDB.database_get_x_latest_entries('devices',TableName,'timestamp',number_of_entries)
		if isValid:
			output = ConvertValDataFromDBForOutput(db_data,request_values)
	return isValid, output


def PullValData_LatestT(request_ids,request_values_str,time_sec_str):
	DeviceIDs = request_ids.split(',')
	request_values = request_values_str.split(',')
	output_json = {}
	try:
		time_sec = fnc_toolbox.num(time_sec_str)
	except:	
		time_sec = 0
	for DeviceID in DeviceIDs:
		if time_sec <= DBCacheDevice_time:
			received_json = PullDataFromCache_LatestT(DeviceID,request_values,time_sec)
			isValid = True
		else:
			isValid, received_json  = PullValDataFromDB_LatestT(DeviceID,request_values,time_sec)
		if isValid:			
			output_json[DeviceID] = received_json	
	return isValid, output_json


def PullValDataFromDB_LatestT(DeviceID,request_values,time_sec):
	output = {}
	TableName = TableNameFromID(DeviceID)
	[isValid,TableExists] = MyDB.check_table_exists('devices',TableName)
	if isValid and TableExists:		
		start_time = round(time.time() - time_sec)
		end_time = round(time.time())
		[isValid,db_data] = MyDB.database_get_entries_between('devices',TableName,'timestamp','timestamp',start_time,end_time)
		if isValid:
			output = ConvertValDataFromDBForOutput(db_data,request_values)
	return isValid, output


def PullValData_Between(request_ids,request_values_str,timestamp_range_str):
	DeviceIDs = request_ids.split(',')
	request_values = request_values_str.split(',')
	try:
		timestamp_range = timestamp_range_str.split(',')
		start_time = fnc_toolbox.num(timestamp_range[0])
		end_time = fnc_toolbox.num(timestamp_range[1])
	except:
		start_time = round(time.time())
		end_time = round(time.time())
	output_json = {}
	for DeviceID in DeviceIDs:
		isValid, received_json = PullDataFromDB_Between(DeviceID,request_values,start_time,end_time)
		if isValid:
			output_json[DeviceID] = received_json
	return isValid, output_json


def PullDataFromDB_Between(DeviceID,request_values,start_time,end_time):
	output = {}
	TableName = TableNameFromID(DeviceID)
	[isValid,TableExists] = MyDB.check_table_exists('devices',TableName)
	if isValid and TableExists:
		[isValid,db_data] = MyDB.database_get_entries_between('devices',TableName,'timestamp','timestamp',start_time,end_time)
		if isValid:
			output = ConvertValDataFromDBForOutput(db_data,request_values)
	return isValid, output


def GetRequestValuesFromValJSON(request_values,val_json):
	output = {}
	if request_values == ['*']:
		for request_value in val_json:
			output[request_value] = val_json[request_value]
	else:
		for request_value in request_values:
			if request_value in val_json:
				output[request_value] = val_json[request_value]
			else:
				output[request_value] = 'null'
	return output


def ConvertValDataFromDBForOutput(db_data,request_values):
	output_data = {}
	for i in db_data:
		output_data_row = {}
		#ts = time.mktime(db_data[i]['timestamp'].timetuple())
		#ts = round(time.mktime(db_data[i]['timestamp'].timetuple()))
		ts = db_data[i]['timestamp'].replace(tzinfo=timezone.utc).timestamp()
		output_data_row = GetRequestValuesFromValJSON(request_values,db_data[i]['value'])
		output_data[ts] = output_data_row
	return output_data
#}
#+++++++++	PULL DATA	++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def check_get_arguments(request_arguments,required_arguments):
	isValid = True
	for agr in required_arguments:
		if agr not in request_arguments:
			isValid = False
	return isValid

def TableNameFromID(DeviceID):
	output = 'sensor_' + DeviceID
	return output
	
def GetLatestTS(JSON):
	return min(JSON.keys())
	
def GetAgeOfTS(TS):
	current_ts = time.time()
	age = current_ts - TS
	return age
	



#+++++++++	 DEVICES CACHE	+++++++++++++++++++++++++++++++++++++++++++++++++++++
#{
def DBCacheDevice_Construct():
	[isValid,db_tables] = MyDB.get_tables_in_schema('devices')
	for table_name in db_tables:
		if (table_name.find('sensor_') == 0):
			DeviceID = table_name[len('sensor_'):]
			if DeviceID != 'null':				
				DBCacheDevice[DeviceID] = {}
				isValid, output_json = PullValDataFromDB_LatestT(DeviceID,['*'],DBCacheDevice_time)
				if isValid:
						DBCacheDevice[DeviceID] = output_json

def DBCacheDevice_Update(DeviceID,ts,val_json):
	if DeviceID not in DBCacheDevice:
		DBCacheDevice[DeviceID] = {} 

	DBCacheDevice[DeviceID][ts] = val_json	
	DBCacheDevice_RemoveOld()

def DBCacheDevice_RemoveOld():
	current_ts = time.time()
	old_ts = current_ts - DBCacheDevice_time
	for DeviceID in DBCacheDevice:
		for ts in DBCacheDevice[DeviceID]:
			if ts < old_ts:
				DBCacheDevice.pop(ts, None)
				
def PullDataFromCache_Latest(DeviceID,request_values):
	output = {}
	latest_ts = 0;
	if DeviceID not in DBCacheDevice:
		print(' ** Calling non existing DeviceID ["' + DeviceID + '"] from DBCacheDevice')
	else: 
		if DBCacheDevice[DeviceID] != {}:
			for ts in DBCacheDevice[DeviceID]:
				if ts > latest_ts:
					latest_ts = ts
			output[ts] = GetRequestValuesFromValJSON(request_values,DBCacheDevice[DeviceID][latest_ts])
	return output
				
def PullDataFromCache_LatestT(DeviceID,request_values,time_sec):
	output = {}
	for ts in DBCacheDevice[DeviceID]:
		if GetAgeOfTS(ts) < time_sec:
			output[ts] = {}
			output[ts]['val'] = GetRequestValuesFromValJSON(request_values,DBCacheDevice[DeviceID][ts])
	return output
#}
#+++++++++	 DEVICES CACHE	+++++++++++++++++++++++++++++++++++++++++++++++++++++


#+++++++++	 ALERTS	+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#{
def CheckExists_ProfileID(ProfileID):
	global alerts_profiles
	if ProfileID in alerts_profiles:
		return True
	else:
		return False

def PullDataFromDB_AlertProfiles():
	global MyDB, alerts_profiles
	alerts_profiles = {}
	[isValid,Exists] = MyDB.check_table_exists('alerts','profiles')
	if isValid and Exists:
		[isValid,CallResult] = MyDB.database_get_x_latest_entries('alerts','profiles','profile_id',999)
		if isValid:
			for entry in CallResult:
				ProfileID = CallResult[entry]['profile_id'].strip()
				alerts_profiles[ProfileID] = CallResult[entry]
				del alerts_profiles[ProfileID]['profile_id']
				del alerts_profiles[ProfileID]['table_id']
				alerts_profiles[ProfileID]['triggered'] = False			
				alerts_profiles[ProfileID]['state'] = 'ok'			
			AlertRules_Devices_Update()
			return True
		else:
			return False
	else:
		return False
	
def SyncDataWithDB_AlertProfiles():
	global MyDB, alerts_profiles
	for ProfileID in alerts_profiles:
		if alerts_profiles[ProfileID]['state'] == 'new':
			print('Insert JSON')
			InsertJSON = {}
			InsertJSON['profile_id'] = ProfileID
			InsertJSON['enabled'] = alerts_profiles[ProfileID]['enabled']
			InsertJSON['level'] = alerts_profiles[ProfileID]['level']
			InsertJSON['rules'] = alerts_profiles[ProfileID]['rules']
			MyDB.sql_insert_json('alerts','profiles',InsertJSON)
			alerts_profiles[ProfileID]['state'] == 'ok'
		elif alerts_profiles[ProfileID]['state'] == 'updated':
			print('Update JSON')
			InsertJSON = {}
			InsertJSON['profile_id'] = ProfileID
			InsertJSON['enabled'] = alerts_profiles[ProfileID]['enabled']
			InsertJSON['level'] = alerts_profiles[ProfileID]['level']
			InsertJSON['rules'] = alerts_profiles[ProfileID]['rules']
			MyDB.sql_update_json('alerts','profiles','profile_id',ProfileID,InsertJSON)
			alerts_profiles[ProfileID]['state'] == 'ok'
	
def AlertProfile_Update_Enabled(ProfileID,enabled_status):	
	global alerts_profiles
	alerts_profiles[ProfileID]['enabled'] = enabled_status
	alerts_profiles[ProfileID]['state'] = 'updated'
	SyncDataWithDB_AlertProfiles()
	return True
	
def AlertProfile_Update_Level(ProfileID,new_level):	
	global alerts_profiles
	alerts_profiles[ProfileID]['level'] = new_level
	alerts_profiles[ProfileID]['state'] = 'updated'
	SyncDataWithDB_AlertProfiles()
	return True	
	
def AlertProfile_Update_All(ProfileID,data_json):
	global alerts_profiles
	UpdateProfileJSON = {}	
	if 'enabled' in data_json:
		UpdateProfileJSON['enabled'] = data_json['enabled']
	else:
		UpdateProfileJSON['enabled'] = True
	if 'level' in data_json:
		UpdateProfileJSON['level'] = data_json['level']
	else:
		UpdateProfileJSON['level'] = 1
	if 'rules' in data_json:
		UpdateProfileJSON['rules'] = data_json['rules']		
	else:
		isValid = False
		return isValid		
	UpdateProfileJSON['triggered'] = False
	UpdateProfileJSON['state'] = 'updated'
	
	alerts_profiles[ProfileID] = UpdateProfileJSON
	AlertRules_Devices_Update()
	SyncDataWithDB_AlertProfiles()
	
	isValid = True
	return isValid
	
def AlertRules_Devices_Update():
	global alerts_profiles,AlertRules_Devices
	AlertRules_Devices = {}
	for ProfileID in alerts_profiles:
		for rule_number in alerts_profiles[ProfileID]['rules']:
			DeviceID = alerts_profiles[ProfileID]['rules'][rule_number]['device_id']
			if DeviceID not in AlertRules_Devices:
				AlertRules_Devices[DeviceID] = []
			AlertRules_Devices[DeviceID].append(ProfileID)

def New_AlertProfile(data_json):
	global alerts_profiles,AlertRules_Devices
	NewProfileJSON = {}	
	if 'enabled' in data_json:
		NewProfileJSON['enabled'] = data_json['enabled']
	else:
		NewProfileJSON['enabled'] = True
	if 'level' in data_json:
		NewProfileJSON['level'] = data_json['level']
	else:
		NewProfileJSON['level'] = 1
	if 'rules' in data_json:
		NewProfileJSON['rules'] = data_json['rules']		
	else:
		isValid = False
		return [isValid, '']		
	NewProfileJSON['triggered'] = False
	NewProfileJSON['state'] = 'new'
	ProfileID = fnc_toolbox.generate_random_string_lower(10)
	alerts_profiles[ProfileID] = NewProfileJSON
	AlertRules_Devices_Update()
	SyncDataWithDB_AlertProfiles()	
	isValid = True
	return [isValid, ProfileID]

def check_threshold(threshold_type,threshold_value,reading_value):
	if threshold_type == 'upper':
		if reading_value > threshold_value:
			return True
		else:
			return False
	elif threshold_type == 'lower':
		if reading_value < threshold_value:
			return True
		else:
			return False
	else:
		return False
		
def ProcessAlert_AllProfiles():
	global alerts_profiles
	#print('Processing all rules')
	#print('{')
	for ProfileID in alerts_profiles:
		 ProcessAlert_ProfileID(ProfileID)
	#print('}')		
		

def ProcessAlert_ProfileID(ProfileID):
	global alerts_profiles
	print_str = 'Running "ProcessRule_Thresholds" for Rule: ' + ProfileID
	if alerts_profiles[ProfileID]['enabled']:
		print_str += ', Rule enabled.. continuing'
		isTriggered = False
		for rule_number in alerts_profiles[ProfileID]['rules']:
		# {
			this_rule = alerts_profiles[ProfileID]['rules'][rule_number]
			DeviceID = this_rule['device_id']	
			isValid, output_json = PullValData_Latest(DeviceID,str(this_rule['val_type']))
			if output_json != {} and output_json[DeviceID] != {}:
				last_update = GetLatestTS(output_json[DeviceID])				
				latest_val = output_json[DeviceID][last_update][this_rule['val_type']]
				if GetAgeOfTS(last_update) > (60*60*24):
					print_str += ', Last update to old to run rule'
					print(print_str)
					break
				if check_threshold(this_rule['rule_type'],this_rule['value'],latest_val):
					isTriggered = True
					if this_rule['duration'] > 0:
					# {
						isValid, output_json = PullValData_LatestT(DeviceID,str(this_rule['val_type']),str(this_rule['duration']))
						if output_json != {}:
							for ts_entry in output_json[DeviceID]:
								if not check_threshold(this_rule['rule_type'],this_rule['value'],output_json[DeviceID][ts_entry][this_rule['val_type']]):
									isTriggered = False
					# }
		# }
		if isTriggered:
			RuleTriggered(ProfileID)
		else:
			print_str += ', Rule not triggered'
			alerts_profiles[ProfileID]['triggered'] = False
	#print(print_str)
				
	
def ProcessAlert_DeviceID(DeviceID):
	global AlertRules_Devices
	if DeviceID in AlertRules_Devices:
		for ProfileID in AlertRules_Devices[DeviceID]:
			ProcessAlert_ProfileID(ProfileID)

def RuleTriggered(ProfileID):
	global alerts_profiles
	if not alerts_profiles[ProfileID]['triggered']:
		print('	#### RULE ' + ProfileID+ ' TRIGGERED')
		alerts_profiles[ProfileID]['triggered'] = True
		url_to_read = 'http://192.168.100.224/server/status/'
		try:
			response=urllib.request.urlopen(url_to_read, timeout=120)
			page=response.read().decode('utf-8')
			print(page)
		except:
			print(' ** Unable to call Alert URL')
	else:
		print('rule already triggered')
#}
#+++++++++	 ALERT - THRESHOLDS	+++++++++++++++++++++++++++++++++++++++++++++++

