import urllib
import urllib2
from lxml import etree
from http import cookiejar
import time

def myget_time():
    t1 = time.localtime()
    return "%s-%s-%s %s:%s:%s -->" % (t1.tm_year, t1.tm_mon, t1.tm_mday, t1.tm_hour, t1.tm_min, t1.tm_sec)

def openUrl(url, data):
    cookie = cookiejar.MozillaCookieJar()
    cookie.load('cookie')
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)
    headers = {
        'User-Agnet' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
    data = urllib.urlencode(data).encode('utf-8')
    req = urllib2.Request(url, data, headers=headers)
    try:
        response = urllib2.urlopen(req)
        html = response.read().decode('utf-8')
        return html
    except urllib2.URLError as e:
        if hasattr(e, 'code'):
            print('HTTPError:%d' % e.code)
        elif hasattr(e, 'reason'):
            print('URLError:%s' % e.reason)

def get_current_reservation(equipment_id, date):
    print("get_current_reservation("+equipment_id+", "+date+")")
    url = 'http://www.synl.ac.cn:8090/tsd/Wap/Sub/detail/id/' + str(equipment_id)
    html = openUrl(url, {})
    if html:
        root = etree.HTML(html)
        table_root = root.xpath('/html/body/div[2]/div[1]/div[1]/div[3]/div[2]/div[2]')[0]
        target_day = time.strptime(date,"%Y-%m-%d")
        days_from_today = int(time.strftime('%j', target_day)) - int(time.strftime('%j'))
        num_ul = days_from_today / 3 + 1
        num_li = days_from_today % 3 + 1
        with open('log.log', 'a') as f:
            f.write('\r\n\r\nCurrent time: ' + myget_time() + '\r\n')
            f.write('get_current_reservation.target_day=' + str(target_day) + '\r\n')
            f.write('get_current_reservation.date=' + str(date) + '\r\n')
            f.write('get_current_reservation.num_ul=' + str(num_ul) + '\r\n')
            f.write('get_current_reservation.num_li=' + str(num_li) + '\r\n')
        target_day_root = table_root.xpath('ul[%s]/li[%s]/dl[1]' % (num_ul, num_li))[0]
        dds = range(24)
        for i in range(24):
            dd = target_day_root.xpath('dd[%s]/span/div' % (i+1))
            if dd:
                dds[i] = "yes"
            else:
                dds[i] = "no"
    else:
        dds = get_current_reservation(equipment_id)

    with open('log.log', 'a') as f:
        f.write('get_current_reservation.dds=' + str(dds) + '\r\n')
    return dds

def get_empty_time(equipment_id, date):
    dds = get_current_reservation(equipment_id, date)
    flag = "yes"
    dds_arr = []
    for i in range(24):
        if dds[i] != flag:
            flag = "no" if flag == "yes" else "yes"
            dds_arr.append({'start':i, 'end':i+1, 'state':flag})
        else:
            dds_arr[-1]['end'] = i+1

    with open('log.log', 'a') as f:
        f.write('get_empty_time.dds_arr=' + str(dds_arr) + '\r\n')
    return dds_arr

if __name__ == '__main__':
    dds_arr = get_empty_time('22', date='2018-7-3')

            
            
    
