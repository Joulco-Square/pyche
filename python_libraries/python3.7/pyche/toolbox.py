import string
import random

def generate_random_string(length):
	allchar = string.ascii_letters + string.digits
	random_string = "".join(random.choice(allchar) for x in range(length))
	return random_string

def generate_random_string_lower(length):
	return generate_random_string(length).lower()
	
def is_float(value):
	try:
		float(value)
		return True
	except:
		return False		

def is_integer(value):
	try:
		int(value)
		return True
	except:
		return False

def num(value):
	if is_float(value):
		return float(value)
	elif is_integer(value):
		return int(value)
	else:
		return 'error'
        

def is_num(value):
	if (is_float(value) or is_integer(value)):		
		return True
	else:
		return False	