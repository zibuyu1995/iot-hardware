import json
import time

import smbus
from paho.mqtt import client as mqtt


# BH1750FVI config
DEVICE = 0x23  # Default device I2C address
POWER_DOWN = 0x00
POWER_ON = 0x01
RESET = 0x07
CONTINUOUS_LOW_RES_MODE = 0x13
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
ONE_TIME_HIGH_RES_MODE_1 = 0x20
ONE_TIME_HIGH_RES_MODE_2 = 0x21
ONE_TIME_LOW_RES_MODE = 0x23
bus = smbus.SMBus(1)

# MQTT Broker config
broker = '127.0.0.1'
port = 1883
topic = 'smartHomeHubs/light'


def read_light():
    data = bus.read_i2c_block_data(DEVICE, ONE_TIME_HIGH_RES_MODE_1)
    light_level = round((data[1] + (256 * data[0])) / 1.2, 2)
    return light_level


def connect_mqtt():
    client = mqtt.Client(client_id='light_01')
    client.connect(host=broker, port=port)
    return client


def run():
    mqtt_client = connect_mqtt()
    while True:
        light_level = read_light()
        publish_msg = {'lightLevel': light_level}
        mqtt_client.publish(
            topic,
            payload=json.dumps(publish_msg)
        )
        print(publish_msg)
        time.sleep(1)


if __name__ == "__main__":
    run()
