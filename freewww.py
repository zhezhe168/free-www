#coding=utf8
import requests,re,time

username = '面板用户'
password = '面板密码' 
ID = '机器ID'
check = 'vm'
restart = 'vm.restart'

#此处的机房请修改为自己机器所在的，目前所知kvm,kvm1,kvm2...
checkurl = 'http://kvm.free-www.ru:1500/vmmgr?out=xml&authinfo={0}:{1}&func={2}&elid={3}'.format(username,password,check,ID)
keepurl = 'http://kvm.free-www.ru:1500/vmmgr?out=xml&authinfo={0}:{1}&func={2}&elid={3}'.format(username,password,restart,ID)
list1 = [('ok', 'vm.restart')]

def check(url = checkurl):
	try:
		s = requests.Session()
		r = s.get(url)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except Exception as e:
		print(e)

def restart(url = keepurl):
	try:
		s = requests.Session()
		r = s.get(url)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		khtml = r.text
		result = re.findall(r'><(.*)/><tparams><elid>%s</elid><out>xml</out><func>(.*)</func>'%ID,khtml)
		if list1 == result:
			print("Success Runing!")
		else:
			print("Error")
	except Exception as e:
		print(e)	

def main():
	rhtml = check()
	id_num = re.findall(r'<id>(\d+)</id>',rhtml)
	state = re.findall(r'<vmstatus>(.*)</vmstatus>',rhtml)
	if len(state) != 1:
			print("检测到不止一台VPS")
		if "running" in state[id_num.index(ID)]:
			print("Free-www is Running")
		else:
			print("%s is not running"%ID)
			restart()


if __name__ == '__main__':
	while True:
		main()
		time.sleep(300)
