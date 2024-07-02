"""
Author: Cettiidae
Version: 1.2.0
Update Date: 2024-06-27
"""
import requests
from Utility.risingStones import rs_login


def rs_signin(cookies,daoyu_ticket):
    """
    石之家签到组件
    :param daoyu_ticket:
    :param cookies: 石之家cookies
    :return: status: success/fail
    """
    signinApi = "https://apiff14risingstones.web.sdo.com/api/home/sign/signIn"
    headers = {
        'authority': 'apiff14risingstones.web.sdo.com',
        'method': 'POST',
        'scheme': 'https',
        'content-length': '0',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'accept': 'application/json, text/plain, */*',
        'authorization': daoyu_ticket,
        'user-agent': 'Mozilla/5.0 (Linux; Android 12; V2218A Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36 DaoYu/9.4.14',
        'origin': 'https://ff14risingstones.web.sdo.com',
        'x-requested-with': 'com.sdo.sdaccountkey',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://ff14risingstones.web.sdo.com/',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        "Cookie": cookies
    }
    signinResult = requests.post(url=signinApi, headers=headers)
    signinResult = signinResult.json()
    if signinResult["code"] == 10000:
        if rs_login_new.debug:
            print(f'SignIn OK‘ {signinResult["msg"]}')
        msg = '签到成功 ~'
        rs_login_new.logger_stream.info('签到成功了 ~')
    elif signinResult["code"] == 10001:
        if rs_login_new.debug:
            print(f'Already signed in‘ {signinResult["msg"]}')
        msg = '已经签过到了，请不要重复签到 ~'
        # rs_login_new.logger_stream.info('已经签到了 ~')
    else:
        if rs_login_new.debug:
            print(f'SignIn Fail‘ {signinResult["msg"]}')
        msg = '签到失败 ~ 原因可能是盛趣的签到参数变动，请反馈给开发者。'
        rs_login_new.logger_stream.info('签到失败了 ~')
        rs_login_new.logger_logs.error(signinResult["msg"])
    return msg
