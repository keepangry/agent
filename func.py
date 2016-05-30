from random import choice, uniform
import time

SUCCESS = 0
FAILED = -1


# 随机生成head
def gene_headers():
    ua = [
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
        'User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
        'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)'
    ]

    rf = [
        # 'https://www.baidu.com/link?url=bv0PSNITotS0lI-PW43XKekt2AL6W9L14EdNCf9fbXn-Qd9epnjAPE268Qx-8Htz&wd=&eqid=fa7ba21700a35c5b00000003574a4870',
        'https://www.baidu.com/'
    ]

    hds = {'User-Agent': choice(ua),
           'Referer': choice(rf),
           }
    return hds;


# 读取代理文件到列表
def get_proxy_data(filename):
    content = open(filename).read().strip().split('\n')
    proxy = []
    for line in content:
        proxies = {}
        proxies['http'] = line.split('#')[1]
        proxy.append(proxies)
    return proxy

#def get_good_proxy(filename,change_flag=False):
#    proxy = get_proxy_data(filename)



def get_conn(sql, lis):
    # conn = pymysql.connect(host='127.0.0.1', port=3306, user='scrapy', passwd='scrapy', db='scrapy',charset='utf8')
    #    cur = conn.cursor()
    #    #sql = ("insert into pianzib(phone,comment,report_time,weight_info,url) values(%s,%s,%s,%s,%s)")
    #    #lis = (item['phone'],item['comment'],item['report_time'],item['weight_info'],item['url'])
    #    status=0000
    #    try:
    #        status = cur.execute(sql,lis)
    #    except Exception as e:
    #        print(e)

    #    if status==1:
    #        print('success',item['url'])
    #    else:
    #        print('failed')

    #    cur.close()
    #    conn.close()
    pass


def get_now_str():
    return time.strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    print(get_proxy_data('proxy/proxyinfo_20160529.txt'))
