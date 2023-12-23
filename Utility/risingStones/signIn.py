import requests

"""
签个到示范：
from Utility.risingStones import rs_login
from Utility.risingStones import signIn as rs_signin
print(rs_signin.rs_signin(rs_login.login()))
#给默认账户签个到
"""


def rs_signin(cookies):
    """
    石之家签到组件
    :param cookies: 石之家cookies
    :return: status: success/fail
    """
    signinApi = "https://apiff14risingstones.web.sdo.com/api/home/sign/signIn"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        "Cookie": cookies
    }
    signinResult = requests.post(url=signinApi, headers=headers)
    signinResult = signinResult.json()
    print(signinResult)
    if signinResult["code"] == 10000:
        return {
            "status": "success",
            "message": signinResult["msg"],
        }
    else:
        return {
            "status": "fail",
            "message": signinResult["msg"],
        }
