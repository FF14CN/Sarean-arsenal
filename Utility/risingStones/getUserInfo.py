import requests
import httpx
from Utility.risingStones import constant


def get_rs_userinfo(cookies, daoyu_ticket):
    """
    石之家用户信息组件，获取登录用户的信息
    :param cookies: 石之家cookie
    :return: status: success/fail, message: msg
    """
    userInfoApi = "https://apiff14risingstones.web.sdo.com/api/home/userInfo/getUserInfo"
    headers = {
        **constant.RS_HEADERS_GET,
        'authorization': daoyu_ticket,
    }
    get_userinfo_cookies = {
        'ff14risingstones': cookies
    }
    with httpx.Client(http2=True) as client:
        userInfoResult = client.get(userInfoApi, headers=headers, cookies=get_userinfo_cookies)
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