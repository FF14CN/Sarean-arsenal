import requests

"""
点个赞示范：
from Utility.risingStones import rs_login
from Utility.risingStones import like as rs_like
print(rs_like.rs_like(9365, 1, rs_login.login()))
#给官方水楼点赞
"""


def rs_like(post_id, type, cookies):
    """
    石之家评论组件
    :param post_id: 帖子id
    :param type: 点赞类型，1=对贴文点赞，2=对评论点赞
    :param cookies: 石之家cookies
    :return: status: success/fail
    """
    likeApi = "https://apiff14risingstones.web.sdo.com/api/home/posts/like"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        "Cookie": cookies
    }
    payload = {
        "id": post_id,
        "type": type,
    }
    likeResult = requests.post(url=likeApi, headers=headers, data=payload)
    likeResult = likeResult.json()
    if likeResult["code"] == 10000:
        return {
            "status": "success",
            "message": likeResult["msg"],
        }
    else:
        return {
            "status": "fail",
            "message": likeResult["msg"],
        }
