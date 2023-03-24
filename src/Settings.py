import threading

def InitializeGlobals():
	global connected
	global monitor
	global bt_thread
	global notification_cb_set
	global noah_char
	global pause
	global MQTT_Location
	global MQTT_Lock

	connected = False
	monitor = None #This is a temporary name for the client/Central object
	bt_thread = None
	notification_cb_set = False
	noah_char = None
	pause = False
	MQTT_Location = None
	MQTT_Lock = threading.lock()
	print("GLOBALS DONE")
