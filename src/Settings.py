import threading

def InitializeGlobals():
	global connected
	global monitor
	global bt_thread
	global notification_cb_set
	global esp_char
	global pause
	global MQTT_Speakers
	global MQTT_UpdateFlag
	global MQTT_Lock
	global PCBPauseGame
	global PCBEndGame

	connected = False
	monitor = None # This is a temporary name for the client/Central object
	bt_thread = None
	notification_cb_set = False
	esp_char = None
	pause = False
	MQTT_Speakers = None
	MQTT_UpdateFlag = True
	MQTT_Lock = threading.Lock()
	PCBPauseGame = False
	PCBEndGame = False
	print("GLOBALS DONE")
