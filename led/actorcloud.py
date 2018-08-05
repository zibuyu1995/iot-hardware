# coding: utf-8

"""

 @filename: actorcloud.py
 @Time: 2018/7/21 12:00
 @Author: EMQ_Mousse

"""

import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


client = mqtt.Client(client_id='raspberrypitemp')
client.username_pw_set("raspberrypitemp", "raspberrypitemp")
client.on_connect = on_connect
client.on_message = on_message

client.connect("iot.actorcloud.io", 1883, 60)

client.loop_forever()
