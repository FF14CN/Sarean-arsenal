"""
Author: Cettiidae
Version: 1.2.0
Update Date: 2024-06-27
"""
import requests
from Utility.risingStones import rs_login
from Utility.risingStones import constant
import httpx

def rs_signin(cookies,daoyu_ticket):
    """
    石之家签到组件
    :param daoyu_ticket:
    :param cookies: 石之家cookies
    :return: status: success/fail
    """
    signinApi = "https://apiff14risingstones.web.sdo.com/api/home/sign/signIn"
    headers = {
        **constant.RS_HEADERS_POST_TEST,
        'authorization': daoyu_ticket,
        # "Cookie":  cookies
    }
    with httpx.Client(http2=True) as client:
        signinResult = client.post(signinApi, headers=headers)

    signinResult = signinResult.json()
    if signinResult["code"] == 10000:
        if rs_login.debug:
            print(f'SignIn OK‘ {signinResult["msg"]}')
        msg = '签到成功 ~'
        rs_login.logger_stream.info('签到成功了 ~')
    elif signinResult["code"] == 10001:
        if rs_login.debug:
            print(f'Already signed in‘ {signinResult["msg"]}')
        msg = '已经签过到了，请不要重复签到 ~'
    else:
        if rs_login.debug:
            print(f'SignIn Fail‘ {signinResult["msg"]}')
        msg = '签到失败 ~ 原因可能是盛趣的签到参数变动，请反馈给开发者。'
        rs_login.logger_stream.info('签到失败了 ~')
        rs_login.logger_logs.error(signinResult["msg"])
    return msg