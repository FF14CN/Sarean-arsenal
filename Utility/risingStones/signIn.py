<<<<<<< Updated upstream
=======
"""
Update: 2024-07-02
"""
>>>>>>> Stashed changes
import requests

"""
签个到示范：
from Utility.risingStones import rs_login
<<<<<<< Updated upstream
from Utility.risingStones import signIn as rs_signin
print(rs_signin.rs_signin(rs_login.login()))
#给默认账户签个到
"""
=======
from Utility.risingStones import constant
>>>>>>> Stashed changes


def rs_signin(cookies):
    """
    石之家签到组件
    :param cookies: 石之家cookies
    :return: status: success/fail
    """
    signinApi = "https://apiff14risingstones.web.sdo.com/api/home/sign/signIn"
    headers = {
<<<<<<< Updated upstream
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
=======
        **constant.RS_HEADERS_POST,
        'authorization': daoyu_ticket,
>>>>>>> Stashed changes
        "Cookie": cookies
    }
    signinResult = requests.post(url=signinApi, headers=headers)
    signinResult = signinResult.json()
    print(signinResult)
    if signinResult["code"] == 10000:
<<<<<<< Updated upstream
        return {
            "status": "success",
            "message": signinResult["msg"],
        }
    else:
        return {
            "status": "fail",
            "message": signinResult["msg"],
        }
=======
        if rs_login.debug:
            print(f'SignIn OK‘ {signinResult["msg"]}')
        msg = '签到成功 ~'
    elif signinResult["code"] == 10001:
        if rs_login.debug:
            print(f'Already signed in‘ {signinResult["msg"]}')
        msg = '已经签过到了，请不要重复签到 ~'
    else:
        if rs_login.debug:
            print(f'SignIn Fail‘ {signinResult["msg"]}')
        msg = '签到失败 ~ 原因可能是盛趣的签到参数变动，请反馈给开发者。'
        rs_login.logger_logs.error(signinResult["msg"])
    return msg
>>>>>>> Stashed changes
