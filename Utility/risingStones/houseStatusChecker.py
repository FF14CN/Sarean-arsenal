
import re


def house_status_checker(user_info):
    """
    石之家房屋状态组件
    :return: {"house_status": "Unknown"/"Normal"/"Warning", "remain_day": remain_day/"error"}
    """
    if user_info["status"] == "success":  # 判断是否成功获取用户信息
        user_info = user_info["message"]["data"]["characterDetail"]
        if "house_remain_day" in user_info:  # 判断是否存在房屋过提醒字段。如果用户主动隐藏房屋信息，该字段必定出现且内容为“******”
            if "*" in user_info["message"]["data"]["characterDetail"]["house_remain_day"]: # 判断用户是否隐藏。
                houseStatus = {"house_status": "Unknown", "error": "用户隐藏了房屋状态"}
            else:
                remain_day = re.findall(r'\d+', user_info["house_remain_day"])
                houseStatus = {"house_status": "Warning", "remain_day": remain_day}
        else:
            houseStatus = {"house_status": "Normal"}

    else:
        houseStatus = {"house_status": "Unknown", "error": str(user_info)}

    if houseStatus["house_status"] == "Warning":
        house_status_msg = "房屋剩余{}天".format(houseStatus["remain_day"])
        return house_status_msg
    if houseStatus["house_status"] == "Unknown":
        house_status_msg = "房屋状态未知，具体错误信息：{}".format(houseStatus["error"])
        return house_status_msg
    if houseStatus["house_status"] == "Normal":
        house_status_msg = "房屋状态正常"
        return house_status_msg