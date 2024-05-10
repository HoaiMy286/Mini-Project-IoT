import sys
import cv2  # Install opencv-python
import os
import time
import random
import datetime

from Adafruit_IO import MQTTClient
from simple_ai import *
from uart import *

AIO_FEED_IDs = ["led", "pump"]
# infor user Adafruit

def connected(client):
    print("Ket noi thanh cong ...")
    for topic in AIO_FEED_IDs:
        client.subscribe(topic)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

previous_led_status = None

def message(client , feed_id , payload):
    global previous_led_status 
    print("Nhan du lieu: " + payload + ", feed id: " + feed_id)
    if feed_id == "led":
        if payload == "0":  # OFF
            writeData("Led_OFF")
            previous_led_status = 0 
        else:               # ON
            writeData("Led_ON")
            previous_led_status = 1
    if feed_id == "pump":
        if payload == "0":  # OFF
            writeData("Pump_OFF") 
        else:               # ON
            writeData("Pump_ON")     

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

counter = 10
sensor_type = 0

counter_ai = 5
ai_result = ""
previous_ai_result = ""

def control_light():
    global previous_led_status 
    now = datetime.datetime.now()
    
    # LED ON (22h00)
    if now.hour == 12 and now.minute == 16 and previous_led_status != 1:
    # if now.hour == 22 and now.minute == 0:
        client.publish("led", "1") 
        previous_led_status = 1
    
    # LED OFF (5h00)
    elif now.hour == 12 and now.minute == 17 and previous_led_status != 0:
    # elif now.hour == 5 and now.minute == 0:
        client.publish("led", "0")
        previous_led_status = 0

# Main loop

while True:  
    readSerial(client)
    control_light()

    counter_ai = counter_ai - 1
    if counter_ai <= 0:
        counter_ai = 5

        previous_ai_result = ai_result
        ai_result = image_detector()
        print("AI Output: ", ai_result)

        if ai_result != previous_ai_result:
            client.publish("ai", ai_result)

    time.sleep(1)
