import requests
from lxml import etree
from bs4 import BeautifulSoup as bs
import queue as Queue
import threading
import time,re
from func import gene_headers


# write proxy
def writeproxy(porxyinfo):
    now_time = time.strftime('%Y%m%d')
    with open('proxy/proxyinfo_%s.txt'%now_time,'a+') as f:
        f.write(porxyinfo+'\n')

# return page code
def GetPageText(url):
    r = requests.get(url,headers=gene_headers())
    return r.text

# return post urllist
def GetPostUrl(source):
    posturllist = []

    iplist = bs(source,'lxml').find("table",{"id":"ip_list"}).findAll("tr")[1:]
    for item in iplist:
        getinfo = item.findAll("td")
        ip      = getinfo[1].get_text(strip='\r\n')
        port    = getinfo[2].get_text(strip='\r\n')
        address = getinfo[3].get_text(strip='\r\n')
        type    = getinfo[5].get_text(strip='\r\n')
        posturllist.append(type.lower()+'#'+ip+':'+port)
    return posturllist

def Checkproxy(porxyinfo):
    #正则匹配进行筛选
    if not re.match(r'^http#\d+\.\d+\.\d+\.\d+\:\d+$',porxyinfo):
        return

    proxies = {}
    proxies['http'] = porxyinfo.split('#')[1]

    try:
        r = requests.get("http://ip.chinaz.com/", proxies=proxies,timeout=3,headers=gene_headers())
    except:
        print('%s，不可用'%porxyinfo)
    else:
        writeproxy(porxyinfo)
        print('%s，可用'%porxyinfo)
    
    # if r:
    #     print(proxies, bs(requests.get('http://ip.chinaz.com/').content,'lxml').find("span",{"class":"info3"}).get_text(strip='\r\n'))
    #     writeproxy(porxyinfo)
    # else:
    #     print('No')

def getproxyid():
    start = time.time()
    queue = Queue.Queue()
    class ThreadUrl(threading.Thread):
        """Threaded Url Grab"""
        def __init__(self, queue):
            threading.Thread.__init__(self)
            self.queue = queue
            global mutex
        def run(self):
            while True:
                porxyinfo = self.queue.get()
                try:
                    mutex.acquire(5)
                    try:
                        Checkproxy(porxyinfo)
                    except:
                        time.sleep(0.15)
                        mutex.release()
                        self.queue.task_done()
                        continue
                    time.sleep(0.15)
                    mutex.release()

                    self.queue.task_done()
                except Exception as e:
                    time.sleep(0.15)
                    self.queue.task_done()       

    pagenum =5
    targets  = ['http://www.xicidaili.com/nn/%d'%page for page in range(1,pagenum+1)]
    targets += ['http://www.xicidaili.com/wn/%d'%page for page in range(1,pagenum+1)]
    for proxyurl in targets:
        try:
            PageText = GetPageText(proxyurl)
        except Exception as e:
            print(e)
            break
        
        PostUrlList = GetPostUrl(PageText)

        #进程循环
        # for url in PostUrlList:
        #     Checkproxy(url)

        #多线程
        mutex = threading.Lock()
        for i in range(5):
            t = ThreadUrl(queue)
            t.setDaemon(True)
            try:
                t.start()
            except:
                pass

        for host in PostUrlList:
            queue.put(host)
        queue.join()
    print("Elapsed Time: %s" % (time.time() - start) )

if __name__ == '__main__':
    getproxyid()
