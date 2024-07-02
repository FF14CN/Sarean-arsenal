"""
author: KuLiPa
contact: me@pipirapira.com
created: 2024-07-02
file: constant.py
version: 1.0.0
description: All headers
"""

RS_MIN_HEADERS = {
    'authority': 'daoyu.sdo.com',
    'method': 'GET',
    'scheme': 'https',
    'accept-encoding': 'gzip',
    'user-agent': 'okhttp/2.5.0'
}

RS_HEADERS_GET = {
    'authority': 'apiff14risingstones.web.sdo.com',
    'method': 'GET',
    'scheme': 'https',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Linux; Android 12; V2218A Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36 DaoYu/9.4.14',
    'origin': 'https://ff14risingstones.web.sdo.com',
    'x-requested-with': 'com.sdo.sdaccountkey',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://ff14risingstones.web.sdo.com/',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
}

RS_HEADERS_POST = {
        'authority': 'apiff14risingstones.web.sdo.com',
        'method': 'POST',
        'scheme': 'https',
        'content-length': '0',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Linux; Android 12; V2218A Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36 DaoYu/9.4.14',
        'origin': 'https://ff14risingstones.web.sdo.com',
        'x-requested-with': 'com.sdo.sdaccountkey',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://ff14risingstones.web.sdo.com/',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }

RS_PARAMS = {
    'src_code': '4',
    'app_version': '9.4.14',
    'app_version_code': '688',
    'device_gid': '_08:ff:3d:32:60:00',
    'device_os': '12',
    'device_manufacturer': 'vivo',
    'device_txzDeviceId': '',
    '_dispath': '0',
    'clientId': 'ff14risingstones',
    'appId': '6788',
    'scope': 'get_account_profile',
    'extend': '',
    'scene': ''
}