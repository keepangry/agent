# -*- coding: utf-8 -*-
import pymysql
import requests
import urllib.request
from bs4 import BeautifulSoup
from func import *

#第一步暂不做那么细，把所有内容放在一起，作为整体。
def parse_html(html):
	bsObj = BeautifulSoup(html, "html.parser")
	ret_data = ''
	try:
		bs = bsObj.find(id='content_left').find_all('div',attrs={'class':'result c-container ','srcid':'1599'})
	except Exception as e:
		print(e)
	else:
		if(len(bs)<5):
			print('数据过少')
			return FAILED,ret_data
		else:
			for item in bs:
				title = item.find('a').get_text()
				abstract = item.find('div',attrs={'class':'c-abstract'}).get_text()
				source_url = item.find('a',attrs={'class':'c-showurl'}).get_text()
				ret_data += title+abstract
			return SUCCESS,ret_data
	finally:
		pass

def get_baidu_search_by_key(key_word):
	base_url = 'http://www.baidu.com.cn/s?'
	hds = gene_headers()
	proxies = choice(get_proxy_data('proxy/proxyinfo_20160529.txt'))
	params = {
		'wd':key_word,
		'cl':'3',
#		'tn':'91412435_hao_pg',
		'ie':'utf-8',
		'rn':'30',
	}
	url_params = urllib.parse.urlencode(params)
	a = base_url+url_params
	ret = ''
	origin_data = {}
	try:
		#r = requests.get(base_url+url_params,headers=hds,proxies=proxies)
		r = requests.get(base_url+url_params,headers=hds)
		ret = r.content.decode('utf8')
		parse_status,ret = parse_html(ret)
		with open('key_word_data/'+key_word,'w') as f:
				f.write(ret)

		origin_data['html_content'] = ret
		origin_data['crawl_flag'] = '20150529_1'
		origin_data['search_source'] = 'baidu'
		origin_data['key_word'] = key_word
		status = orgin_data_save(origin_data)
		if status==SUCCESS:
			print('获取成功：%s'%key_word)
			return SUCCESS,ret
		else:
			return FAILED
	except Exception as e:
		print(e)
		print('获取失败：%s'%key_word)
		return FAILED,ret


def orgin_data_save(data):
	conn = pymysql.connect(host='182.92.113.26', port=3306, user='agent', passwd='agent', db='agent',charset='utf8')
	cur = conn.cursor()
	sql = "insert into origin_crawl_data(key_word,search_source,html_content,create_time,crawl_flag) values(%s,%s,%s,%s,%s)"
	lst = (data['key_word'],data['search_source'],data['html_content'],get_now_str(),data['crawl_flag'])
	try:
		status = cur.execute(sql,lst)
		return SUCCESS
	except Exception as e:
		print(e)
		return FAILED

	cur.close()


def crawl_control_by_database():
	conn = pymysql.connect(host='182.92.113.26', port=3306, user='agent', passwd='agent', db='agent',charset='utf8')
	#获取未爬取关键词进行爬取
	cur = conn.cursor()
	status = cur.execute("select key_word from key_word where status=%s",('0'))
	if status==0:
		return
	r_key_word = cur.fetchall()
	cur.close()
	#抓取，成功则加入表，并置关键词状态为1即：已爬取
	for key_word in r_key_word:
		status,ret = get_baidu_search_by_key(key_word[0])
		#成功
		if status==0:
			cur = conn.cursor()
			status = cur.execute("update key_word set status=%s where key_word=%s",('1',key_word))
			cur.close()
		time.sleep(uniform(2,4))
	conn.close()



if __name__ == '__main__':
	#get_baidu_search_by_key('哈哈')
	crawl_control_by_database()

