#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from datetime import date, datetime, timedelta
import time,requests
import smtplib,os
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart


#邮件的发送者和接受者
me = "309506489@qq.com"
# 多个收件人用list,单个收件人字符串
# accpter = ["1045033116@qq.com","309506489@qq.com","1031937206@qq.com"]
accpter = ['1045033116@qq.com','18612404428@163.com']
#每次循环等待间隔时间,默认60秒程序唤醒一次
waitTime = 60
#需要定时监测的时间点
timeList = ['10:30','11:30','13:45','14:30','14:45','14:55']
# timeList = ['20:07','20:09','20:11']
#基金代码
fundCode =['161725','000311','110022','161616','486001']

def runTaskRegularTime():
	while True:
		str_time_now = datetime.now().strftime('%H:%M')
		finish_time = datetime.now().strftime('%H')
		if int(finish_time)<15:#3点后结束
			if str(str_time_now) in timeList:#按照设定好的时间对比
			# if 1>0:#调试用
				mainTask()
				time.sleep(60)
			else:
				taskWait(str_time_now)
		else:
			print('闭市了\n\f')
			time.sleep(2)
			mainTask()
			break


def mainTask():
	list =[]
	for n in range(len(fundCode)):
		str = inquiryRate(fundCode[n])+"\n\r"
		list.append(str)
	sendEmail(list)


def taskWait(currentTime):
	print('current time：' + str(currentTime))
	print('process will wakes up every %s seconds because it does not arrive at the specified time' % (waitTime))
	print ('')
	print ('')
	time.sleep(waitTime)

#调接口查询
def inquiryRate(shourNumber):
	url = (" http://fundmobapi.eastmoney.com/FundMApi/FundVarietieValuationDetail.ashx?version=5.3.0&plat=Android&appType=ttjj&FCODE=%s&deviceid=e19655bcbef4c4b362d908f8bcbdd67f||946596830144568&product=EFund&MobileKey=e19655bcbef4c4b362d908f8bcbdd67f||946596830144568"%shourNumber)
	r = requests.get(url, params=None)
	# print(r.json()["Expansion"])
	shortname=r.json()["Expansion"]["SHORTNAME"]
	yn=float(r.json()["Expansion"]["DWJZ"])
	tn=float(r.json()["Expansion"]["GZ"])
	upordown=float(r.json()["Expansion"]["GSZZL"])
	# print("_____________________")

	if (upordown)>0:
		stra = ("%s--------%s涨了,昨天净值为：%s,今天净值为：%s，涨了%s个点")%(upordown,shortname,yn,tn,upordown)
		# print(stra)
		return stra
	else:
		n = upordown.__neg__()
		strb =("%s--------%s跌了，昨天净值为：%s,今天净值为：%s，降了%s个点")%(upordown,shortname,yn,tn,n)
		# print(strb)
		return strb


def sendEmail(list):
	msg = MIMEMultipart()
	msg['from'] = me
	msg['to'] = ','.join(accpter)
	msg['subject'] = Header("%s基金数据"%datetime.now().strftime('%H:%M'), 'utf-8')
	mailBody = ''.join(list)
	print(mailBody)
	puretext = MIMEText(mailBody, 'plain', 'utf-8')
	msg.attach(puretext)
	try:
		server = smtplib.SMTP_SSL('smtp.qq.com', '465')
		server.login(me, "lhiawwpunkcrbjeg")
		server.sendmail(me, accpter, msg.as_string())
		server.quit()

	except Exception as e:
		print(str(e))
	return

if __name__ == '__main__':
	runTaskRegularTime()