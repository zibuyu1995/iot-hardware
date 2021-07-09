from RPi import GPIO


def led_on():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, GPIO.HIGH)
    print('LED on')


if __name__ == '__main__':
    led_on()
