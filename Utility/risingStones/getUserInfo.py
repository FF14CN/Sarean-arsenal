import requests


def get_rs_userinfo(cookies, daoyu_ticket):
    """
    石之家用户信息组件，获取登录用户的信息
    :param cookies: 石之家cookie
    :return: status: success/fail, message: msg
    """
    userInfoApi = "https://apiff14risingstones.web.sdo.com/api/home/userInfo/getUserInfo"
    headers = {
        'authority': 'apiff14risingstones.web.sdo.com',
        'method': 'GET',
        'scheme': 'https',
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
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    get_userinfo_cookies = {
        'ff14risingstones': cookies
    }
    userInfoResult = requests.get(url=userInfoApi, headers=headers, cookies=get_userinfo_cookies)
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
