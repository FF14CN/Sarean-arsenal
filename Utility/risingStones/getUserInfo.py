"""
Update: 2024-07-02
"""
import requests
from Utility.risingStones import constant


def get_rs_userinfo(cookies):
    """
    石之家用户信息组件，获取登录用户的信息
    :param cookies: 石之家cookie
    :return: status: success/fail, message: msg
    """
    userInfoApi = "https://apiff14risingstones.web.sdo.com/api/home/userInfo/getUserInfo"
    headers = {
<<<<<<< Updated upstream
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        "Cookie": cookies
=======
        **constant.RS_HEADERS_GET,
        'authorization': daoyu_ticket,
>>>>>>> Stashed changes
    }
    userInfoResult = requests.get(url=userInfoApi, headers=headers)
    userInfoResult = userInfoResult.json()
    if userInfoResult["code"] == 10000:
        return {
            "status": "success",
            "message": userInfoResult
        }
    else:
        return {
            "status": "fail",
            "message": userInfoResult
        }
