# author: "baoyu"
# date: 2023/2/8

import ssl
import requests
import smtplib
import json
import time
from email.message import EmailMessage

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}


def sms(content):
    # 无需安装第三方库
    EMAIL_ADDRESS = 'xxx@qq.com'  # 邮箱地址
    EMAIL_PASSWORD = 'xxxxxxxxxxxxx'  # QQ邮箱SMTP的授权码
    smtp = smtplib.SMTP('smtp.qq.com', 25)
    context = ssl.create_default_context()
    sender = EMAIL_ADDRESS  # 发件邮箱
    receiver = ['xxxxxxxxx@qq.com']  # 收件邮箱
    subject = "上线啦"  # 主题
    body = content
    msg = EmailMessage()
    msg['subject'] = subject  # 邮件主题
    msg['From'] = sender
    msg['To'] = receiver
    msg.set_content(body)  # 邮件内容

    with smtplib.SMTP_SSL("smtp.qq.com", 465, context=context) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


if __name__ == '__main__':
    firstFlag = True
    initialIps = []
    while True:
        data = requests.get(
            'http://xxxxxx/druid/websession.json?orderBy=&orderType=asc&page=1&perPageCount=1000000&',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'})
        message = ''
        if 200 == data.status_code:
            if data.content is not None:
                if json.loads(data.content)['Content'] is not None:
                    data = json.loads(data.content)['Content']
                    if firstFlag:
                        for i in data:
                            initialIps.append(i['RemoteAddress'])
                        initialIps = list(set(initialIps))
                    else:
                        newIps = []
                        for i in data:
                            if i['RemoteAddress'] not in initialIps:
                                newIps.append(i['RemoteAddress'])
                                initialIps.append(i['RemoteAddress'])
                        if len(newIps) > 0:
                            message = '有新人上线啦，' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + \
                                      '\n' + str(newIps)
                else:
                    message = '读取内容失败，' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            else:
                message = '未获取到内容，' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        else:
            message = '请求失败' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if message != '':
            sms(message)
        time.sleep(600)
