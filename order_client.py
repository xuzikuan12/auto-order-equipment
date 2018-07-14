# -*- coding: gbk -*-

import tsd
import sys
import time
from lxml import etree

equipments_data = {}
equipments_data['28'] = '1#数控伺服中走丝线切割机'
equipments_data['22'] = '场发射透射电镜(F20)-143'
secs = 13 * 24 * 3600 # 计算预约时间，提前 13 天预约
date = time.localtime( (time.time() + secs))
date = "%s-%s-%s" % (date.tm_year, date.tm_mon, date.tm_mday)

def write_log(msg):
    log_this = tsd.myget_time() + msg + '\r\n'
    with open('log.log', 'a') as f:
        f.write(log_this)
    print(log_this)    

def order_client(equipment_id, date=date):
    dds_arr = tsd.get_empty_time(equipment_id, date)
    executed = False
    for dd in dds_arr:
        if dd['state'] == 'no' and dd['end'] < 24:
            if dd['start'] < 8:
                dd['start'] = 8
            data = {}
            data['id'] = equipment_id
            data['sdates'] = date
            data['stimes'] = '%s:00' % dd['start']
            data['edates'] = date
            data['etimes'] = '%s:00' % dd['end']
            data['nums'] = '1'
            data['bz'] = ''
            msg = order_equipment(equipment_id, date=date, data=data)
            if msg == '预约成功'.decode('ISO-8859-1'):
                write_log('设备 %s 预约成功，日期为 %s' % (equipments_data[equipment_id], date))
                executed = True
            else:
                write_log('预约失败！设备: %s , msg: %s' % (equipments_data[equipment_id], msg.encode('gbk')))

    if not executed:
        msg = "there is no suitalbe time"
        write_log('预约失败！设备: %s , msg: %s' % (equipments_data[equipment_id], msg.encode('gbk')))

def order_equipment(equipment_id, date=date, data={}):
    print("order_equipment("+equipment_id+", "+date+", "+str(data)+")")
    if data == {}:
        data['id'] = equipment_id
        data['sdates'] = date
        data['stimes'] = '08:00'
        data['edates'] = date
        data['etimes'] = '23:00'
        data['nums'] = '1'
    if len(sys.argv) > 1 and sys.argv[1] == 'run':
        data['bz'] = ''
    else:
        return 'This is the test code, if you want to run this program, put "run" at first argument positon'
    url = 'http://www.synl.ac.cn:8090/tsd/Wap/Sub/detail/id/' + str(equipment_id)
    with open('log.log', 'a') as f:
        f.write('order_equipment.url=' + str(url) + '\r\n')
        f.write('order_equipment.data=' + str(data) + '\r\n')
    html = tsd.openUrl(url, data)
    root = etree.HTML(html)
    msg = root.xpath('/html/body/div/div[2]/text()')[0]
    return msg

if __name__ == '__main__':
    if len(sys.argv) ==  1:
        order_client('28');
    else:
        if sys.argv[1] != 'run':
            print('put "run" at first argument positon')
        else:
            if len(sys.argv) == 4:
                order_client(sys.argv[2], sys.argv[3])
            else:
                order_client(sys.argv[2])
