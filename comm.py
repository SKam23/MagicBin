import requests
import json 
import random

REDIS_SERVER = ""
SECRET_KEY = "" 

def send_code():
	code = generate_code()
	thisData = {"hash": code} 
	requests.post(REDIS_SERVER + "/register/newtrash", data = json.dumps(thisData))
	
	
def generate_code():
	ops = "ABCDEFGHIJKLMNOPQRSTUVXYZ"
	result = ""
	for i in range(8):
        index = random.randint(0, len(ops)-1)
        result += ops[index]
        
    return result 
        
		
	
	
