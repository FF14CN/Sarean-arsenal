#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
import configparser
from email.mime.text import MIMEText
from email.utils import formataddr


def send(title, content):
    """
    SMTP发送邮件
    :param title: 邮件标题
    :param content: 邮件内容
    :return:
    """
    smtp_config = configparser.ConfigParser()
    smtp_config.read('config.ini')
    pushkey = smtp_config.get('Notification', 'pushkey')
    sender = smtp_config.get('Notification', 'smtp-username')
    sender_pass = smtp_config.get('Notification', 'smtp-password')
    smtp_host = smtp_config.get('Notification', 'smtp-host')
    smtp_port = int(smtp_config.get('Notification', 'smtp-port'))

    reciver = pushkey
    sender = sender
    sender_pass = sender_pass

    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = formataddr(["FF14 Utility Server", sender])
    msg['To'] = formataddr(["User", reciver])
    msg['Subject'] = title  # 邮件标题
    # +++++++++++++++++++++++++++++++++++
    import ssl
    ctx = ssl.create_default_context()
    ctx.set_ciphers('DEFAULT')
    # +++++++++++++++++++++++++++++++++++
    server = smtplib.SMTP_SSL(smtp_host, smtp_port, context=ctx)
    server.login(sender, sender_pass)
    try:
        server.sendmail(sender, [reciver, ], msg.as_string())
    except Exception as e:
        print(e)
        server.quit()
        return {
            'status': 'failed',
            'error': e
        }
    server.sendmail(sender, [reciver, ], msg.as_string())
    server.quit()
    return {
        'status': 'success'
    }
