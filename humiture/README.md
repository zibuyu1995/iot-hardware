# 树莓派获取温湿度数据上传到 actorcloud

### 环境安装:
```
pip install -r requirements.txt
```
### 修改配置文件
需要修改设备id 用户名 密码 温湿度上传间隔
```
vi config.py
```
### 运行:
```
python mqtt_publish.py
```
### Reference:
[actorcloud](https://www.actorcloud.io/)
[Adafruit-DHT](https://github.com/adafruit/Adafruit_Python_DHT)

