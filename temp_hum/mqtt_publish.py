# coding=utf-8

import paho.mqtt.client as mqtt
import json
import time
import threading
from random import randint
from temp_hum import temp_and_hum

def on_connect(client, userdata, flags, rc):
    temperature, humidity = temp_and_hum()
    client.publish('temp_hum', payload=json.dumps({"temperature": temperature, "humidity": humidity}), qos=1)
    print("Connected with result code "+str(rc))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


def on_publish(client, userdata, mid):
    print mid
    # client.disconnect()


def connect_test():
    client = mqtt.Client(client_id='raspberrypitemp')
    client.username_pw_set('raspberrypitemp', 'raspberrypitemp')
    client.on_connect = on_connect
    # client.on_publish = on_publish
    client.connect("139.198.190.35", 1883, 60)
    client.loop_forever()


# thread_list = []
# for i in range(10):
#     t = threading.Thread(target=test_connect)
#     thread_list.append(t)
#
# for task in thread_list[:3]:
#     time.sleep(0.5)
#     task.start()
connect_test()
