import configparser
import random
import time

import requests
import Utility.sdoLogin.QRCode as QRCode

user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 "
              "Safari/537.36")


def is_rs_login(cookies):
    '''
    Checks if cookie is valid.
    :return: {"status": True/False, "msg": data}
    '''
    is_login_api = "https://apiff14risingstones.web.sdo.com/api/home/GHome/isLogin"
    headers = {
        "User-Agent": user_agent,
        "Cookie": cookies
    }
    login_info = requests.get(is_login_api, headers=headers).json()
    if login_info['code'] == 10000:
        return {
            "status": True,
            "msg": login_info['data']}
    else:
        noc_config = configparser.RawConfigParser()
        noc_config.read('config.ini', encoding='utf-8')
        if noc_config.get('Notification', 'noc-enable') == 'True':
            import Utility.Notifications.push as pusher
            pusher.push('石之家登陆过期提醒！', '您的Cookie已过期！')
        return {
            "status": False,
            "msg": login_info}


def rs_cookies_login(cookies):
    '''
    调用扫码登录登录石之家,并返回登录后的cookies
    :return: dict cookies
    '''
    login_url = "https://apiff14risingstones.web.sdo.com/api/login/login"
    headers = {
        "User-Agent": user_agent,
        "Cookie": cookies
    }
    # 获取扫码登录关键参数，ticket
    sdoLogin_ticket = QRCode.login("6788", "1",
                                   "http://apiff14risingstones.web.sdo.com/api/home/GHome/login?redirectUrl=https://ff14risingstones.web.sdo.com/pc/index.htmlp")

    # 将传入的cookies变为登录态
    activeCookiesUrl = ("https://apiff14risingstones.web.sdo.com/api/home/GHome/login?redirectUrl=https"
                        "://ff14risingstones.web.sdo.com/pc/index.html&ticket=") + sdoLogin_ticket

    activeCookies = requests.get(activeCookiesUrl, headers=headers)
    print(activeCookies.text)


def rs_cookies_init():
    """
    初始化石之家cookies：ff14risingstones
    :return: dict cookies
    """
    # generate timestamp
    rs_config = configparser.RawConfigParser()
    rs_config.read('config.ini', encoding='UTF-8')

    # 判断是否存在石之家cookie，若不存在就生成一个
    if rs_config.get('RisingStones', 'rs_cookies') == "":
        cookies_init_url = "https://apiff14risingstones.web.sdo.com/api/home/GHome/isLogin"
        headers = {
            "User-Agent": user_agent
        }
        cookies = requests.get(cookies_init_url, headers=headers).cookies
        for rs_cookies_item in cookies:
            if rs_cookies_item.name == 'ff14risingstones':
                expires = rs_cookies_item.expires
                rs_config.set('RisingStones', 'rs_cookies_expires', expires)
        cookies = requests.utils.dict_from_cookiejar(cookies)
        # sdo的神秘登录cookie拼接
        domainhash = str(445385824)
        randomid = round(899999999 * random.random() + 1E9)
        initialtime = str(int(time.time()))
        userinfo = f"userinfo=userid={domainhash}-{randomid}-{initialtime}&siteid=SDG-08132-01;"
        ff14risingstones = "ff14risingstones=" + cookies['ff14risingstones'] + ";"
        rs_config.set('RisingStones', 'rs_cookies', ff14risingstones + userinfo)
        rs_config.write(open('config.ini', 'w', encoding='UTF-8'))
        print("已写入初始石之家Cookie：", ff14risingstones + userinfo)

    # 判断存在的cookie是否有效
    if rs_config.get('RisingStones', 'rs_cookies') != "":
        cookies = rs_config.get('RisingStones', 'rs_cookies')
        if is_rs_login(cookies)['status']:
            # 若cookie有效，则直接返回
            return cookies
        else:
            # 若cookie尚未登录，则跳转sdoLogin统一登录后再使用
            cookies = rs_cookies_login(cookies)
            return cookies


def login():
    return rs_cookies_init()
