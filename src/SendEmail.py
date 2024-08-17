import os
import smtplib
from email.mime.text import MIMEText
# 引入smtplib和MIMEText
from time import sleep
import feedparser
from datetime import datetime, timedelta
from dateutil import parser

def r2e(rss_urls):

    # 初始化HTML内容
    html_content = '<title>RSS Updates</title>\n  '

    # RSS源的URL
    for rss_url in rss_urls:

        # 解析标题
        html_content += f"<h3> {rss_url[0]} 内容更新</h3 >\n <ol>\n"

        # 解析RSS源
        feed = feedparser.parse(rss_url[1])

        # 获取当前时间，转换为没有时区信息的datetime对象
        now = datetime.now()



        # 遍历RSS源中的条目
        for entry in feed.entries:
            # 将条目的发布时间转换为datetime对象
            published_time = parser.parse(entry.published)

            # 将发布时间转换为没有时区信息的datetime对象
            published_time = published_time.replace(tzinfo=None)

            # 检查发布时间是否在最近24小时内
            if now - published_time <= timedelta(hours=24):
                # 将标题、链接、CDATA和更新时间添加到HTML内容中
                html_content += f'''
                <li>
                    <a href="{entry.link}">{entry.title}</a>
                    <p>{entry.summary}</p>  <!-- 假设使用summary字段作为CDATA内容 -->
                    <p>Updated on: {published_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
                </li>
                '''
        html_content += '    </ol>\n'


    # 打印HTML内容或将其写入文件
    return (html_content)
    

def sentemail(body):
    host = 'smtp.163.com'
    # 设置发件服务器地址
    port = 465
    # 设置发件服务器端口号。注意，这里有SSL和非SSL两种形式，现在一般是SSL方式
    sender = 'nmecdzb@163.com'
    # 设置发件邮箱，一定要自己注册的邮箱
    pwd = os.getenv("Email_PWD")
    # 设置发件邮箱的授权码密码，根据163邮箱提示，登录第三方邮件客户端需要授权码
    receiver = 'time4action@163.com'
    # 设置邮件接收人，可以是QQ邮箱
    mybody = body
    # 设置邮件正文，这里是支持HTML的
    msg = MIMEText(mybody, 'html')
    # 设置正文为符合邮件格式的HTML内容
    msg['subject'] = 'RSS Updates'
    # 设置邮件标题
    msg['from'] = sender
    # 设置发送人
    msg['to'] = receiver
    # 设置接收人
    try:
        s = smtplib.SMTP_SSL(host, port)
        # 注意！如果是使用SSL端口，这里就要改为SMTP_SSL
        s.login(sender, pwd)
        # 登陆邮箱
        s.sendmail(sender, receiver, msg.as_string())
        # 发送邮件！
        print('Done.sent email success')
    except smtplib.SMTPException:
        print('Error.sent email fail')


if __name__ == '__main__':
    rss_urls = [["YouGov", 'https://today.yougov.com/news/feeds/latest/']]
    body=r2e(rss_urls)
    sentemail(body)
