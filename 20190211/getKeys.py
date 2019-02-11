import requests
import schedule
import time
import csv
import os
import traceback
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from email.mime.application import MIMEApplication

date = time.strftime('%Y%m%d', time.localtime(time.time()))
filedirectory = "/opt/python" + os.path.sep + date
#filedirectory = "F:\\简书\\python\\pythoncharm" + os.path.sep + date

def getSuggest(key=""):
    try:
        SUGGESTURL = "https://suggest.taobao.com/sug?code=utf-8&q="
        SUGGESTURL = SUGGESTURL + key
        r = requests.get(SUGGESTURL)
        json = r.json()
        return json["result"]
    except:
        l = open(filedirectory + os.path.sep + +date + "log.txt",'a')
        traceback.print_exc(l)
        l.flush()
        l.close()


def generatecsv():
    if not os.path.exists(filedirectory):
        os.mkdir(filedirectory)
    filename = filedirectory + os.path.sep + date + ".csv"
    f = open(filename,'w',encoding='utf-8-sig')
    try:
        items = getSuggest("水杯")
        writer = csv.writer(f)
        writer.writerow(["推荐词","商品代号"])
        for row in items:
            writer.writerow(row)
    except:
        logfilepath = filedirectory + os.path.sep + date + ".log"
        print(logfilepath)
        logfile = open(logfilepath,'a')
        logfile.writelines(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+os.linesep)
        traceback.print_exc(file=logfile)
        logfile.flush()
        logfile.close()
    finally:
        f.close()


def sendEmail():
    filename = filedirectory + os.path.sep + date + ".csv"
    # 第三方 SMTP 服务
    mail_host = "smtp.163.com"  # SMTP服务器
    mail_user = "jackwuchenghao@163.com"  # 用户名
    mail_pass = "4553283wch"  # 授权密码，非登录密码
    sender ="jackwuchenghao@163.com" # 发件人邮箱(最好写全, 不然会失败)
    receivers = ['jackwuchenghao@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    content = "this is the new suggest about 水杯"
    message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
    m = MIMEMultipart()
    m.attach(message)
    csvfile = MIMEApplication(open(filename, 'rb').read())
    csvfile.add_header('Content-Disposition', 'attachment', filename=date + ".csv")
    m.attach(csvfile)
    m['Subject'] = "水杯"
    m['From'] = "{}".format(sender)
    m['To'] = ",".join(receivers)
    smtpserver = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
    try:
        smtpserver.login(mail_user, mail_pass)  # 登录验证
        smtpserver.sendmail(sender, receivers, m.as_string())  # 发送
    except:
        logfilepath = filedirectory + os.path.sep + date + ".log"
        print(logfilepath)
        logfile = open(logfilepath,'a')
        logfile.writelines(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+os.linesep)
        traceback.print_exc(file=logfile)
        logfile.flush()
        logfile.close()
    finally:
        smtpserver.quit()


def dailywork():
    generatecsv()
    sendEmail()

if __name__ == "__main__":
    schedule.every(1).day.at("00:00").do(dailywork)
    while True:
        schedule.run_pending()