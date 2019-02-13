![每日美图](https://upload-images.jianshu.io/upload_images/13419832-3e586b39e3c231bf.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
#介绍
因为自己想着手搞一波淘宝，准备用于获取淘宝首页关键字推荐词，想化妆品、服装这种我们是不适合做的竞争太大了。
我们暂时定为水杯这种小类目的，对于新开的店面除了刷单，最重要的还是自然流量。自然流量都是淘宝买家，搜索关键字显示商品标题，看到商品列表主图，点击进入查看宝贝详情，所以想做一个可以每天定时将关于“水杯”关键字的建议词。这样的话可以根据每天的关键字来进行修改商品的标题。
#实现
我们使用python3.6实现功能，我们的功能可以分为4个部分
1. 获取关键字建议词
2. 将获取的建议词写入csv
3. 将csv加入邮件附件发送
4. 定时执行1-3步
关于各部分的代码如下
##获取关键字建议词
```python
def getSuggest(key,date,filedirectory):
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
```
使用requests模块直接获取建议词，将结果中json数据拿去出来，出错时将错误栈内容记录进日志中。
##将获取的建议词写入csv
```python
def generatecsv(date,filedirectory):
    if not os.path.exists(filedirectory):
        os.mkdir(filedirectory)
    filename = filedirectory + os.path.sep + date + ".csv"
    f = open(filename,'w',encoding='utf-8-sig')
    try:
        items = getSuggest("水杯",date,filedirectory)
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
```
将内容以utf-8的编码写入csv中，出错时将错误栈内容记录进日志中。
##将csv加入邮件附件发送
```python
def sendEmail(date,filedirectory):
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
```
发送邮件这部分代码有点多就不全部贴出来了，有兴趣的读者可以点击文末的链接下载查看
##定时执行1-3步
```python
if __name__ == "__main__":
    schedule.every(1).day.at("00:00").do(dailywork)
    while True:
        schedule.run_pending()
```
使用schedule模块实现定时执行函数的功能。
##python与模块安装难点
其实代码的实现不是特别难的事情，但是在服务器的运行还是比较麻烦的，在centos上的步骤如下，因为系统自带oython2.7千万别删除，因为yum是依赖于python2.7的：
```bash
yum -y install zlib*
yum install openssl-devel zilb-devel python3-devel
wget https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tgz -P /opt
tar -zxvf Python-3.6.1.tgz
cd Python-3.6.1
./configure --with-ssl --prefix=/usr/local/python3
make && make install
ln -s /usr/local/python3/bin/python3 /usr/bin/python3
ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3
vim ~/.bash_profile
//添加`PATH=$PATH:$HOME/bin:/usr/local/python3/bin`保存退出
source ~/.bash_profile
wget --no-check-certificate  https://pypi.python.org/packages/source/p/pip/pip-8.0.2.tar.gz#md5=3a73c4188f8dbad6a1e6f6d44d117eeb
tar -zxvf pip-8.0.2.tar.gz
cd pip-8.0.2
python3 setup.py build
python3 setup.py install
pip3 install requests
pip3 install schedule
```

#总结
1. 对于想做淘宝的小商户来说最好一开始不要做竞争激烈的类目。
2. 自然流量的关键点为标题、主图、宝贝详情。
3. 本文的代码可以点击[链接](https://github.com/OnlyPiglet/python/tree/master/20190211)查看。
4. 在centos上安装python3.6时注意，因为centos系统自带oython2.7千万别删除，因为yum是依赖于python2.7的。