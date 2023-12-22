import configparser

import requests


def send(title: str, content: str):
    """
    发送 bark 通知
    :param title: 通知标题
    :param content: 通知内容
    :return:  {'status': 'success'} 或 {'status': 'failed'}
    """
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='UTF-8')
    pushkey = config.get('Notification', 'push-key')
    url = 'https://api.day.app/' + pushkey
    headers = {
        "Content-Type": "application/json",
        "charset": "UTF-8"
    }
    # bark通知将被分组到“FF14”，并且会自动保存
    load = {
        "title": title,
        "body": content,
        "badge": 1,
        "sound": "minuet.caf",
        "icon": "https://huiji-thumb.huijistatic.com/ff14/uploads/thumb/3/33/000030.png/30px-000030.png",
        "group": "FF14",
        "isArchive": 1,
    }
    response = requests.post(url, headers=headers, json=load)
    if response.status_code == 200:
        return {'status': 'success'}
    else:
        return {'status': 'failed', 'error': response.text}
