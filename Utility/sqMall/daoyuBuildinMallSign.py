import requests


def daoyumall_sign(sub_session_id, account_id):
    """
    仅适用于叨鱼内的盛趣商城签到操作 PC端不适用
    :param sub_session_id: 子账号的Daoyukey值
    :param account_id: 子账号的AccountID
    :return:  0： 签到成功 1: 重复签到 2: 签到失败
    """
    sign_url = 'https://sqmallservice.u.sdo.com/api/us/integration/checkIn'
    sign_data = {'merchantId': 1}
    sign_header = {
        'authority': 'sqmallservice.u.sdo.com',
        'method': 'PUT',
        'scheme': 'https',
        'qu-web-host': 'https://m.qu.sdo.com',
        'qu-hardware-platform': '1',
        'qu-software-platform': '2',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 DaoYu/9.3.3',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'qu-deploy-platform': '4',
        'qu-merchant-id': '1',
        'origin': 'https://m.qu.sdo.com',
        'x-requested-with': 'com.sdo.sdaccountkey',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://m.qu.sdo.com/',
    }
    sign_cookies = {
        'sessionId': sub_session_id,
        'direbmemllam': account_id,
    }
    sign_response = requests.put(sign_url, headers=sign_header, cookies=sign_cookies, data=sign_data, verify=False)
    sign_json = sign_response.json()
    if sign_json['resultMsg'] == 'SUCCESS':
        return 0
    elif sign_json['resultMsg'] == '今日已签到，请勿重复签到':
        return 1
    else:
        return 2
