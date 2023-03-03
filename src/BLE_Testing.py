"""Example of how to create a Central device/GATT Client"""
from enum import IntEnum
import struct

from bluezero import adapter
from bluezero import central
import threading
import time 


NOAH_SERVER_UUID = "df9f28cb-9b6a-4c8f-a3ff-8f087738c90a"
NOAH_UUID = "7bb6db74-6c47-4722-bb33-bfa652f64713"

connected = False
monitor = None #This is a temporary name for the client/Central object
bt_thread = None
notification_cb_set = False
noah_char = None

def on_disconnect(self):
    global bt_thread
    """Disconnect from the remote device."""
    print('Disconnected!')  
    print('Stopping notify')
    for character in monitor._characteristics:
        character.stop_notify()  
    print('Disconnecting...')  
    monitor.disconnect()   

    monitor.quit() #bt_thread should exit after this
    
    #flag setting
    global connected
    connected = False
    print( f"The thread is {bt_thread}")

    return 

    #Attempt to scan and reconnect
    print("Server disconnected. Sleeping for five seconds, then attemting to reconnect...")
    time.sleep(5)
    for dongle in adapter.Adapter.available():
        devices = central.Central.available(dongle.address)
        while not devices:
            print("Cannot find server. Sleeping for 2s...")
            time.sleep(2)
            devices = scan_for_devices()
            print('Found our device!')
        for dev in devices:
            if NOAH_SERVER_UUID.lower() in dev.uuids:
                print('Found our device!')
                bt_thread = threading.Thread(target=connect_and_run, args=[dev])
                bt_thread.start()
                print(f"Just started thread {bt_thread}")
                break
        break

def scan_for_devices(
        adapter_address=None,
        device_address=None,
        timeout=5.0):
    """
    Called to scan for BLE devices advertising the Heartrate Service UUID
    If there are multiple adapters on your system, this will scan using
    all dongles unless an adapter is specfied through its MAC address
    :param adapter_address: limit scanning to this adapter MAC address
    :param hrm_address: scan for a specific peripheral MAC address
    :param timeout: how long to search for devices in seconds
    :return: generator of Devices that match the search parameters
    """
    # If there are multiple adapters on your system, this will scan using
    # all dongles unless an adapter is specified through its MAC address
    for dongle in adapter.Adapter.available():
        # Filter dongles by adapter_address if specified
        if adapter_address and adapter_address.upper() != dongle.address():
            continue
        #MENA reset before scanning to not pickup old results
       # central.Central.available(dongle.address) = None

        # Actually listen to nearby advertisements for timeout seconds
        dongle.nearby_discovery(timeout=timeout)

        # Iterate through discovered devices
        for dev in central.Central.available(dongle.address):
            if  dev.name == "NOAH_ESP32":
                print(str(dev.name))
                for uuid in dev.uuids:
                    print(uuid)

            # Otherwise, return devices that advertised the HRM Service UUID
            if NOAH_SERVER_UUID.lower() in dev.uuids:
                print("Found a device with the SRV uuid. Yielding it...")
                yield dev

def on_new_noah(iface, changed_props, invalidated_props):
    value = changed_props.get('Value', None)
    if not value:
        print("\'Value\' not found!")
        return

    retVal = int(value[0])

    print("Got value "  + str(retVal))
    # number = int(value[0])
    # x = 5
    #  noah_char.write_value(x.to_bytes(1,byteorder='big', signed=False))
    # Only update the global here, do the actual writing in main



def connect_and_run(dev=None, device_address=None):
    """
    Main function intneded to show usage of central.Central
    :param dev: Device to connect to if scan was performed
    :param device_address: instead, connect to a specific MAC address
    """
    # Create Interface to Central
    global noah_char

    if dev:
        print('Dev is being used')
        global monitor
        if monitor is None: #ADDED this IF
            print('Creating new Central Object...')
            monitor = central.Central(
                adapter_addr=dev.adapter,
                device_addr=dev.address)
            #Add the following here instead of after the else
            print('Central created! Adding characteristics...')
            # Characteristics that we're interested must be added to the Central
            # before we connect so they automatically resolve BLE properties
            # Heart Rate Measurement - notify
            noah_char = monitor.add_characteristic(NOAH_SERVER_UUID, NOAH_UUID)
    else:
        monitor = central.Central(device_addr=device_address)

    # Now Connect to the Device
    if dev:
        print("Connecting to " + dev.alias)
    else:
        print("Connecting to " + device_address)
    monitor.connect()
    
    # Check if Connected Successfully
    if not monitor.connected:
        print("Didn't connect to device!")
        return
    global connected
    connected = True
    monitor.dongle.on_disconnect = on_disconnect
    print('Connection successful!')

    # Enable heart rate notifications
    noah_char.start_notify()

    global notification_cb_set
    if not notification_cb_set:
        print('Setting callback for notifications')
        noah_char.add_characteristic_cb(on_new_noah)
        notification_cb_set = True

    try:
        # Startup in async mode to enable notify, etc
        monitor.run()
    except KeyboardInterrupt:
        print("Disconnecting")

    connected = False
    monitor.disconnect()
    monitor.quit()


if __name__ == '__main__':
    # Discovery nearby heart rate monitors
    print("Scanning for devices")
    devices = scan_for_devices()
    for dev in devices:
        if dev:
            print("Device Found!")

        #global bt_thread
        bt_thread = threading.Thread(target=connect_and_run, args=[dev])
        bt_thread.start()
        print( f"The thread is {bt_thread}")
        while True:
            while connected:
                for i in range(3):
                    x = 6
                    noah_char.write_value(x.to_bytes(1,byteorder='big', signed=False))
                time.sleep(4)
                prior_connection = True
            while not connected:
                print("Waiting for connection")
                time.sleep(2)

        # Only demo the first device found
        #TODO For now we break after first one
