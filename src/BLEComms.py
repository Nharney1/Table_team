"""Example of how to create a Central device/GATT Client"""
import struct
import threading
import time

from bluezero import adapter
from bluezero import central
from enum import IntEnum

from . import Settings

SEND_SPEAKERS = 100

ESP_SERVER_UUID = "df9f28cb-9b6a-4c8f-a3ff-8f087738c90a"
ESP_UUID = "7bb6db74-6c47-4722-bb33-bfa652f64713"

def on_disconnect(self):
    print('Disconnected!')  
    print('Stopping notify')
    for character in Settings.monitor._characteristics:
        character.stop_notify()  
    print('Disconnecting...')  
    Settings.monitor.disconnect()   

    Settings.monitor.quit() #bt_thread should exit after this
    
    #flag setting
    Settings.connected = False
    print( f"The thread is {Settings.bt_thread}")

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
            if ESP_SERVER_UUID.lower() in dev.uuids:
                print('Found our device!')
                Settings.bt_thread = threading.Thread(target=connect_and_run, args=[dev])
                Settings.bt_thread.start()
                print(f"Just started thread {Settings.bt_thread}")
                break
        break

def scan_for_devices(
        adapter_address=None,
        device_address=None,
        timeout=5.0):

    # If there are multiple adapters on your system, this will scan using
    # all dongles unless an adapter is specified through its MAC address
    for dongle in adapter.Adapter.available():
        # Actually listen to nearby advertisements for timeout seconds
        dongle.nearby_discovery(timeout=timeout)

        # Iterate through discovered devices
        for dev in central.Central.available(dongle.address):
            if  dev.name == "NOAH_ESP32":
                print(str(dev.name))
                for uuid in dev.uuids:
                    print(uuid)

            # Otherwise, return devices that advertised the HRM Service UUID
            if ESP_SERVER_UUID.lower() in dev.uuids:
                print("Found a device with the SRV uuid. Yielding it...")
                yield dev

def on_new_noah(iface, changed_props, invalidated_props):
    value = changed_props.get('Value', None)
    if not value:
        print("\'Value\' not found!")
        return

    retVal = int(value[0])

    print("Got value "  + str(retVal))
    # Update global state here


def connect_and_run(dev=None, device_address=None):

    if dev:
        print('Dev is being used')
        if Settings.monitor is None: #ADDED this IF
            print('Creating new Central Object...')
            Settings.monitor = central.Central(
                adapter_addr=dev.adapter,
                device_addr=dev.address)
            #Add the following here instead of after the else
            print('Central created! Adding characteristics...')
            # Characteristics that we're interested must be added to the Central
            # before we connect so they automatically resolve BLE properties
            # Heart Rate Measurement - notify
            Settings.esp_char = Settings.monitor.add_characteristic(ESP_SERVER_UUID, ESP_UUID)
    else:
        Settings.monitor = central.Central(device_addr=device_address)

    # Now Connect to the Device
    if dev:
        print("Connecting to " + dev.alias)
    else:
        print("Connecting to " + device_address)

    Settings.monitor.connect()
    
    # Check if Connected Successfully
    if not Settings.monitor.connected:
        print("Didn't connect to device!")
        return

    Settings.connected = True
    Settings.monitor.dongle.on_disconnect = on_disconnect
    print('Connection successful!')

    Settings.esp_char.start_notify()

    if not Settings.notification_cb_set:
        print('Setting callback for notifications')
        Settings.esp_char.add_characteristic_cb(on_new_noah)
        Settings.notification_cb_set = True

    try:
        # Startup in async mode to enable notify, etc
        Settings.monitor.run()
    except KeyboardInterrupt:
        print("Disconnecting")

    Settings.connected = False
    Settings.monitor.disconnect()
    Settings.monitor.quit()

def Init_BLE():
    # Discovery nearby heart rate monitors
    print("Scanning for devices")
    devices = scan_for_devices()
    for dev in devices:
        if dev:
            print("Device Found!")

        Settings.bt_thread = threading.Thread(target=connect_and_run, args=[dev])
        Settings.bt_thread.start()
        print( f"The thread is {Settings.bt_thread}")
        return
        # Only demo the first device found
        #TODO For now we break after first one

def SendCommand(command, argList):
    if command == SEND_SPEAKERS:
        Settings.esp_char.write_value(SEND_SPEAKERS.to_bytes(1,byteorder='big', signed=False))
        if len(argList) == 1:
            # We only really need one speaker, but to be compliant for the ESP32 state machine send it twice
            Settings.esp_char.write_value(argList[0].to_bytes(1,byteorder='big', signed=False))
            Settings.esp_char.write_value(argList[0].to_bytes(1,byteorder='big', signed=False))
        elif len(arglist) == 2:
            # We need to play two different speakers
            Settings.esp_char.write_value(argList[0].to_bytes(1,byteorder='big', signed=False))
            Settings.esp_char.write_value(argList[1].to_bytes(1,byteorder='big', signed=False))

