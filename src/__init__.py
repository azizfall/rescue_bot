
import time
import json 
from flask import Flask, request
from flask import jsonify
import os
import sys
import subprocess 

app = Flask(__name__)

current_angle = 0


@app.route('/')
def homepage():
        return "HI MAN HERRO" 


@app.route('/api/v1/setup/camera') 
def setup_camera():
	if request.method == 'POST':
		call(["./serv","0"])
		return jsonify({"Status":"Success"})
	else: return jsonify({"Status":"Failure"})

@app.route('/api/v1/camera',methods=['GET','POST'])
def camera_control():
	if request.method == 'POST':
		servo_req = request.json
		key = servo_req['key']
		os.system("./serv 180")
		subprocess.call(['/var/www/FlaskApp/FlaskApp/.serv','180'],shell=True)
		#cmd = ["./serv","180"]
		#p = subprocess.Popen(cmd,stdout = subprocess.PIPE,stderr = subprocess.PIPE, stdin = subprocess.PIPE)
		#out , err = p.communicate()
		#if key == 'left':
		#	if current_angle != 0:
		#		current_angle = current_angle - 30
		#		call(["./serv",str(current_angle)])
		#		return jsonify({"Status":"Success"})
		#elif key == 'right':
		#	if current_angle != 180:
		#		current_angle = current_angle + 30
		#		call(["./serv",str(current_angle)])
		#		return jsonify({"Status","Success"})
		#return jsonify({"Status":"Failure"})

@app.route('/api/v1/motors', methods=['GET','POST']) 
def motor_control():
	if request.method == 'POST':
		motor_req = request.json
		key = motor_req['key']
		dev = os.open("/dev/memory",os.O_RDWR)
		if key == 'left':
			data = "L"
			os.write(dev,data)
			return jsonify({"Status":"success"})
		elif key == 'right':
			data = "R"
			os.write(dev,data)
			return  jsonify({"Status":"success"})
	return jsonify({"Status":"Failure"})

if __name__ == "__main__": 
        app.run()

