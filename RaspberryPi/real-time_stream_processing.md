如何使用 EMQX + Kuiper 在树莓派上进行物联网实时流计算

整体思路是:
温度传感器上报温度 到 emqx broker， Kuiper 订阅到消息, 验证规则: 持续温度超过多少，调用http发送告警
 