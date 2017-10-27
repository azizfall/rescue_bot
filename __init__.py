import RPi.GPIO as GPIO
import time
import json 
GPIO.setmode(GPIO.BCM)
from flask import Flask, request 

app = Flask(__name__)

servo_pin = 25
GPIO.setup(servo_pin,GPIO.OUT)
pwm = GPIO.PWM(servo_pin,50)
current_angle = 0

def duty_cycle(angle):
	duty_cycle = 0.0333333333*angle + 4.5 
	return duty_cycle


@app.route('/')
def homepage():
        return "HI MAN HERRO" 


@app.route('/app/v1/setup/camera') 
def setup_camera():
	if request.method == 'POST': 
		pwm.start(4.5)
@app.route('/api/v1/camera', methods=['GET','POST']) 
def camera_control(): 
	if request.method == 'POST': 
		servo_req = request.json
		key = servo_req['key']
		if key == 'left' and current_angle != 0:
			current_angle = current_angle - 5
			duty_cycle = duty_cycle(current_angle)
			pwm.ChangeDutyCycle(duty_cycle)
		elif key == 'right' and current_angle != 180:
			current_angle = current_angle + 5
			duty_cycle = duty_cycle(current_angle)
			pwm.ChangeDutyCycle(duty_cycle)

if __name__ == "__main__": 
        app.run()

