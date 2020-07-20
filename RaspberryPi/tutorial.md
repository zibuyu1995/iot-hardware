# 利用树莓派构建私有智能家居网关

智能家居网关是所有智能家居的核心大脑，通过它可以实现智能家居设备信息的采集、远程控制、智能联动控制等功能。我们在享受智能家居带来的便利时也应该思考：是否愿意智能家居厂商收集有关于我们生活习惯等私密信息？在本项目中我们将尝试使用 RaspberryPi + EMQ X Edge  + Kuiper 实现私有家庭智能网关，并实现光照强度与led灯联动控制。

## 所需组件

### RaspberryPi 3b+ 以及更高版本

### EMQ X Edge

EMQ X Edge 是轻量级多协议物联网边缘消息中间件，支持部署在资源受限的物联网边缘硬件。支持 MQTT, CoAP, HTTP 以及 Modbus 等协议。

### EMQ X Kuiper

通过实时分析家居采集的各类数据，将重要的结果通过本地显示设备，或者通过云端发送给用户的手机应用，实现对家庭设备的即时状态管理与控制

### BH1750FVI 光照传感器

文字介绍

### LED 灯

文字介绍

### 330 Ω电阻

文字介绍

### 面包板, 跳线若干

文字介绍



## 环境搭建？

### 电路连接

BH1750FVI、LED 与树莓派连接（怎么链接？加个图？）

### 树莓派配置



### EMQ X edge 安装与运行（安装在哪里？）

```bash
$ mkdir ~/smart-home-hubs
$ cd ~/smart-home-hubs
# 替换 raspbian8 为你系统版本
$ wget https://www.emqx.io/downloads/edge/v4.1.0/emqx-edge-raspbian8-v4.1.0.zip
$ unzip emqx-edge-raspbian8-v4.1.0.zip
$ cd ./emqx
# run emqx 
$ ./bin/emqx start
# output: EMQ X Edge v4.1.0 is started successfully!
```

### EMQ X Kuiper 安装与运行（安装在哪里？）

```bash
# 下载软件包
$ wget https://github.com/emqx/kuiper/releases/download/0.4.2/kuiper-0.4.2-linux-armv7l.zip
$ unzip kuiper-0.4.2-linux-armv7l.zip
$ mv kuiper-0.4.2-linux-armv7l ./kuiper
$ cd ./kuiper
$ mkdir ./rules
$ ./bin/server
```

## 代码编写

### BH1750FVI 光照传感器数据上传

编写代码读取并计算 BH1750FVI 传感器光照强度数据，并将光照强度数据通过 **MQTT** 协议发布到 **smartHomeHubs/light** 主题上

```python
# gy30.py
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

```

### 配置 Kuiper 流处理规则

创建 Kuiper 流以及规则

- 创建流

  ```bash
  $ cd ~/smart-home-hubs/kuiper
  
  $ ./bin/cli create stream smartHomeHubs '(lightLevel float) WITH (FORMAT="JSON", DATASOURCE="smartHomeHubs/light")'
  ```

- 查询流数据

  ```bash
  ./bin/cli query
  > select * from smartHomeHubs
  ```

- 编写开启 led 规则(onLed.rule)

  当光照强度小于55时将向 ``smartHomeHubs/led` 主题发送 `"{\"status\": \"on\"}"` 消息

  ```
  {
     "sql":"SELECT * from smartHomeHubs where lightLevel < 55 ",
     "actions":[
        {
           "mqtt":{
              "server":"tcp://127.0.0.1:1883",
              "topic":"smartHomeHubs/led",
              "sendSingle":true,
              "dataTemplate": "{\"status\": \"on\"}"
           }
        }
     ]
  }
  ```

- 编写关闭 led 规则(offLed.rule)

  当光照强度大于 55 时将向 ``smartHomeHubs/led` 主题发送 `"{\"status\": \"off\"}"` 消息

  ```
  {
     "sql":"SELECT * from smartHomeHubs where lightLevel > 55 ",
     "actions":[
        {
           "mqtt":{
              "server":"tcp://127.0.0.1:1883",
              "topic":"smartHomeHubs/led",
              "sendSingle":true,
              "dataTemplate": "{\"status\": \"off\"}"
           }
        }
     ]
  }
  ```

- 添加规则

  ```bash
  $ ./bin/cli create rule onLed -f ./rules/onLed.rule 
  $ ./bin/cli create rule onLed -f ./rules/offLed.rule 
  ```

  

### LED 灯控制

编写 LED 控制代码（简单一段文字说明下这段代码）

```python
# led.py
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

```



## 运行测试

1. `python gy30.py` 获取当前光照数据

   ![gy30](/Users/mousse/Library/Containers/com.tencent.xinWeChat/Data/Library/Application%20Support/com.tencent.xinWeChat/2.0b4.0.9/6d2e1af87f56639d2fba9f1c1afe63ac/Message/MessageTemp/9fff9cf7b7aa518ae093ec5ed6d9253f/File/_assets/gy30.png)

2. `python led.py` 获取 `led  `控制信息

   ![led](/Users/mousse/Library/Containers/com.tencent.xinWeChat/Data/Library/Application%20Support/com.tencent.xinWeChat/2.0b4.0.9/6d2e1af87f56639d2fba9f1c1afe63ac/Message/MessageTemp/9fff9cf7b7aa518ae093ec5ed6d9253f/File/_assets/led.png)

3. 测试
   ​![gy30_control](/Users/mousse/Library/Containers/com.tencent.xinWeChat/Data/Library/Application%20Support/com.tencent.xinWeChat/2.0b4.0.9/6d2e1af87f56639d2fba9f1c1afe63ac/Message/MessageTemp/9fff9cf7b7aa518ae093ec5ed6d9253f/File/_assets/gy30_control.png)
   ![led_control]()