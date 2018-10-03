#!/usr/bin/python
# coding=utf-8

import json

from config import (
    broker_host, broker_port, broker_keepalive,
    client_id, username, password
)
from led_control import led_turn, led_off
from paho.mqtt import client as mqtt


# 连接回调接口
def on_connect(client, userdata, flags, rc):
    print("Connecting to the MQTT server...")
    if rc == 0:
        print("Connection success")
    else:
        print("Connected with result code "+str(rc))


def on_message(client, userdata, msg):
    print("Topic: " + msg.topic+"Message: "+str(msg.payload))
    payload = json.loads(msg.payload)
    led_status = payload.get('led')
    if led_status is None:
        client.disconnect()
    elif led_status:
        led_turn()
    else:
        led_off()


# mqtt 连接
def connect_mqtt():
    client = mqtt.Client(client_id=client_id)
    client.username_pw_set(username, password)
    client.connect(broker_host, broker_port, broker_keepalive)
    client.on_connect = on_connect
    client.subscribe('led', qos=1)
    client.on_message = on_message
    client.loop_forever()


if __name__ == '__main__':
    connect_mqtt()
