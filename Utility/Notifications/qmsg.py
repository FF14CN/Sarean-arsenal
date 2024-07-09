import configparser

import requests
# https://qmsg.zendee.cn/docs/api/#%E6%8E%A8%E9%80%81%E6%8E%A5%E5%8F%A3%E5%8F%82%E6%95%B0

def send(title: str, content: str):
    """
    发送 qmsg 通知
    :param title: 通知标题
    :param content: 通知内容
    :return:  {'status': 'success'} 或 {'status': 'failed'}
    """
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='UTF-8')
    pushkey = config.get('Notification', 'push-key')
    qmsg_target = config.get('Notification', 'qmsg-target')
    qmsg_target_number = config.get('Notification', 'qmsg-target-number')

    if qmsg_target == 'normal':
        url = 'https://qmsg.zendee.cn/jsend/' + pushkey
    elif qmsg_target == 'group':
        url = 'https://qmsg.zendee.cn/jgroup/' + pushkey
    else:
        return {'status': 'failed', 'error': 'qmsg-target配置错误'}


    headers = {
        "Content-Type": "application/json",
        "charset": "UTF-8"
    }
    load = {
        "msg": "[" + title + "]\n" + content,
    }
    if qmsg_target_number != '':
        load['qq'] = qmsg_target_number
    response = requests.post(url, headers=headers, json=load)
    if response.status_code == 200:
        return {'status': 'success'}
    else:
        return {'status': 'failed', 'error': response.text}

