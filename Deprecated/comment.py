import requests

"""
水一贴示范：
from Utility.risingStones import rs_login
from Utility.risingStones import comment as rs_comment
commentraw = '<p><span class="at-emo">[emo29]</span>&nbsp;</p>'
print(rs_comment.rs_comment("9365", commentraw, "0", "0", "", rs_login.login()))
#官方水楼水一贴
"""


def rs_comment(post_id, comment, parent_id, root_parent, comment_pic, cookies):
    """
    石之家评论组件
    :param post_id: 帖子id
    :param comment: 评论内容 请使用p标签包裹
    :param parent_id: 父评论id
    :param root_parent: 根评论id 目前观察到与parent_id相同
    :param comment_pic: 评论图片
    :param cookies: 石之家cookie
    :return: status: success/fail
    """
    commentApi = "https://apiff14risingstones.web.sdo.com/api/home/posts/comment"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        "Cookie": cookies
    }
    payload = {
        "content": str(comment),
        "posts_id": str(post_id),
        "parent_id": str(parent_id),
        "root_parent": str(root_parent),
        "comment_pic": str(comment_pic)
    }
    commentResult = requests.post(url=commentApi, headers=headers, data=payload)
    commentResult = commentResult.json()
    if commentResult["code"] == 10000:
        return {
            "status": "success",
            "message": commentResult["msg"],
        }
    else:
        return {
            "status": "fail",
            "message": commentResult["msg"],
        }
