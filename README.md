# auto-order-equipment
Auto order equipments for tsd system in IMR

程序会先获取需要预约的那天的设备预约情况，然后预约8：00-23：00之间空闲的时间。
如果空闲时间为0：00-12：00，程序会预约8：00-12：00这一时间段。

# 实例1：
order_client.exe run 28

run为必须的参数
28为1号线切割的id
自动预约13天后的设备

# 实例2：
order_client.exe run 28 2018-7-6

run为必须的参数
28为1号线切割的id
预约2018-7-6当天的设备
