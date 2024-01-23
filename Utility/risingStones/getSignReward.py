import time

import requests


def getRewardStatus(cookies):
    """
    获取签到奖励状态
    :param cookies: 石之家登录后的cookie
    """
    currentTime = time.strftime("%Y-%m")
    RewardStatusurl = "https://apiff14risingstones.web.sdo.com/api/home/sign/signRewardList?month={}".format(
        currentTime)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/89.0.4389.90 Safari/537.36",
        "Cookie": cookies
    }
    rewardStatus = requests.get(url=RewardStatusurl, headers=headers).json()
    signLogUrl = "https://apiff14risingstones.web.sdo.com/api/home/sign/mySignLog?month={}".format(currentTime)
    signLogCount = requests.get(url=signLogUrl, headers=headers).json()["data"]["count"]
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


def getSignIDReward(cookies, rewardId):
    """
    获取签到奖励
    :param cookies: 石之家登录后的cookie
    :param rewardId: 签到奖励状态内的id
    """
    getRewardUrl = "https://apiff14risingstones.web.sdo.com/api/home/sign/getSignReward"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/89.0.4389.90 Safari/537.36",
        "Cookie": cookies
    }
    payload = {
        "id": int(rewardId)
    }
    getReward = requests.post(url=getRewardUrl, headers=headers, data=payload).json()
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
        for status in rewardStatus["data"]:
            if status["is_get"] == 0:
                time.sleep(10)
                getResult = getSignIDReward(cookies, index)
                returnMsg["data"][index - 1]["claimStatus"] = str(getResult)
            else:
                claimStatus = f"奖励{index}不满足领取条件！或已领取！"
                print(claimStatus)
                returnMsg["data"][index - 1]["claimStatus"] = claimStatus
            index += 1
    else:
        print(rewardStatus["data"])
    return returnMsg