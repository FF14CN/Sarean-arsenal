from datetime import datetime
import time
from Utility.risingStones import rs_login

import requests


def getRewardStatus(cookies, daoyu_ticket):
    """
    获取签到奖励状态
    :param cookies: 石之家登录后的cookie
    """
    currentTime = time.strftime("%Y-%m")
    RewardStatusurl = "https://apiff14risingstones.web.sdo.com/api/home/sign/signRewardList?"
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
    status_cookies = {
        'ff14risingstones': cookies
    }
    rewardStatus = requests.get(url=RewardStatusurl, headers=headers, cookies=status_cookies).json()
    signLogUrl = "https://apiff14risingstones.web.sdo.com/api/home/sign/mySignLog?month={}".format(currentTime)
    signLogCount = requests.get(url=signLogUrl, headers=headers, cookies=status_cookies).json()["data"]["count"]
    if rewardStatus["code"] == 10000:
        return {
            "status": "success",
            "count": signLogCount,
            "data": rewardStatus["data"]
        }
    else:
        return {
            "status": "failed",
            "data": rewardStatus["msg"]
        }


def getSignIDReward(cookies, rewardId, rewardMonth, daoyu_ticket):
    """
    获取签到奖励
    :param cookies: 石之家登录后的cookie
    :param rewardId: 签到奖励状态内的id
    :param rewardMonth: 签到奖励的月份
    """
    getRewardUrl = "https://apiff14risingstones.web.sdo.com/api/home/sign/getSignReward?tempsuid=4128eb82-03e6-41d0-b6e9-1d87f5f08d6c"
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
    payload = {
        "id": rewardId,
        "month": rewardMonth,
        "tempsuid": "6870dd4d-ddfc-4be7-9628-c720e53c1994"
    }
    get_signid_reward_cookies = {
        'ff14risingstones': cookies
    }
    getReward = requests.post(url=getRewardUrl, headers=headers, data=payload, cookies=get_signid_reward_cookies).json()
    if getReward["code"] == 10000:
        return {
            "status": "success",
            "data": getReward["msg"]
        }
    else:
        return {
            "status": "failed",
            "data": getReward["msg"]
        }


def getReward(cookies, daoyu_ticket):
    """
    获取签到奖励
    :param cookies: 石之家登录后的cookie
    :param daoyu_ticket: daoyu_ticket
    """
    global status
    msg = ''
    rewardStatus = getRewardStatus(cookies, daoyu_ticket)
    if rewardStatus["status"] == "success":
        returnMsg = {
            "count": rewardStatus["count"],
            "data": [
                {
                    "description": "[10天]传送网使用券*30",
                    "status": rewardStatus["data"][0]["is_get"],
                    "claimStatus": ""
                },
                {
                    "description": "[20天]白银陆行鸟的羽毛X5",
                    "status": rewardStatus["data"][1]["is_get"],
                    "claimStatus": ""
                },
                {
                    "description": "[30天]1根黄金陆行鸟的羽毛",
                    "status": rewardStatus["data"][2]["is_get"],
                    "claimStatus": ""
                }
            ]
        }
        index = 1
        today = datetime.now()
        for status in rewardStatus["data"]:
            reward_name = returnMsg["data"][index - 1]["description"]
            if status["is_get"] == 0:
                time.sleep(10)
                getResult = getSignIDReward(cookies, index, today.strftime("%Y-%m"), daoyu_ticket)
                returnMsg["data"][index - 1]["claimStatus"] = str(getResult)
            else:
                claimStatus = f"{reward_name}不满足领取条件或已领取 "
                returnMsg["data"][index - 1]["claimStatus"] = claimStatus
                msg = msg + claimStatus
            index += 1
    else:
        print(rewardStatus["data"])
    if rs_login_new.debug:
        print(msg)
    return msg
