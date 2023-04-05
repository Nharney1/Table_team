import sys
import json
import paho.mqtt.client as mqtt
import csv
import time
import numpy as np 
import math
from collections import Counter
from . import Settings
from statistics import mode, StatisticsError

WALK_TO_SPEAKER = 250
ROTATE_TO_SPEAKER = 251
STUCK_BEACON = 999

closestspeakerarray = []
xstuckcounter = 0
ystuckcounter = 0

def distbetweenpoints(p1,p2):
    return math.sqrt(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))

def remove_smallest(numbers):
    smallestIndex = numbers.index(min(numbers))
    numbers[smallestIndex] = 1000
    return numbers

def closestspeaker(p1,p2):
    speaker1 = [0,0]
    speaker2 = [1.6,0]
    speaker3 = [3.15,0]
    speaker4 = [4.7,0]
    speaker5 = [6.3,0]
    speaker6 = [6.3,1.8]
    speaker7 = [6.3,3.6]
    speaker8 = [4.7,3.6]
    speaker9 = [3.15,3.6]
    speaker10 = [1.6,3.6]
    speaker11 = [0, 3.6]
    speaker12 = [0,1.8]

    computedpoint = [p1,p2]
    closestspeaker = []
    speakers = [speaker1, speaker2, speaker3, speaker4, speaker5, speaker6, speaker7, speaker8, speaker9, speaker10, speaker11, speaker12]
    disttospeakers = [distbetweenpoints(computedpoint, speaker) for speaker in speakers]
    #print(disttospeakers)
    closestspeaker.append(disttospeakers.index(min(disttospeakers)) + 1)
    disttospeakers = remove_smallest(disttospeakers)
    closestspeaker.append(disttospeakers.index(min(disttospeakers)) + 1)
    return closestspeaker

def trilateration(x1,y1,r1,x2,y2,r2,x3,y3,r3): #Based on https://www.101computing.net/cell-phone-trilateration-algorithm/
    A = 2*x2 - 2*x1
    B = 2*y2 - 2*y1
    C = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2
    D = 2*x3 - 2*x2
    E = 2*y3 - 2*y2
    F = r2**2 - r3**2 - x2**2 + x3**2 - y2**2 + y3**2
    x = (C*E - F*B) / (E*A - B*D)
    y = (C*D - A*F) / (B*D - A*E)
    return x,y

def trilateration3D(x1,y1,z1,r1,x2,y2,z2,r2,x3,y3,z3,r3):
    P1=np.array([x1,y1,z1])
    P2=np.array([x2,y2,z2])
    P3=np.array([x3,y3,z3])       
    p1 = np.array([0, 0, 0])
    p2 = np.array([P2[0] - P1[0], P2[1] - P1[1], P2[2] - P1[2]])
    p3 = np.array([P3[0] - P1[0], P3[1] - P1[1], P3[2] - P1[2]])
    v1 = p2 - p1
    v2 = p3 - p1

    Xn = (v1)/np.linalg.norm(v1)

    tmp = np.cross(v1, v2)

    Zn = (tmp)/np.linalg.norm(tmp)

    Yn = np.cross(Xn, Zn)

    i = np.dot(Xn, v2)
    d = np.dot(Xn, v1)
    j = np.dot(Yn, v2)

    X = ((r1**2)-(r2**2)+(d**2))/(2*d)
    Y = (((r1**2)-(r3**2)+(i**2)+(j**2))/(2*j))-((i/j)*(X))
    Z1 = np.sqrt(max(0, r1**2-X**2-Y**2))
    Z2 = -Z1

    K1 = P1 + X * Xn + Y * Yn + Z1 * Zn
    K2 = P1 + X * Xn + Y * Yn + Z2 * Zn
    return K1[0],K1[1]

def smoothpoint(x,y):
    computedpoint = [x,y]
    leftedge = [0,abs(y)]
    topedge = [abs(x),0]
    rightedge = [1.9202, abs(y)]
    bottomedge = [abs(x), 1.0972]
    edges = [leftedge, topedge, rightedge, bottomedge]

    #disttoedges = [0,0,0,0]
    #disttoedges[0] = abs(x-0)
    #disttoedges[1] = abs(y-0)
    #disttoedges[2] = abs(1.9304-x)
    #disttoedges[3] = abs(1.0287-y)
    disttoedges = [distbetweenpoints(computedpoint, edge) for edge in edges]
    indexmindist = disttoedges.index(min(disttoedges))
    if indexmindist == 0:
        smoothedpoint = [0, min(max(y,0),1.0972)]
    elif indexmindist == 1:
        smoothedpoint = [min(max(x,0),1.9202), 0]
    elif indexmindist == 2:
        smoothedpoint = [1.9304, min(max(y,0),1.0972)]
    elif indexmindist == 3:
        smoothedpoint = [min(max(x,0),1.9202),1.0972]

    return smoothedpoint


def get_percentage_diff(previous, current):
    try:
        percentage = (previous - current)/((previous + current)/2) * 100
    except ZeroDivisionError:
        percentage = float('inf')
    return percentage

def on_connect(mqttc, obj, flags, rc):
    print("rc: "+str(rc))

xarray = []
yarray = []

def on_message(mqttc, obj, msg):
    global closestspeakerarray
#print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    if (msg.topic == "t/sd/uwb"):
        uwbdist = json.loads(msg.payload.decode("utf-8"))["dist"]
        #print("Distances from beacons", uwbdist)
        r1 = abs(float(uwbdist.split(",")[0])) #LEMON
        r2 = abs(float(uwbdist.split(",")[1])) #COCONUT
        r3 = abs(float(uwbdist.split(",")[2])) #CARAMEL
        x1 = 0
        y1 = -0.1
        z1 = 0.762
        x2 = 1.9304 #76"
        y2 = -0.1
        z2 = 0.762
        x3 = 0.9602 #38.5"
        y3 = 1.0287#40.5"
        z3 = 0.762
        global xarray
        global yarray
        global xstuckcounter
        global ystuckcounter

        x,y = trilateration(x1,y1,r1,x2,y2,r2,x3,y3,r3)
        #x,y = trilateration3D(x1,y1,z1,r1,x2,y2,z2,r2,x3,y3,z3,r3)
        #print(x,y)

        #if abs(x - np.mean(xarray)) < 0.61:
        #   xarray.append(x)
        #if abs(y - np.mean(yarray)) < 0.61:
        #   yarray.append(y)

        if len(xarray) > 5:
            x = np.mean(xarray)
            y = np.mean(yarray)
            xstuckcounter += len(set(xarray))
            ystuckcounter += len(set(yarray))
            #print("Before smoothing in meters", [x,y])
            arraydist = np.round(smoothpoint(x,y),2)
            arraydistfeet = np.round([r*3.28084 for r in arraydist],2)
            #print("After smoothing in meters", arraydist)
            #print("After smoothing in feet", arraydistfeet)
            currentclosestspeaker = closestspeaker(arraydistfeet[0],arraydistfeet[1])
            closestspeakerarray.append(currentclosestspeaker[0])
            closestspeakerarray.append(currentclosestspeaker[1])

            if len(closestspeakerarray) == 6:
                if xstuckcounter <= 3 or ystuckcounter <= 3:
                    ret = mqttc.publish("t/sd/feedback", STUCK_BEACON)
                    time.sleep(3)

                xstuckcounter = 0
                ystuckcounter = 0
                print("Array of closest speakers is", closestspeakerarray)
                uniqueitems = Counter(closestspeakerarray).keys()
                if len(uniqueitems) >= 5:
                    closestspeakerarray.pop(0)
                    closestspeakerarray.pop(0)

                else:
                    finalclosestspeaker = []
                    try:
                        finalclosestspeaker.append(mode(closestspeakerarray))
                        closestspeakerarray = [el for el in closestspeakerarray if el != mode(closestspeakerarray)]
                        finalclosestspeaker.append(mode(closestspeakerarray))
                    except StatisticsError:
                        temp = Counter(closestspeakerarray)
                        finalclosestspeaker_freq = temp.most_common(2)
                        finalclosestspeaker = [speak[0] for speak in finalclosestspeaker_freq]

                    print("Closest speaker is", finalclosestspeaker)
                    Settings.MQTT_Lock.acquire()
                    if sorted(Settings.MQTT_Speakers) != sorted(finalclosestspeaker):
                        Settings.MQTT_Speakers = sorted(finalclosestspeaker)
                        Settings.MQTT_UpdateFlag = True
                    Settings.MQTT_Lock.release()

                    closestspeakerarray = []
        if len(xarray) > 5:
            xarray = []
        if len(yarray) > 5:
            yarray = []

        xarray.append(x)
        yarray.append(y)

def on_publish(mqttc, obj, mid):
    print("mid: "+str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)

def MQTT_Main():
    print("Starting MQTT thread")
    mqttc = mqtt.Client(transport='websockets')   
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe

    mqttc.connect('broker.emqx.io', 8083, 60)
    mqttc.subscribe("t/sd/uwb", 0)
    mqttc.subscribe("t/sd/feedback", 0)
    #mqttc.subscribe("$SYS/#", 0)
    #ret= mqttc.publish("t/sd/feedback","L")                   #publish
    mqttc.loop_forever()
