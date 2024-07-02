import configparser
import random
import time

import requests
<<<<<<< Updated upstream
import Utility.sdoLogin.QRCode as QRCode
=======
import urllib3
from kuai_log import get_logger
from Utility.risingStones import constant
>>>>>>> Stashed changes

user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 "
              "Safari/537.36")


<<<<<<< Updated upstream
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
=======
def rs_tencent_check(response):
    """
    check if banned by tencent-fire-wall [您的请求已被该站点的安全策略拦截]
    :param response:
    :return: bools True or False
    """
    baned_text = '您的请求已被该站点的安全策略拦截'
    if baned_text in response:
        logger_stream.error('请求已经被沟槽的腾讯防火墙拦截，暂时没有解决办法，建议一个小时左右后重试')
        if debug:
            print('Baned by Tencent-Fire-Wall.')
        return True
    else:
        if debug:
            print('Tencent-Fire-Wall passed.')
        return False


def rs_config_check(result):
    """
    check config.ini
    :return: True or False
    """
    if ((rs_config.get('Normal', 'daoyukey', ) != ''
         or rs_config.get('Normal', 'manuid', ) != ''
         or rs_config.get('Normal', 'deviceid', ) != '')
            or rs_config.get('Normal', 'showusername', ) != ''):
        if debug:
            print('Everything which i need is alright.')
        return True
    else:
        logger_stream.error('重要参数缺失，请检查Config.ini是否正确配置,程序即将结束。')
        sys.exit()


def rs_get_temp_cookies():
    """
    get a temp cookies for rising stones login
    :return: temp_cookies: temp cookies for rising stones login
    """

    tp_cookies_url = 'https://apiff14risingstones.web.sdo.com/api/home/GHome/isLogin'
    get_tp_cookies_response = requests.get(tp_cookies_url, headers=constant.RS_HEADERS_GET, verify=False)
    tp_cookies = get_tp_cookies_response.cookies.get('ff14risingstones')
    if tp_cookies != '':
        if debug:
            print('Temp-Cookies: ' + tp_cookies)
        return tp_cookies
>>>>>>> Stashed changes
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


def rs_cookies_init():
    """
    初始化石之家cookies：ff14risingstones
    :return: dict cookies
    """
<<<<<<< Updated upstream
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
=======
    user_sessid = rs_config.get('Normal', 'daoyukey')
    device_id = rs_config.get('Normal', 'deviceid')
    manuid = rs_config.get('Normal', 'manuid')
    get_flowid_url = 'https://daoyu.sdo.com/api/thirdPartyAuth/initialize'
    get_flowid_params = {
        **constant.RS_PARAMS,
        'device_id': device_id,
        'device_manuid': manuid,
        'USERSESSID': user_sessid,
    }
    get_flowid_cookies = {
        'USERSESSID': user_sessid
    }
    get_flowid_response = requests.get(get_flowid_url, params=get_flowid_params, cookies=get_flowid_cookies,
                                       verify=False, headers=constant.RS_MIN_HEADERS)
    try:
        flowid = get_flowid_response.json()['data']['flowId']
        if flowid != '':
            if debug:
                print('Flowid: ' + str(flowid))
            return flowid
    except KeyError as e:
        logger_logs.error(f'KeyError: {e}')
        if debug:
            print('KeyError: ' + str(e))
        return None
>>>>>>> Stashed changes


def get_areaID(cookies, area_name):
    """
    获取服务器区域ID
    :return: int
    """
<<<<<<< Updated upstream
    getAreaAndGroupListUrl = "https://apiff14risingstones.web.sdo.com/api/home/groupAndRole/getAreaAndGroupList"
    headers = {
        "User-Agent": user_agent,
        "Cookie": cookies
    }
    areaAndGroupList = requests.get(getAreaAndGroupListUrl, headers=headers).json()["data"]
    for area in areaAndGroupList:
        if area["AreaName"] == area_name:
            return area["AreaID"]
=======
    user_sessid = rs_config.get('Normal', 'daoyukey')
    device_id = rs_config.get('Normal', 'deviceid')
    manuid = rs_config.get('Normal', 'manuid')

    get_account_id_list_url = 'https://daoyu.sdo.com/api/thirdPartyAuth/queryAccountList'
    get_account_id_list_params = {
        **constant.RS_PARAMS,
        'device_id': device_id,
        'device_manuid': manuid,
        'USERSESSID': user_sessid,
        'flowId': flowid
    }
    get_account_id_list_cookies = {
        'USERSESSID': user_sessid,
    }
    get_account_id_list_response = requests.get(get_account_id_list_url, params=get_account_id_list_params,
                                                headers=constant.RS_MIN_HEADERS,
                                                cookies=get_account_id_list_cookies, verify=False)
    get_account_id_list_json = get_account_id_list_response.json()
    if get_account_id_list_json['return_message'] == 'success':
        account_id_list = get_account_id_list_json['data']['accountList']
        if debug:
            print(account_id_list)
        logger_stream.info(f'拉取账号列表成功，当前主账户下发现{len(account_id_list)}个子账户.')
        return account_id_list
    else:
        logger_stream.info(f'从服务器拉取子账号列表失败，请检查config.ini中的参数是否填写准确。')
        if debug:
            print(get_account_id_list_json)
        logger_logs.error(f'Get accountList error，{get_account_id_list_json}。')
        return None
>>>>>>> Stashed changes


def get_characterID(cookies, areaID, character_name):
    """
    获取角色ID
    :return: str
    """
    getCharacterListUrl = f"https://apiff14risingstones.web.sdo.com/api/home/groupAndRole/getFF14Characters?AreaID={areaID}"
    headers = {
        "User-Agent": user_agent,
        "Cookie": cookies
    }
<<<<<<< Updated upstream
    characterList = requests.get(getCharacterListUrl, headers=headers).json()["data"]
    for character in characterList:
        if character["character_name"] == character_name:
            return str(character["character_id"])
=======
    make_confirm_params = {
        **constant.RS_PARAMS,
        'device_id': device_id,
        'device_manuid': manuid,
        'USERSESSID': user_sessid,
        'flowId': flowid,
        'accountId': account_id
    }
    make_confirm_cookies = {
        'USERSESSID': user_sessid,
    }
    make_confirm_response = requests.get(make_confirm_url, params=make_confirm_params,
                                         headers=make_confirm_header, cookies=make_confirm_cookies, verify=False)
    make_confirm_json = make_confirm_response.json()
    confirm_message = make_confirm_json['return_message']
    if confirm_message == 'success':
        if debug:
            print(f'Confirm with server Successful, AccountID：{account_id}')
        return True
    else:
        if debug:
            print(make_confirm_json)
        logger_stream.info(f'与服务器鉴权中发生错误，请将Logs反馈给开发者')
        logger_logs.error(f'Confirm with server Failed ：{confirm_message}')
        return False
>>>>>>> Stashed changes


def rs_character_bind(cookies):
    """
    绑定石之家角色
    :return: dict cookies
    """
    rs_config = configparser.RawConfigParser()
    rs_config.read('config.ini', encoding='UTF-8')
    rs_character = rs_config.get('RisingStones', 'rs_character')
    rs_area = rs_config.get('RisingStones', 'rs_area')

<<<<<<< Updated upstream
    bindUrl = "https://apiff14risingstones.web.sdo.com/api/home/groupAndRole/bindCharacterInfo"
    headers = {
        "User-Agent": user_agent,
        "Cookie": cookies
    }
    areaID = get_areaID(cookies, rs_area)
    characterID = get_characterID(cookies, areaID, rs_character)
    payload = {
        "character_id": characterID,
        "platform": 1,
        "device_id": "IOS20230530",
    }
    bindResult = requests.post(bindUrl, headers=headers, data=payload)
    return bindResult


def login():
    cookies = rs_cookies_init()
    print("绑定结果：", rs_character_bind(cookies))
    return cookies
=======
    get_daoyu_ticket_url = 'https://daoyu.sdo.com/api/thirdPartyAuth/confirm?'
    get_daoyu_ticket_params = {
        **constant.RS_PARAMS,
        'device_id': device_id,
        'device_manuid': manuid,
        'USERSESSID': user_sessid,
        'flowId': flowid
    }
    get_daoyu_ticket_cookies = {
        'USERSESSID': user_sessid,
    }
    get_daoyu_ticket_response = requests.get(get_daoyu_ticket_url, params=get_daoyu_ticket_params,
                                             headers=constant.RS_MIN_HEADERS, cookies=get_daoyu_ticket_cookies,
                                             verify=False)
    get_sub_account_key_json = get_daoyu_ticket_response.json()
    if get_sub_account_key_json['return_code'] == 0:
        sub_account_key = get_sub_account_key_json['data']['authorization']
        if debug:
            print(f'Get Sub_Account_Key Successful, User_sessionID：{sub_account_key}')
        return sub_account_key
    else:
        logger_logs.error(f'Get Sub_Account_Key error，{get_sub_account_key_json}')
        logger_stream.info(f'获取叨鱼子账号票据失败，请将Logs反馈给开发者')
        return None


def rs_dao_login(sub_account_key, temp_cookies):
    """
    # step in risingStones loginnnnnn. fucking new way to get DaoyuToken
    :return: DaoyuToken
    """

    dao_login_url = 'https://apiff14risingstones.web.sdo.com/api/home/GHome/daoLogin'
    dao_login_params = {
        'authorization': sub_account_key
    }
    dao_login_cookies = {
        'ff14risingstones': temp_cookies
    }
    dao_login_response = requests.get(dao_login_url, headers=constant.RS_HEADERS_GET, params=dao_login_params,
                                      cookies=dao_login_cookies, verify=False)
    dao_login_json = dao_login_response.json()
    if dao_login_json['code'] == 10000:
        daoyu_token = dao_login_json['data']['DaoyuToken']
        if debug:
            print(f'Get DaoyuToken Successful, DaoyuToken：{daoyu_token}')
        return daoyu_token
    else:
        logger_logs.error(f'Get DaoyuToken error，{dao_login_response}')
        logger_stream.info(f'获取DaoyuToken失败，请将Logs反馈给开发者')
        return None


def rs_do_login(daoyu_ticket, temp_cookies):
    rs_login_url = 'https://apiff14risingstones.web.sdo.com/api/home/GHome/isLogin'
    rs_login_headers = {
        **constant.RS_HEADERS_GET,
        'authorization': daoyu_ticket,
    }
    rs_login_cookies = {
        'ff14risingstones': temp_cookies
    }
    rs_login_response = requests.get(rs_login_url, headers=rs_login_headers, cookies=rs_login_cookies, verify=False)
    rs_login_json = rs_login_response.json()
    if rs_login_json['code'] == 10000:
        if debug:
            print(f'当前账户：[{rs_login_json["data"]["area_name"]}]'
                  f'[{rs_login_json["data"]["group_name"]}]'
                  f'[{rs_login_json["data"]["character_name"]}]')
        rs_cookies = rs_login_response.cookies.get('ff14risingstones')
        rs_login_status = True
        return rs_login_status, rs_cookies
    elif rs_login_json['code'] == 10103:
        rs_cookies = ''
        rs_login_status = False
        logger_stream.info(f'清先用手机石之家绑定游戏内角色后重试，详情请查看Github上相关说明')
        return rs_login_status, rs_cookies
    else:
        rs_cookies = ''
        rs_login_status = False
        if debug:
            print(f'rs login failed' + rs_login_json)
        logger_logs.error(f'Login error，{rs_login_json}')
        logger_stream.info(f'其他错误导致登录失败，请将Logs反馈给开发者')

        return rs_login_status, rs_cookies


def rs_bind(cookies, daoyu_ticket):
    bind_url = 'https://apiff14risingstones.web.sdo.com/api/home/groupAndRole/getCharacterBindInfo?platform=1'
    bind_headers = {
        **constant.RS_HEADERS_GET,
        'authorization': daoyu_ticket,
    }
    bind_cookies = {
        'ff14risingstones': cookies
    }
    bind_response = requests.get(bind_url, headers=bind_headers, cookies=bind_cookies, verify=False)
    bind_cookies = bind_response.cookies.get('ff14risingstones')
    if debug:
        print(f'Bind user account Success. {bind_cookies}')
    return bind_cookies
>>>>>>> Stashed changes
