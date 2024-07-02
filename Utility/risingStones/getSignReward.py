from datetime import datetime
<<<<<<< Updated upstream
import time

=======
from Utility.risingStones import rs_login
from Utility.risingStones import constant
>>>>>>> Stashed changes
import requests
import time


def getRewardStatus(cookies):
    """
    获取签到奖励状态
    :param cookies: 石之家登录后的cookie
    """
    currentTime = time.strftime("%Y-%m")
    RewardStatusurl = "https://apiff14risingstones.web.sdo.com/api/home/sign/signRewardList?month={}".format(
        currentTime)
    headers = {
<<<<<<< Updated upstream
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/89.0.4389.90 Safari/537.36",
        "Cookie": cookies
=======
        **constant.RS_HEADERS_GET,
        'authorization': daoyu_ticket,
>>>>>>> Stashed changes
    }
    rewardStatus = requests.get(url=RewardStatusurl, headers=headers).json()
    signLogUrl = "https://apiff14risingstones.web.sdo.com/api/home/sign/mySignLog?month={}".format(currentTime)
<<<<<<< Updated upstream
    signLogCount = requests.get(url=signLogUrl, headers=headers).json()["data"]["count"]
=======
    signLogCount = requests.get(url=signLogUrl, headers=headers, cookies=status_cookies).json()["data"]["count"]
    if rs_login.debug:
        print(rewardStatus)
>>>>>>> Stashed changes
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


def getSignIDReward(cookies, rewardId,rewardMonth):
    """
    获取签到奖励
    :param cookies: 石之家登录后的cookie
    :param rewardId: 签到奖励状态内的id
    :param rewardMonth: 签到奖励的月份
    """
    getRewardUrl = "https://apiff14risingstones.web.sdo.com/api/home/sign/getSignReward"
    headers = {
<<<<<<< Updated upstream
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/89.0.4389.90 Safari/537.36",
        "Cookie": cookies
=======
        **constant.RS_HEADERS_GET,
        'authorization': daoyu_ticket,
>>>>>>> Stashed changes
    }
    payload = {
        "id": int(rewardId),
        "month": rewardMonth
    }
<<<<<<< Updated upstream
    getReward = requests.post(url=getRewardUrl, headers=headers, data=payload).json()
=======
    if rs_login.debug:
        print(payload)
    get_signid_reward_cookies = {
        'ff14risingstones': cookies
    }
    getReward = requests.post(url=getRewardUrl, headers=headers, data=payload, cookies=get_signid_reward_cookies).json()
    if rs_login.debug:
        print(getReward)
>>>>>>> Stashed changes
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


def getReward(cookies):
    """
    获取签到奖励
    :param cookies: 石之家登录后的cookie
    """
    global status
    rewardStatus = getRewardStatus(cookies)
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
            if status["is_get"] == 0:
<<<<<<< Updated upstream
                time.sleep(10)
                getResult = getSignIDReward(cookies, index,today.strftime("%Y-%m"))
=======
                time.sleep(50)
                getResult = getSignIDReward(cookies, index, today.strftime("%Y-%m"), daoyu_ticket)
>>>>>>> Stashed changes
                returnMsg["data"][index - 1]["claimStatus"] = str(getResult)
            else:
                claimStatus = f"奖励{index}不满足领取条件！或已领取！"
                print(claimStatus)
                returnMsg["data"][index - 1]["claimStatus"] = claimStatus
            index += 1
    else:
        print(rewardStatus["data"])
    return returnMsg