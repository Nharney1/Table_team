def InitializeGlobals():
	global connected
	global monitor
	global bt_thread
	global notification_cb_set
	global noah_char
	global pause

	connected = False
	monitor = None #This is a temporary name for the client/Central object
	bt_thread = None
	notification_cb_set = False
	noah_char = None
	pause = False
	print("GLOBALS DONE")