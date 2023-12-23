import random
from time import sleep

import requests


def getUserTaskInfo(cookies):
    """
    获取石之家盖章任务状态
    :param cookies: 石之家cookies
    :return: 石之家盖章任务状态
    """
    taskInfoUrl = "https://apiff14risingstones.web.sdo.com/api/home/active/online2312/myTaskInfo"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        "Cookie": cookies
    }
    userTaskInfo = requests.get(taskInfoUrl, headers=headers)
    seal_total = userTaskInfo.json()["data"]["onceTask"]["seal_total"]
    userTaskInfo = userTaskInfo.json()["data"]["dayTask"]

    return {
        "seal_total": seal_total,
        "sign_status": userTaskInfo["sign_status"],
        "sign_seal": userTaskInfo["sign_seal"],
        "like_num": userTaskInfo["like_num"],
        "like_seal": userTaskInfo["like_seal"],
        "comment_status": userTaskInfo["comment_status"],
        "comment_seal": userTaskInfo["comment_seal"],
    }


def finishTask(cookies, taskType):
    """
    完成石之家盖章任务
    :param cookies: 石之家cookies
    :param taskType: 任务类型
    """
    if taskType == "like":
        from Utility.risingStones.like import rs_like
        for count in range(10):
            randomNum = random.randint(1, 863318)
            status = rs_like(randomNum, 2, cookies)
            sleep(1)
        return status
    elif taskType == "comment":
        from Utility.risingStones.comment import rs_comment
        randomNum = random.randint(1, 29)
        commentraw = f'<p><span class="at-emo">[emo{randomNum}]</span>&nbsp;</p>'
        status = rs_comment("9365", commentraw, "0", "0", "", cookies)
        return status
    elif taskType == "signIn":
        from Utility.risingStones.signIn import rs_signin
        status = rs_signin(cookies)
        return status
    else:
        print("任务类型错误")


def doSeal(cookies, sealType):
    """
    执行盖章任务
    :param cookies: 石之家cookies
    :param sealType: 盖章类型
    :return: 盖章状态
    """
    sealUrl = "https://apiff14risingstones.web.sdo.com/api/home/active/online2312/doSeal"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        "Cookie": cookies
    }
    payload = {
        "type": sealType
    }

    doSeal = requests.post(sealUrl, headers=headers, data=payload)
    if doSeal.json()["code"] == 10000:
        return {
            "status": doSeal.json()["msg"],
        }
    else:
        return {
            "status": doSeal.json()["msg"],
        }


def getSealReward(cookies, seal_num):
    """
    获取盖章奖励
    :param cookies: 石之家cookies
    :param seal_num: 盖章数量
    """
    # 有奖数量3、5、9、15、19、24、27、30
    sealRewardUrl = f"https://apiff14risingstones.web.sdo.com/api/home/active/online2312/getSealReward?seal_num={seal_num}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        "Cookie": cookies
    }
    getSealReward = requests.get(sealRewardUrl, headers=headers)
    if getSealReward.json()["code"] == 10000:
        return {
            "status": getSealReward.json()["msg"],
        }
    else:
        return {
            "status": getSealReward.json()["msg"],
        }


def run():
    from Utility.risingStones.rs_login import login as rs_login
    from Utility.risingStones.rs_login import is_rs_login as rs_userInfo
    cookies = rs_login()
    userTaskInfo = getUserTaskInfo(cookies)
    userInfo = rs_userInfo(cookies)["msg"]
    print("当前登录账户" + userInfo["character_name"] + "@" + userInfo["group_name"])
    print("当前签到状态：" + str(userTaskInfo))
    # if userTaskInfo["sign_status"] == 1:
    # 不知道为什么，没签到也是1
    finishTask(cookies, "signIn")

    if userTaskInfo["like_num"] < 5:
        # 点赞不够
        print("点赞不够，正在随机点赞")
        print(finishTask(cookies, "like"))

    if userTaskInfo["comment_status"] < 1:
        # 评论不够
        print("评论不够，正在随机评论")
        print(finishTask(cookies, "comment"))

    # 盖章
    for sealIndex in range(1, 4):
        sleep(1)
        print(doSeal(cookies, sealIndex))

    # 领奖
    for rewardNum in [3, 5, 9, 15, 19, 24, 27, 30]:
        sleep(10)
        print("Day=" + str(rewardNum) + getSealReward(cookies, rewardNum))

    userTaskInfo = getUserTaskInfo(cookies)
    print("当前签到状态：" + str(userTaskInfo))
