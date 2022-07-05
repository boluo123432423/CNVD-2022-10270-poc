# -*- coding:utf-8 -*-
import requests
import sys
import threading
from bs4 import BeautifulSoup
from requests.packages import urllib3
import xlsxwriter as xw
import fire
from time import sleep
from IPy import IP

headers={
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'
}
def writer(url,title):
	''' 写入TXT文档'''
	with open('url.txt','a',encoding='utf-8') as f:
		f.write(url+'                            '+title + '\n')#写入名字并换行
def requestsurl(url,port):
	url1='https://' + str(url) + ':'+str(port)
	url2='https://' + str(url) + ':'+str(port)
	#以下为GET请求
	try:
		urllib3.disable_warnings()
		req = requests.get(url1, headers=headers, timeout=3)
		req_title = BeautifulSoup(req.text,'html.parser')
		#print (str(req.status_code))
		print(url, '\t', req.status_code, '\t', req_title.title.string, "访问成功", end='\n')
		writer(url1,req_title.title.string)
	except:
		try:
			urllib3.disable_warnings()
			req1 = requests.get(url1, headers=headers, timeout=3)
			req_title = BeautifulSoup(req1.text,"html.parser")
			#print (str(req.status_code))
			print(url, '\t', req.status_code, '\t', req_title.title.string, "访问成功")
			writer(url2,req_title.title.string)
		except:
        		print(url1,'\t', url2, '\t', "None", '\t', "访问失败！" )
#
def loopip(ip):
	ip = IP(ip,make_net=True)
	for i in ip:
		print(i)
		n=1
		for n<65535:
			main_thread = threading.Thread(target=requestsurl,args=(i,n,))
			main_thread.start()
			n=n+1
			while 1:
			#判断正在运行的线程数量,如果小于5则退出while循环,
			#进入for循环启动新的进程.否则就一直在while循环进入死循环
				if(len(threading.enumerate()) < 500):
					break
def Nip(ip):
#	if '/' in str(ip):
#		loopip(ip)
#		return
	ip = IP(ip,make_net=True)
	for i in ip:
		print(i)
		main_thread = threading.Thread(target=requestsurl,args=(i,80,))
		main_thread.start()
		while 1:
		#判断正在运行的线程数量,如果小于5则退出while循环,
		#进入for循环启动新的进程.否则就一直在while循环进入死循环
			if(len(threading.enumerate()) < 500):
				break
fire.Fire()
