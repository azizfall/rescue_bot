
import time
import json 
from flask import Flask, request
from flask import jsonify
import os
import subprocess 

from dbconnect import connect 

app = Flask(__name__)

#current_angle = 0


@app.route('/')
def homepage():
        return "HI MAN HERRO" 


@app.route('/api/v1/robot/available',methods=['GET','POST'])
def available():
	if request.method == 'POST':
		cursor,conn = connect()
		cursor.execute("SELECT available from Robot")
		is_available = cursor.fetchone()
		conn.commit()
		cursor.close()
		conn.close()
		return jsonify({"available":is_available}) 

@app.route('/api/v1/robot/dissable',methods=['GET','POST'])
def dissbale():
	if request.method == 'POST':
		cursor,conn = connect()
		cursor.execute("UPDATE Robot SET available=0")
		conn.commit()
		cursor.close()
		conn.close()
		return jsonify({"Status":"Success"})


@app.route('/api/v1/robot/enable',methods=['GET','POST'])
def enable():
	if request.method == 'POST':
		cursor,conn = connect()
		cursor.execute("UPDATE Robot SET available=1")
		conn.commit()
		cursor.close()
		conn.close()
		return jsonify({"Status":"Success"})


@app.route('/api/v1/setup/camera', methods=['GET','POST']) 
def setup_camera():
	if request.method == 'POST':
		cmd=['/var/www/FlaskApp/FlaskApp/serv','0']
		p = subprocess.Popen(cmd,stdout = subprocess.PIPE,stderr = subprocess.PIPE, stdin = subprocess.PIPE)
		out , err = p.communicate()
		return jsonify({"Status":"Success"})
	else: return jsonify({"Status":"Failure"})

@app.route('/api/v1/gps',methods=['GET','POST'])
def gps():
	if request.method == 'POST':
		cmd=['/var/www/FlaskApp/FlaskApp/gps']
		#cmd=['ls','-l']
		p = subprocess.Popen(cmd,stdout = subprocess.PIPE,stderr = subprocess.PIPE, stdin = subprocess.PIPE)
		out , err = p.communicate()
		return jsonify({"GPS_DATA":str(out)})
	return jsonify({"Status":"Failure"})


@app.route('/api/v1/camera',methods=['GET','POST'])
def camera_control():
	try:
		#global current_angle
		if request.method == 'POST':
			servo_req = request.json
			key = servo_req['key']
			if 1:
				if 1:
					#current_angle = current_angle - 30
					#return current_angle
					cmd = ['/var/www/FlaskApp/FlaskApp/serv',str(key)]
					p = subprocess.Popen(cmd,stdout = subprocess.PIPE,stderr = subprocess.PIPE, stdin = subprocess.PIPE)
					out , err = p.communicate()
					#return jsonify({"Status":"Success"})
					return jsonify({"angle":key})
			#elif key == 'right':
			#	if current_angle != 180:
			#		current_angle = current_angle + 30
			#		#return current_angle
			#		cmd = ['/var/www/FlaskApp/FlaskApp/serv',str(current_angle)]
			#		p = subprocess.Popen(cmd,stdout = subprocess.PIPE,stderr = subprocess.PIPE, stdin = subprocess.PIPE)
			#		out , err = p.communicate()
			#		#return jsonify({"Status":"Success"})
			#		return jsonify({"angle":current_angle})
			#return jsonify({"Status":"Failure"})
			#return subprocess.call(['ls','-l'],shell=True)
			return jsonify({"angle":key})
	except Exception as e:
		return str(e)

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
		elif key == 'up':
			data = "F"
			os.write(dev,data)
			return  jsonify({"Status":"success"})
		elif key == 'down':
			data = "B"
			os.write(dev,data)
			return  jsonify({"Status":"success"})
	return jsonify({"Status":"Failure"})

if __name__ == "__main__": 
        app.run()

