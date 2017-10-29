#import RPi.GPIO as GPIO
import time
import json 
#GPIO.setmode(GPIO.BCM)
from flask import Flask, request
from flask import jsonify
import os

app = Flask(__name__)

#servo_pin = 25
#GPIO.setup(servo_pin,GPIO.OUT)
#pwm = GPIO.PWM(servo_pin,50)
current_angle = 0

def duty_cycle(angle):
	duty_cycle = 0.0333333333*angle + 4.5 
	return duty_cycle


@app.route('/')
def homepage():
        return "HI MAN HERRO" 


@app.route('/api/v1/setup/camera') 
def setup_camera():
	if request.method == 'POST':
		return jsonify({"Status":"Success"})
	else: return jsonify({"Status":"Failure"})
@app.route('/api/v1/camera', methods=['GET','POST']) 
def camera_control():
	if request.method == 'POST':
		servo_req = request.json
		key = servo_req['key']
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

