"""
Author: KuliPoi
Contact: me@pipirapira.com
Created: 2024-06-27
File: rs_login.py
Version: 1.5.0
Description: daoyu login into rising stones (Fuck SQ by the way)
"""

import configparser
import logging
import sys
import string
import random
import uuid
import requests
import httpx
import urllib3
from kuai_log import get_logger
from Utility.risingStones import constant

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

dev = False
rs_config = configparser.RawConfigParser()

if dev:
    print('Dev environment detected')
    rs_config.read('E:\ProJect\Python\Sarean-arsenal\config.ini', encoding='UTF-8')
else:
    rs_config.read('config.ini')

if rs_config.get('Debug', 'Debug') == 'True':
    print("Debug mode on. Everything is cumming to ya.")
    debug = True
else:
    debug = False

logger_stream = get_logger('INFO', level=logging.INFO, is_add_stream_handler=True)
logger_logs = get_logger('DEBUG', level=logging.DEBUG, is_add_file_handler=True, is_add_stream_handler=False,
                         log_path='Logs/', log_filename='latest.log')


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
    headers = {
        **constant.RS_HEADERS_GET
    }
    with httpx.Client(http2=True) as client:
        get_tp_cookies_response = client.get(tp_cookies_url, headers=headers)
    tp_cookies = get_tp_cookies_response.cookies.get('ff14risingstones')
    if tp_cookies != '':
        if debug:
            print('Temp-Cookies: ' + tp_cookies)
        return tp_cookies
    else:
        logger_logs.error(f'Temp-Cookies is none {get_tp_cookies_response.text}')
        if debug:
            print('Temp-Cookies is fucked')
        return None


def rs_get_flowid():
    """
    get flowid for rising stones login
    :return: flowid
    """
    user_sessid = rs_config.get('Normal', 'daoyukey')
    device_id = '-'.join(str(uuid.uuid4()).upper() for _ in range(5))
    manuid = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
    get_flowid_url = 'https://daoyu.sdo.com/api/thirdPartyAuth/initialize'
    get_flowid_headers = {
        **constant.RS_MIN_HEADERS
    }
    get_flowid_params = {
        **constant.RS_PARAMS,
        'device_id': device_id,
        'device_manuid': manuid,
        'USERSESSID': user_sessid,
    }
    get_flowid_cookies = {
        'USERSESSID': user_sessid
    }
    with httpx.Client(http2=True) as client:
        get_flowid_response = client.get(get_flowid_url, params=get_flowid_params, cookies=get_flowid_cookies,
                                         headers=get_flowid_headers)
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


def rs_get_account_id_list(flowid):
    """
    query account id list
    :return: return a account id list like {"accountId": "123456789","displayName": "Username"}
    """
    user_sessid = rs_config.get('Normal', 'daoyukey')
    device_id = '-'.join(str(uuid.uuid4()).upper() for _ in range(5))
    manuid = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

    get_account_id_list_url = 'https://daoyu.sdo.com/api/thirdPartyAuth/queryAccountList'
    get_account_id_list_params = {
        **constant.RS_PARAMS,
        'device_id': device_id,
        'device_manuid': manuid,
        'USERSESSID': user_sessid,
        'flowId': flowid
    }
    get_account_id_header = {
        **constant.RS_MIN_HEADERS
    }
    get_account_id_list_cookies = {
        'USERSESSID': user_sessid,
    }
    with httpx.Client(http2=True) as client:
        get_account_id_list_response = client.get(get_account_id_list_url, params=get_account_id_list_params,
                                                  headers=get_account_id_header,
                                                  cookies=get_account_id_list_cookies)
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


def rs_make_confirm(account_id, flowid):
    """
    服务器鉴权
    :param account_id: 从get_account_id_list中获取的真实用户ID
    :param flowid: 浮动值
    :return: 成功返回True 失败返回False
    """
    user_sessid = rs_config.get('Normal', 'daoyukey')
    device_id = '-'.join(str(uuid.uuid4()).upper() for _ in range(5))
    manuid = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

    make_confirm_url = 'https://daoyu.sdo.com/api/thirdPartyAuth/chooseAccount?'
    make_confirm_header = {
        **constant.RS_MIN_HEADERS
    }
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
    with httpx.Client(http2=True) as client:
        make_confirm_response = client.get(make_confirm_url, params=make_confirm_params,
                                           headers=make_confirm_header, cookies=make_confirm_cookies)
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


def rs_get_sub_account_key(flowid):
    """
    获取子账号的DaoyuKey
    :return: 成功返回子账号的DaoyuKey 例如 DYA-xxxxxxxxx 失败返回None
    """
    user_sessid = rs_config.get('Normal', 'daoyukey')
    device_id = '-'.join(str(uuid.uuid4()).upper() for _ in range(5))
    manuid = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

    get_daoyu_ticket_url = 'https://daoyu.sdo.com/api/thirdPartyAuth/confirm?'
    get_daoyu_ticket_header = {
        **constant.RS_MIN_HEADERS
    }
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
    with httpx.Client(http2=True) as client:
        get_daoyu_ticket_response = client.get(get_daoyu_ticket_url, params=get_daoyu_ticket_params,
                                               headers=get_daoyu_ticket_header, cookies=get_daoyu_ticket_cookies)
    get_sub_account_key_json = get_daoyu_ticket_response.json()
    if get_sub_account_key_json['return_code'] == 0:
        try:
            sub_account_key = get_sub_account_key_json['data']['authorization']
            if debug:
                print(f'Get Sub_Account_Key Successful, User_sessionID：{sub_account_key}')
            return sub_account_key
        except KeyError:
            logger_stream.info(f'该账号游戏内没有创建角色，跳过操作。')
            return None
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
    dao_login_headers = {
        **constant.RS_HEADERS_GET
    }
    dao_login_cookies = {
        'ff14risingstones': temp_cookies
    }
    with httpx.Client(http2=True) as client:
        dao_login_response = client.get(dao_login_url, headers=dao_login_headers, params=dao_login_params,
                                        cookies=dao_login_cookies)
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
    with httpx.Client(http2=True) as client:
        rs_login_response = client.get(rs_login_url, headers=rs_login_headers, cookies=rs_login_cookies)
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
    with httpx.Client(http2=True) as client:
        bind_response = client.get(bind_url, headers=bind_headers, cookies=bind_cookies)
    bind_cookies = bind_response.cookies.get('ff14risingstones')
    if debug:
        print(f'Bind user account Success. {bind_cookies}')
    return bind_cookies
