# -*- coding: utf-8 -*-
import configparser
import requests


def send(title, content):
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='UTF-8')
    token = config.get('Notification', 'tg-token')
    userid = config.get('Notification', 'tg-userid')
    url = f'https://api.telegram.org/{token}/sendMessage?chat_id={userid}' + '&text=' + title + '%0A' + content
    response = requests.get(url)
    if response.status_code == 200:
        return {'status': 'success', 'response': response.text}
    else:
        return {'status': 'failed', 'error': response.text}
