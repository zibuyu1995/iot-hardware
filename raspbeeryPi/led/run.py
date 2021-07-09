import json

from RPi import GPIO
from paho.mqtt import client as mqtt_client

# EMQ X Cloud Deployment config
BROKER = 'broker.emqx.io'
PORT = 1883
TOPIC = "emqx/led"
CLIENT_ID = "emqx-led"
USERNAME = 'emqx'
PASSWORD = 'public'


def led_on():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, GPIO.HIGH)
    print('LED on')


def led_off():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, GPIO.LOW)
    print('LED off')


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(TOPIC)
    else:
        print("Failed to connect, return code {rc}".format(rc=rc), )


def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print("Received `{payload}` from `{topic}` topic".format(payload=payload, topic=msg.topic))
    msg_dict = json.loads(payload)
    action = msg_dict.get('action')
    if action == 'on':
        led_on()
    elif action == 'off':
        led_off()
    else:
        pass


def connect_mqtt():
    client = mqtt_client.Client(CLIENT_ID)
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT)
    return client


def run():
    client = connect_mqtt()
    client.loop_forever()


if __name__ == '__main__':
    run()
