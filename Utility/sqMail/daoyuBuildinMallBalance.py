import requests


def daoyu_mall_balance(session_id):
    """
    仅适用于叨鱼内部商城的查询签到积分 PC端不适用
    :param session_id: 子账号的Daoyukey值
    :return: 返回签到积分余额
    """
    get_balance_url = 'https://sqmallservice.u.sdo.com/api/rs/member/integral/balance?merchantId=1'
    get_balance_header = {
        'authority': 'sqmallservice.u.sdo.com',
        'method': 'GET',
        'scheme': 'https',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'qu-deploy-platform': '4',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'qu-merchant-id': '1',
        'qu-hardware-platform': '1',
        'qu-software-platform': '2',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 DaoYu/9.3.3',
        'qu-web-host': 'https://m.qu.sdo.com',
        'origin': 'https://m.qu.sdo.com',
        'x-requested-with': 'com.sdo.sdaccountkey',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://m.qu.sdo.com/',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    get_balance_cookies = {
        'sessionId': session_id
    }
    get_balance_response = requests.get(get_balance_url, headers=get_balance_header, cookies=get_balance_cookies,
                                        verify=False)
    get_balance_json = get_balance_response.json()
    balance = get_balance_json['data']['balance']
    return balance
