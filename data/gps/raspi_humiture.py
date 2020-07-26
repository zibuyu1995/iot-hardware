#!/usr/bin/python
# coding=utf-8

import Adafruit_DHT
from config import gpio_channel


def humiture():
    # dht11, gpio 4
    humidity, temperature = Adafruit_DHT.read_retry(11, gpio_channel)
    return temperature, humidity
