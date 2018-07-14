# auto-order-equipment
Auto order equipments for TSD system of IMR  
程序会先获取需要预约的那天的设备预约情况，然后预约8：00-23：00之间空闲的时间。
## cookie 获取
登陆手机版网页：http://www.synl.ac.cn:8090/tsd/Wap/Index/login  
使用F12->console 输入 document.cookie 回车即可获得cookie，按照示例文件填写即可。  
## 使用
下载 order_client.exe， equipments.pkl 和 cookie，修改cookie后即可使用。
## 情况1：
如果空闲时间为0：00-12：00，程序会预约8：00-12：00这一时间段。
## 情况2：
如果空闲时间为0：00-24：00，程序会预约8：00-23：00这一时间段。
## 情况3：
如果空闲时间为0：00-8：00 或者 23:00-24:00，则程序会提示找不到合适的时间。
## 实例1：
`order_client.exe run 28`  
run为必须的参数  
28为1号线切割的id  
自动预约13天后的设备  
## 实例2：
`order_client.exe run 28 2018-7-6`  
run为必须的参数  
28为1号线切割的id  
预约2018-7-6当天的设备  
