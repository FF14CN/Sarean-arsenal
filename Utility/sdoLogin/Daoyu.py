"""
Author: KuliPoi
Contact: me@pipirapira.com
Created: 2023-12-20
File: Daoyu.py
Version: 2.5.0
Description: DAOYU LOGIN, FUCK SQ BY WAY
"""
import logging
import urllib3
import requests
import configparser
import os
from kuai_log import get_logger
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger_stream = get_logger('INFO', level=logging.INFO, is_add_stream_handler=True)
logger_logs = get_logger('DEBUG', level=logging.DEBUG, is_add_file_handler=True, is_add_stream_handler=False,
                         log_path='Logs/',log_filename='latest.log')


# DYKey打码
def dykey_encrypt(self):
    return re.sub(r"(?<=DY_)(.*)(?=..)", lambda match: '*' * len(match.group(1)), self)


# 配置文件读取
def config_handler():
    """
    读取配置文件 config.ini
    :return: 返回 手机号/配置服务器/设备ID/设备型号/DaoyuKey/ShowUsername
    """
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    device_id = config.get('Normal', 'DeviceID')
    manuid = config.get('Normal', 'ManuID')
    daoyu_key = config.get('Normal', 'DaoyuKey')
    show_username = config.get('Normal', 'ShowUsername')
    return device_id, manuid, daoyu_key, show_username


# 初始化检测
def initialize():
    """
    初始化检测
    :return: 本地已有配置文件，从云端同步成功返回True / 从云端同步失败返回None
    """
    if os.path.exists('config.ini'):  # 检测配置文件是否存在
        logger_stream.info('检测到存在配置文件，无需进行初始化...')
        return True
    else:
        url = 'https://pipirapira.com/config/config.ini'
        local_filename = 'config.ini'
        try:
            logger_stream.info('检测到第一次运行，正在从云端同步配置文件..')
            requests.get(url, verify=False).raise_for_status()
            with open(local_filename, 'wb') as file:
                file.write(requests.get(url).content)
            logger_stream.info('从云端同步配置文件成功')
            return True
        except requests.exceptions.RequestException as e:
            logger_stream.error(f'同步配置失败，请检查网络连接或反馈给开发者, {e}')
            return None


# 获取guid
def get_guid(device_id, manuid):
    """
    Guid 是叨鱼App 结合设备ID和设备型号产生的一个参数会在登录前提供生成 Scene 莫名其妙的参数 大概是叨鱼的app的信息
    :param device_id: 设备ID
    :param manuid: 设备型号
    :return: 成功会返回 guid 和 scene 失败则返回None 因为Scene很莫名其妙所以不敢写死 动态获取吧
    """
    guid_url = 'https://daoyu.sdo.com/api/userCommon/getGuid'
    guid_params = {
        'phone': 'phone',
        'media_channel': 'AppStore',
        'device_id': {device_id},
        'app_version': 'i.9.3.3',
        'key': 'key',
        'device_os': 'iOS17.0',
        'idfa': '00000000-0000-0000-0000-000000000000',
        'src_code': '8',
        'device_manuid': {manuid},
    }
    headers = {
        'user-agent': 'SdAccountKeyM/9.3.3 (iPhone; iOS 17.0; Scale/3.00)',
        'content-type': 'application/json',
    }

    guid_response = requests.get(guid_url, params=guid_params, headers=headers, verify=False)
    guid_json = guid_response.json()
    guid = guid_json['data']['guid']
    scene = guid_json['data']['scene']
    if guid != '' and scene != '':
        logger_logs.debug('Guid and scene get Successful. Guid：' + guid + '  scene：' + scene)
        return guid, scene
    else:
        logger_logs.error('Guid or Scene Error Guid：' + guid + 'scene：' + scene)
        logger_stream.info('致命错误，获取Guid失败了，请将Logs反馈给开发者，程序即将停止。')
        return None


# DaoyuTicket
# step 1/4 Get flowid
def get_flowid(manuid, deviceid, sessionid, show_username):
    """
     获取浮动值 用来校验 校验四联的第一步
    :param manuid: 设备型号
    :param deviceid: 设备ID
    :param sessionid: Daoyu_Key 主账号的关键参数 类似 DY_xxxxx 手机号登录之后生成，不重新登陆一般不会改变
    :param show_username: 一般是叨鱼登录手机号的中间四位打码值 如 138****1234
    :return: 成功则返回浮动值 失败返回None
    """
    get_flowid_url = 'https://daoyu.sdo.com/api/thirdPartyAuth/initialize'
    get_flowid_params = {
        'media_channel': 'AppStore',
        'device_os': 'iOS17.0',
        'idfa': '00000000-0000-0000-0000-000000000000',
        'circle_id': '854742',
        'app_version': 'i.9.3.3',
        'device_manuid': manuid,
        'src_code': '8',
        'clientId': 'qu_shop',
        'appId': '6666',
        'scope': 'get_account_profile',
        'extend': '',
        'device_id': deviceid
    }
    get_flowid_header = {
        'authority': 'daoyu.sdo.com',
        'method': 'GET',
        'scheme': 'https',
        'content-type': 'application/json',
        'accept': '*/*',
        'user-agent': 'SdAccountKeyM/9.3.3 (iPhone; iOS 17.0; Scale/3.00)',
        'accept-language': 'zh-Hans-CN;q=1, zh-Hant-CN;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
    }
    get_flowid_cookies = {
        'USERSESSID': sessionid,
        'is_login': '1',
        'show_username': show_username,
    }
    get_flowid_response = requests.get(get_flowid_url, params=get_flowid_params, headers=get_flowid_header,
                                       cookies=get_flowid_cookies, verify=False)
    get_flowid_json = get_flowid_response.json()
    if get_flowid_json['return_code'] == 0:
        flowid = get_flowid_json['data']['flowId']
        logger_logs.info(f'Get flowID Successful : {flowid}')
        return flowid
    else:
        logger_stream.info('无法获取叨鱼浮动值，请将日志文件发送给开发者')
        logger_logs.error(f'Get flowID Error : {get_flowid_json}')
        return None


# step 2/4 Get accountID list
def get_account_id_list(flowid, deviceid, manuid, sessionid, show_username):
    """
    拉取子账号列表，每个叨鱼我们称之为一个主账号和多个子账号 校验四联的第二步
    :param flowid: 浮动值
    :param deviceid: 设备ID
    :param manuid: 设备型号
    :param sessionid: Daoyu_Key 主账号的关键参数 类似 DY_xxxxx 手机号登录之后生成，不重新登陆一般不会改变
    :param show_username: 一般是叨鱼登录手机号的中间四位打码值 如 138****1234
    :return: 成功则返回一个列表 包含账号的真实ID和登录名 如 {"accountId": "123456789","displayName": "Username"}
    """
    get_account_id_list_url = 'https://daoyu.sdo.com/api/thirdPartyAuth/queryAccountList'
    get_account_id_list_params = {
        'flowId': flowid,
        'idfa': '00000000-0000-0000-0000-000000000000',
        'device_manuid': manuid,
        'src_code': '8',
        'circle_id': '854742',
        'device_os': 'iOS17.0',
        'media_channel': 'AppStore',
        'app_version': 'i.9.3.3',
        'device_id': deviceid
    }
    get_account_id_header = {
        'authority': 'daoyu.sdo.com',
        'method': 'GET',
        'scheme': 'https',
        'content-type': 'application/json',
        'accept': '*/*',
        'user-agent': 'SdAccountKeyM/9.3.3 (iPhone; iOS 17.0; Scale/3.00)',
        'accept-language': 'zh-Hans-CN;q=1, zh-Hant-CN;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
    }
    get_account_id_list_cookies = {
        'USERSESSID': sessionid,
        'is_login': '1',
        'show_username': show_username,
    }
    get_account_id_list_response = requests.get(get_account_id_list_url, params=get_account_id_list_params,
                                                headers=get_account_id_header,
                                                cookies=get_account_id_list_cookies, verify=False)
    get_account_id_list_json = get_account_id_list_response.json()
    if get_account_id_list_json['return_message'] == 'success':
        account_id_list = get_account_id_list_json['data']['accountList']
        logger_stream.info(f'当前主账户下存在{len(account_id_list)}个账户.')
        return account_id_list
    else:
        logger_stream.info(f'拉取子账号列表失败，请将Logs反馈给开发者')
        logger_logs.error(f'Get accountList error，{get_account_id_list_json}。')
        return None


# step 3/4 Confirm with server
def make_confirm(account_id, flowid, deviceid, manuid, sessionid, show_username):
    """
    和服务器握手确认登录
    :param account_id: 从get_account_id_list中获取的真实用户ID
    :param flowid: 浮动值
    :param deviceid: 设备ID
    :param manuid: 设备型号
    :param sessionid: Daoyu_Key 主账号的关键参数 类似 DY_xxxxx 手机号登录之后生成，不重新登陆一般不会改变
    :param show_username:  一般是叨鱼登录手机号的中间四位打码值 如 138****1234
    :return: 成功返回True 失败返回False
    """
    make_confirm_url = 'https://daoyu.sdo.com/api/thirdPartyAuth/chooseAccount?'
    make_confirm_header = {
        'authority': 'daoyu.sdo.com',
        'method': 'GET',
        'scheme': 'https',
        'content-type': 'application/json',
        'accept': '*/*',
        'user-agent': 'SdAccountKeyM/9.3.3 (iPhone; iOS 17.0; Scale/3.00)',
        'accept-language': 'zh-Hans-CN;q=1, zh-Hant-CN;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
    }
    make_confirm_params = {
        'idfa': '00000000-0000-0000-0000-000000000000',
        'flowId': flowid,
        'device_os': 'iOS17.0',
        'media_channel': 'AppStore',
        'accountId': account_id,
        'device_manuid': manuid,
        'app_version': 'i.9.3.3',
        'src_code': '8',
        'device_id': deviceid,
        'circle_id': '854742'
    }
    make_confirm_cookies = {
        'USERSESSID': sessionid,
        'is_login': '1',
        'show_username': show_username,
    }
    make_confirm_response = requests.get(make_confirm_url, params=make_confirm_params,
                                         headers=make_confirm_header, cookies=make_confirm_cookies, verify=False)
    make_confirm_json = make_confirm_response.json()
    confirm_message = make_confirm_json['return_message']
    if confirm_message == 'success':
        logger_logs.debug(f'Confirm with server Successful, AccountID：{account_id}')
        return True
    else:
        logger_stream.info(f'和服务器握手途中发生错误，请将Logs反馈给开发者')
        logger_logs.error(f'Confirm with server Failed ：{confirm_message}')
        return False


# step 4/4 Get DaoyuTicket
def get_sub_account_key(flowid, manuid, deviceid, sessionid, show_username):
    """
    获取子账号的DaoyuKey
    :param flowid: 浮动值
    :param manuid: 设备型号
    :param deviceid: 设备ID
    :param sessionid: Daoyu_Key 主账号的关键参数 类似 DY_xxxxx 手机号登录之后生成，不重新登陆一般不会改变
    :param show_username: 一般是叨鱼登录手机号的中间四位打码值 如 138****1234
    :return: 成功返回子账号的DaoyuKey 例如 DYA-xxxxxxxxx 失败返回None
    """
    get_daoyu_ticket_url = 'https://daoyu.sdo.com/api/thirdPartyAuth/confirm?'
    get_daoyu_ticket_header = {
        'authority': 'daoyu.sdo.com',
        'method': 'GET',
        'scheme': 'https',
        'content-type': 'application/json',
        'accept': '*/*',
        'user-agent': 'SdAccountKeyM/9.3.3 (iPhone; iOS 17.0; Scale/3.00)',
        'accept-language': 'zh-Hans-CN;q=1, zh-Hant-CN;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
    }
    get_daoyu_ticket_params = {
        'app_version': 'i.9.3.3',
        'flowId': flowid,
        'idfa': '00000000-0000-0000-0000-000000000000',
        'circle_id': '854742',
        'device_manuid': manuid,
        'media_channel': 'AppStore',
        'device_os': 'iOS17.0',
        'device_id': deviceid,
        'src_code': '8'
    }
    get_daoyu_ticket_cookies = {
        'USERSESSID': sessionid,
        'is_login': '1',
        'show_username': show_username,
    }
    get_daoyu_ticket_response = requests.get(get_daoyu_ticket_url, params=get_daoyu_ticket_params,
                                             headers=get_daoyu_ticket_header, cookies=get_daoyu_ticket_cookies,
                                             verify=False)
    get_daoyu_ticket_json = get_daoyu_ticket_response.json()
    if get_daoyu_ticket_json['return_code'] == 0:
        daoyu_ticket = get_daoyu_ticket_json['data']['authorization']
        logger_logs.debug(f'Get_daoyuSubKey Successful')
        return daoyu_ticket
    else:
        logger_logs.error(f'Get_daoyuTicket error，{get_daoyu_ticket_json}')
        logger_stream.info(f'获取叨鱼子账号票据失败，请将Logs反馈给开发者')
        return None


# get_temp_session ID
def get_temp_sessionid(main_key):
    get_temp_sessionid_url = 'https://sqmallservice.u.sdo.com/api/us/daoyu/account/getMallLoginStatus'
    get_temp_sessionid_header = {
        'authority': 'sqmallservice.u.sdo.com',
        'method': 'GET',
        'scheme': 'https',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'qu-deploy-platform': '4',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'qu-merchant-id': '',
        'qu-hardware-platform': '1',
        'qu-software-platform': '2',
        'user-agent': 'Mozilla/5.0 (Linux; Android 12; 2206122SC Build/V417IR; wv) AppleWebKit/537.36 (KHTML, '
                      'like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36 DaoYu/9.4.8',
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
    get_temp_sessionid_params = {
        'USERSESSID': main_key
    }
    get_temp_sessionid_response = requests.get(get_temp_sessionid_url, params=get_temp_sessionid_params,
                                               headers=get_temp_sessionid_header, verify=False)
    session_id = get_temp_sessionid_response.cookies.get('sessionId')
    return session_id


# Get sub_account_session
def get_sub_account_session(sub_account_key, temp_account_sessionid):
    get_sub_account_session_url = 'https://sqmallservice.u.sdo.com/api/us/daoyu/account/switch'
    get_sub_account_session_header = {
        'authority': 'sqmallservice.u.sdo.com',
        'method': 'GET',
        'scheme': 'https',
        'qu-merchant-id': '1',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'qu-deploy-platform': '8',
        'sec-fetch-site': 'same-site',
        'qu-web-host': 'https://m.qu.sdo.com',
        'accept-language': 'zh-CN,zh-Hans;q=0.9',
        'sec-fetch-mode': 'cors',
        'accept-encoding': 'gzip, deflate, br',
        'origin': 'https://m.qu.sdo.com',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 DaoYu/9.3.3',
        'referer': 'https://m.qu.sdo.com/',
        'qu-hardware-platform': '2',
        'qu-software-platform': '2',
        'sec-fetch-dest': 'empty'
    }
    get_sub_account_session_params = {
        'daoyuTicket': sub_account_key
    }
    get_sub_account_session_cookies = {
        'sessionId': temp_account_sessionid
    }
    get_temp_sessionid_response = requests.get(get_sub_account_session_url, params=get_sub_account_session_params,
                                               headers=get_sub_account_session_header,
                                               cookies=get_sub_account_session_cookies,
                                               verify=False)
    session_id = get_temp_sessionid_response.cookies.get('sessionId')
    return session_id
