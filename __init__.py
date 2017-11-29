
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
		return jsonify({"available":is_available[0]}) 

@app.route('/api/v1/robot/dissable',methods=['GET','POST'])
def dissable():
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
		cmd=['/var/www/FlaskApp/FlaskApp/serv','1','0']
		p = subprocess.Popen(cmd,stdout = subprocess.PIPE,stderr = subprocess.PIPE, stdin = subprocess.PIPE)
		out , err = p.communicate()
		cmd=['/var/www/FlaskApp/FlaskApp/serv','2','0']
                p = subprocess.Popen(cmd,stdout = subprocess.PIPE,stderr = subprocess.PIPE, stdin = subprocess.PIPE)
                out , err = p.communicate()
		return jsonify({"Status":"Success"})
	else: return jsonify({"Status":"Failure"})

@app.route('/api/v1/gps',methods=['GET','POST'])
def gps():
	if request.method == 'POST':
		cmd=['/var/www/FlaskApp/FlaskApp/gps']
		p = subprocess.Popen(cmd,stdout = subprocess.PIPE,stderr = subprocess.PIPE, stdin = subprocess.PIPE)
		out , err = p.communicate()
		return jsonify({"GPS_DATA":str(out)})
	return jsonify({"Status":"Failure"})


@app.route('/api/v1/camera/1',methods=['GET','POST'])
def camera_control_1():
	try:
		if request.method == 'POST':
			servo_req = request.json
			key = servo_req['key']
			cmd = ['/var/www/FlaskApp/FlaskApp/serv','1',str(key)]
			p = subprocess.Popen(cmd,stdout = subprocess.PIPE,stderr = subprocess.PIPE, stdin = subprocess.PIPE)
			out , err = p.communicate()
			return jsonify({"angle":key})
	except Exception as e:
		return str(e)

@app.route('/api/v1/camera/2',methods=['GET','POST'])
def camera_control_2():
        try:
                if request.method == 'POST':
                        servo_req = request.json
                        key = servo_req['key']
                        cmd = ['/var/www/FlaskApp/FlaskApp/serv','2',str(key)]
                        p = subprocess.Popen(cmd,stdout = subprocess.PIPE,stderr = subprocess.PIPE, stdin = subprocess.PIPE)
                        out , err = p.communicate()
                        return jsonify({"angle":key})
        except Exception as e:
                return str(e)

@app.route('/api/v1/motors/speed',methods=['GET','POST'])
def speed_control():
        try:
                if request.method == 'POST':
                        speed_req = request.json
                        speed = speed_req['speed']
                        cmd = ['/var/www/FlaskApp/FlaskApp/serv','0',str(speed)]
                        p = subprocess.Popen(cmd,stdout = subprocess.PIPE,stderr = subprocess.PIPE, stdin = subprocess.PIPE)
                        out , err = p.communicate()
			cmd = ['/var/www/FlaskApp/FlaskApp/serv','4',str(speed)]
                        p = subprocess.Popen(cmd,stdout = subprocess.PIPE,stderr = subprocess.PIPE, stdin = subprocess.PIPE)
                        out , err = p.communicate()
                        return jsonify({"speed":speed})
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
		elif key == 'stop':
			data = "S"
			os.write(dev,data)
			return jsonify({"Status":"success"})
	return jsonify({"Status":"Failure"})

if __name__ == "__main__": 
        app.run()

