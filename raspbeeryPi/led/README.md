# 远程控制树莓派led 开关
> 编写人: Mousse
> 联系邮箱: zibuyu1995@gmail.com

### 环境安装:
```
pip install -r requirements.txt
```
### 连接图
![LED](https://user-images.githubusercontent.com/17525759/46397023-a4f36f00-c723-11e8-9224-52df300188ce.png)

### 修改配置文件
需要修改设备id 用户名 密码 温湿度上传间隔, gpio口(默认4)
```
vi config.py
```
### 运行:
```
python mqtt_subscribe.py
```
### Reference:
* [actorcloud](https://www.actorcloud.io/)
