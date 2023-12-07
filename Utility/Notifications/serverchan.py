# -*- coding: utf-8 -*-
import configparser
import urllib.parse
import requests


def send(title, content):
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='UTF-8')
    key = config.get('Notification', 'push-key')
    postdata = urllib.parse.urlencode({'title': title, 'desp': content}).encode('utf-8')
    url = f'https://sctapi.ftqq.com/{key}.send'
    response = requests.post(url, data=postdata)
    if response.status_code == 200:
        return {'status': 'success'}
    else:
        return {'status': 'failed', 'error': response.text}
