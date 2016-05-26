
async_mode = None

if async_mode is None:
	try:
		import eventlet
		async_mode = 'eventlet'
	except ImportError:
		pass

	if async_mode is None:
		try:
			from gevent import monkey
			async_mode = 'gevent'
		except ImportError:
			pass

	if async_mode is None:
		async_mode = 'threading'

	print "async_mode is ", async_mode

if async_mode == 'eventlet':
	import eventlet
	eventlet.monkey_patch()
elif async_mode == 'gevent':
	from gevent import monkey
	monkey.patch_all()

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import time, threading

import json, random
from Queue import Queue

import datetime

def get_time():
	now =  datetime.datetime.now()
	return (str(now.minute) +':' + str(now.second))

def validateUser(username, password):
	if username == 'admin' and password == 'secure':
		return True
	return False

app = Flask(__name__)
queue = Queue()
json_data = {'house_id' : 1001, 'sensor_1' : 0, 'sensor_2': 0, 'active': 0, 'time' : get_time() + "xxxx"}

@app.route('/')
def home():
	return render_template('form.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
	username="Dummy"
	password = "Dummy"
	text = ""
	if request.method == 'POST':
		for key in request.form.keys():
			if key == 'username':
				username = request.form[key]
			if key == 'password':
				password = request.form[key]
	if validateUser(username, password):
		print "Rendering value : ", json_data
		return render_template('home.html')
	else:
		print "Rendering value : ", json_data
		return render_template('form.html')


socketio = SocketIO(app, async_mode=async_mode)

@socketio.on('channel_client_to_server')
def client_data(c_request):
	global json_data
	temp = dict(json_data)
	temp['time'] = "Test time"
	data = json.dumps(temp)
	emit("channel_server_to_client", data)

def serial_reads():
	global socketio
	while True:
		data = str(random.randrange(0,100))
		socketio.emit('channel_server_to_client', data)
		print "Data sent %s"%data
		time.sleep(3)

def send_data():
	global socketio, queue
	while True:
		data = queue.get()
		data = json.dumps(data)
		socketio.emit('channel_server_to_client', data)
		print "Remaining data size: %d Data sent %s"%(queue.qsize(), data)

def serial_read():
	import Adafruit_BBIO.UART as uart
	import serial
	uart.setup("UART1")
	port = serial.Serial( '/dev/ttyO1',9600)
	global queue, json_data
	count = 0
	while(1):
		print "\n\nLooking for auduino data\n\n"
		while port.inWaiting()== 0:
			eventlet.sleep(.1)
		data = port.readline().strip()
		print data

		if data == '12849':		#system deactive
			print "Making system deative"
			json_data['active'] = 0
			json_data['sensor_1'] = 0
			json_data['sensor_2'] = 0
			json_data['time'] = get_time() + "abc%d"%count

		elif data == '12593':	#system active
			print "Making system ACTIVE"
			json_data['active'] = 1
			json_data['time'] = get_time() + "def%d"%count

		elif data == '18481':	#sensor_1 active
			print "Sensor 1 movement"
			json_data['sensor_1'] = 1
			json_data['time'] = get_time() + "ghi%d"%count

		elif data == '13881':	#sensor_2 active
			print "Sensor 2 movement"
			json_data['sensor_2'] = 1
			json_data['time'] = get_time() + "jkl%d"%count

		else:
			print "Unusual data : ", data
		#queue.put(json_data)
		data = json.dumps(json_data)
		print data
		socketio.emit('channel_server_to_client', data)
		count += 1
	
if __name__ == '__main__':
	thread1 = threading.Thread(target=serial_read)
	thread1.daemon = True
	thread1.start()

	#thread2 = threading.Thread(target=send_data)
	#thread2.daemon = True
	#thread2.start()

	socketio.run(app, host='', port=5000, debug=True)
