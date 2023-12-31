import requests


def get_rs_userinfo(cookies,uuid):
    """
    石之家用户信息组件，获取特定uuid的用户信息
    :param cookies: 石之家cookie
    :param uuid: 石之家用户uuid
    :return: status: success/fail, message: msg
    """
    userInfoApi = "https://apiff14risingstones.web.sdo.com/api/home/userInfo/getUserInfo?uuid=｛｝".format(uuid)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        "Cookie": cookies
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
