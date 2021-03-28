import datetime
import smtplib
from email.mime.text import MIMEText
from Status.logList import log
from Status.settings import EMAIL_HOST_USER, EMAIL_RECEIVE, EMAIL_FROM, EMAIL_SUBJECT, EMAIL_HOST, EMAIL_HOST_PASSWORD

def send_email(TITLE, HTML_MESSAGE):
    body = '<h1>已达止损点</h1>' \
           '<h2>京东方A</h2>' \
           '<span><p>成本：99 </p><p>现价：88</p></span>' \
           '<p>累计跌幅10%</p>'
    msg = MIMEText(HTML_MESSAGE, 'html')
    # msg = MIMEText(body, 'html')
    msg['subject'] = "{}（{}）".format(TITLE, EMAIL_SUBJECT)
    msg['from'] = EMAIL_FROM
    msg['to'] = EMAIL_RECEIVE
    TIME = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        s = smtplib.SMTP_SSL(EMAIL_HOST, 465)
        s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        s.sendmail(EMAIL_HOST_USER, EMAIL_RECEIVE, msg.as_string())
        log.update('（Message）: <{}>邮件发送成功'.format(TITLE))
    except smtplib.SMTPException:
        log.update('（Message）: Error: 无法发送邮件<{}>'.format(TITLE))
