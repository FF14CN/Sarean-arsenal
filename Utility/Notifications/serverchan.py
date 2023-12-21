# -*- coding: utf-8 -*-
import configparser
import urllib.parse
import requests


def send(title, content):
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='UTF-8')
    key = config.get('Notification', 'push-key')
    url = f'https://sctapi.ftqq.com/{key}.send' + '?title=' + title + '&desp=' + content
    response = requests.get(url)
    if response.status_code == 200:
        return {'status': 'success', 'response': response.text}
    else:
        return {'status': 'failed', 'error': response.text}