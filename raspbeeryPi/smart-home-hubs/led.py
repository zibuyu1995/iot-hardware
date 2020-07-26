import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import json


# MQTT Broker config
broker = '127.0.0.1'
port = 1883
topic = 'smartHomeHubs/led'


def on_connect(client, userdata, flags, rc):
    print("Connecting to the MQTT server...")
    if rc == 0:
        print("Connection success")
    else:
        print("Connected with result code "+str(rc))
    client.subscribe(topic)


def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    led_status = payload.get('status')
    gpio_status = GPIO.input(4)
    if led_status == 'on' and gpio_status == 0:
        GPIO.output(4, True)
        print('LED on')
    elif led_status == 'off' and gpio_status == 1:
        GPIO.output(4, False)
        print('LED off')
    else:
        pass


def run():
    # connect mqtt server
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, 1883, 60)
    # set raspberryPi GPIO pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(4, GPIO.OUT)
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == "__main__":
    run()