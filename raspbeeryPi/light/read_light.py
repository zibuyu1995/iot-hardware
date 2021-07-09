# python 3.x

# EMQ X Cloud Deployment config
BROKER = 'broker.emqx.io'
PORT = 1883
TOPIC = "emqx/light"
CLIENT_ID = "emqx-light"
USERNAME = 'emqx'
PASSWORD = 'public'
FLAG_CONNECTED = 0

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

# init
bus = smbus.SMBus(1)


def read_light():
    data = bus.read_i2c_block_data(DEVICE, ONE_TIME_HIGH_RES_MODE_1)
    light_level = round((data[1] + (256 * data[0])) / 1.2, 2)
    print(light_level)
    msg = {
        "light": light_level
    }
    return msg


if __name__ == '__main__':
    read_light()
