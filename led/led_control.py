#!/usr/bin/env python
# coding: utf-8

import time

from RPi import GPIO


def led_turn():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(4, GPIO.OUT)
    print('LED on')
    GPIO.output(4, GPIO.HIGH)


def led_off():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.output(4, GPIO.HIGH)
    print('LED off')
    GPIO.output(4, GPIO.LOW)
