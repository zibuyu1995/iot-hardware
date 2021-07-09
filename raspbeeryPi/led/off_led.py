from RPi import GPIO


def led_off():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, GPIO.LOW)
    print('LED off')


if __name__ == '__main__':
    led_off()
