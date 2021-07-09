# python 3.x

import time

import Adafruit_DHT
from paho.mqtt import client as mqtt_client

BROKER = 'broker.emqx.io'
PORT = 1883
TOPIC = "emqx/temp_hum"
CLIENT_ID = "temp_hum"
USERNAME = 'emqx'
PASSWORD = 'public'
FLAG_CONNECTED = 0


def read_temp_hum():
    temp, hum = Adafruit_DHT.read_retry(11, gpio_channel)
    msg = {
        "temp": temp,
        "hum": hum
    }
    return msg


def on_connect(client, userdata, flags, rc):
    global FLAG_CONNECTED
    if rc == 0:
        FLAG_CONNECTED = 1
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code {rc}".format(rc=rc), )


def connect_mqtt():
    client = mqtt_client.Client(CLIENT_ID)
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.connect(BROKER, PORT)
    return client


def publish(client):
    while True:
        msg = read_temp_hum()
        result = client.publish(TOPIC, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print("Send `{msg}` to topic `{topic}`".format(msg=msg, topic=TOPIC))
        else:
            print("Failed to send message to topic {topic}".format(topic=TOPIC))
        time.sleep(1)


def run():
    client = connect_mqtt()
    client.loop_start()
    time.sleep(1)
    if FLAG_CONNECTED:
        publish(client)
    else:
        client.loop_stop()


if __name__ == '__main__':
    run()
