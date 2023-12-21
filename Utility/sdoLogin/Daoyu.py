import logging
import urllib3
import requests
import configparser
import os
from kuai_log import get_logger
import json
import time
import re

# print('Daoyu Module [FUCK SQ] - By Pipirapira 2023/12/20')

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger_stream = get_logger('INFO', level=logging.INFO, is_add_stream_handler=True)
logger_logs = get_logger('DEBUG', level=logging.DEBUG, is_add_file_handler=True, is_add_stream_handler=False,
                         log_path=f'{os.path.dirname(os.path.abspath(__file__))}/logs/',
                         log_filename='latest.log')


# 获取路径
def get_path():
    return os.path.dirname(os.path.abspath(__file__))


# 手机号打码
def phone_encrypt(self):
    return self.replace(self[1:10], '*********')


# DYKey打码
def dykey_encrypt(self):
    return re.sub(r"(?<=DY_)(.*)(?=..)", lambda match: '*' * len(match.group(1)), self)


def guid_encrypt(self):
    return re.sub(r"(?<=daoyu_)(.*)(?=\w{2})",
                  lambda match: match.group(1)[:2] + '*' * (len(match.group(1)) - 4) + match.group(1)[-2:], self)


# Json检查
def json_check(json_data, target_text):
    try:
        for key, value in json_data.items():
            if isinstance(value, str) and target_text in value:
                return True
    except json.JSONDecodeError:
        pass

    return False


# 对短信验证码进行解码
def ocr_handler(self):
    """
    :param self: 打开的图片
    :return: 返回解析后的验证码
    """
    host, _, _, username, password, soft_id, codetype, _, _, _, _, _, _ = config_handler()
    ocr_url = f'{host}'
    ocr_params = {
        'user': username,
        'pass': password,
        'softid': soft_id,
        'codetype': codetype,
        'len_min': 6
    }
    ocr_header = {
        'Connection': 'Keep-Alive',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
    }
    files = {'userfile': ('Captcha.jpeg', self)}
    ocr_resp = requests.post(ocr_url, data=ocr_params, headers=ocr_header, files=files, verify=False)
    code_json = ocr_resp.json()
    code = code_json['pic_str']
    errmsg = code_json['err_str']
    if errmsg != 'OK':
        logger_stream.error('解析二维码出错，程序即将退出,服务器返回消息：' + errmsg)
        exit()
    else:
        logger_stream.info('从第三方OCR服务器成功解析验证码：' + code)
        return code


# 配置文件读取
def config_handler():
    config = configparser.ConfigParser()
    config.read(f'{get_path()}/config.ini', encoding='utf-8')
    host = config.get('OCR', 'Host')
    phone_number = config.get('Normal', 'PhoneNumber')
    config_server = config.get('Develop', 'ConfigServer')
    username = config.get('OCR', 'Username')
    password = config.get('OCR', 'Password')
    soft_id = config.get('OCR', 'SoftID')
    codetype = config.get('OCR', 'CodeType')
    device_id = config.get('Normal', 'DeviceID')
    manuid = config.get('Normal', 'ManuID')
    daoyu_key_init = config.get('Normal', 'DaoyuKeyInit')
    daoyu_key = config.get('Normal', 'DaoyuKey')
    sms_enable = config.get('Normal', 'SMSLoginEnable')
    show_username = config.get('Normal', 'ShowUsername')
    logger_logs.info(f'Get Config File Success, Config File Path: {get_path()}/config.ini ,'
                     f'daoyu_key_init: {daoyu_key_init}, '
                     f'sms_enable: {sms_enable}, '
                     f'show_username: {show_username}'
                     f'daoyu_key: {dykey_encrypt(daoyu_key)}'
                     f'device_id: {device_id}, '
                     f'manuid: {manuid}')
    return (host, phone_number, config_server, username, password, soft_id, codetype, device_id, manuid,
            daoyu_key_init, daoyu_key, sms_enable, show_username)


# 初始化检测
def initialize():
    if os.path.exists(f'{get_path()}/config.ini'):  # 检测配置文件是否存在
        logger_stream.info('检测到存在配置文件，无需进行初始化...')
        return True
    else:
        url = 'https://pipirapira.com/config/config.ini'
        local_filename = f'{get_path()}/config.ini'
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
        logger_logs.info('guid:' + guid_encrypt(guid) + ' scene:' + scene)
        return guid, scene
    else:
        logger_logs.error('Guid or Scene Error', guid_json)
        logger_stream.error('致命错误，获取Guid失败了，程序即将停止。')
        return None


# 进行短信验证码登录，并获取sessid
def get_main_key(manu_id, device_id, guid, phone_number, scene):
    # 获得验证码 Session
    send_sms_captcha_url = 'https://daoyu.sdo.com/api/userCommon/sendSmsCode'
    send_sms_captcha_params = {
        'device_os': 'iOS17.0',
        'device_manuid': manu_id,
        'device_id': device_id,
        'idfa': '00000000-0000-0000-0000-000000000000',
        'image_type': '2',
        'sms_type': '2',
        'sms_channel': '1',
        'guid': guid,
        'app_version': 'i.9.3.3',
        'media_channel': 'AppStore',
        'phone': phone_number,
        'scene': scene,
        'src_code': '8',
    }
    headers = {
        'user-agent': 'SdAccountKeyM/9.3.3 (iPhone; iOS 17.0; Scale/3.00)',
        'content-type': 'application/json',
    }
    send_sms_captcha_response = requests.get(send_sms_captcha_url, params=send_sms_captcha_params, headers=headers,
                                             verify=False)
    send_sms_captcha_json = send_sms_captcha_response.json()
    captcha_session = send_sms_captcha_json['data']['captcha_session']
    captcha_url = send_sms_captcha_json['data']['captcha_url']

    if captcha_session and captcha_url != '':
        logger_logs.info('captcha_session:' + captcha_session + ' captcha_url:' + captcha_url)
    else:
        logger_logs.error('Get Captcha Error', send_sms_captcha_json)
        logger_stream.error('致命错误，获取Captcha失败了，程序即将停止。')
        exit()
    # 进入验证码循环校验流程
    while True:
        # 将获取的验证码进行OCR
        captcha_img_url = 'http://captcha.sdo.com/fcgi-bin/show_img.fcgi'
        captcha_img_params = {
            'appid': '151',
            'session_key': captcha_session,
            'gameid': '991002627',
            'areaid': '1',
        }
        captcha_img_headers = {
            'User-Agent': '%E5%8F%A8%E9%B1%BC/1 CFNetwork/1474 Darwin/23.0.0',
            'Host': 'captcha.sdo.com',
            'Accept-Encoding': 'gzip, deflate'
        }

        captcha_response = requests.get(captcha_img_url, params=captcha_img_params, headers=captcha_img_headers,
                                        verify=False)
        with open(f'{get_path()}/Temp/Captcha.jpeg', 'wb') as f:
            f.write(captcha_response.content)
        captcha_img = open(f'{get_path()}/Temp/Captcha.jpeg', 'rb').read()
        captcha_code = ocr_handler(captcha_img)

        # 校验OCR的验证码
        check_captcha_url = 'https://daoyu.sdo.com/api/userCommon/checkCaptcha?'
        check_captcha_params = {
            'idfa': '00000000-0000-0000-0000-000000000000',
            'app_version': 'i.9.3.3',
            'device_id': '7D30233F-F928-430E-BF0C-14A21260527A',
            'phone': phone_number,
            'scene': scene,
            'device_os': 'iOS17.0',
            'src_code': '8',
            'captcha_session': captcha_session,
            'sms_type': '2',
            'image_type': '1',
            'out_info': '',
            'device_manuid': manu_id,
            'media_channel': 'AppStore',
            'captcha_code': captcha_code,
        }
        check_captcha_header = {
            'authority': 'daoyu.sdo.com',
            'scheme': 'https',
            'content-type': 'application/json',
            'user-agent': 'SdAccountKeyM/9.3.3 (iPhone; iOS 17.0; Scale/3.00)',
        }
        check_captcha_response = requests.get(check_captcha_url, params=check_captcha_params,
                                              headers=check_captcha_header, verify=False)
        check_captcha_json = check_captcha_response.json()
        logger_logs.debug(check_captcha_json)
        if 'is_captcha' in check_captcha_json['data'] and check_captcha_json['data']['is_captcha'] == '0':
            logger_stream.info('校验码和服务器核对成功，短信验证码已经下发，请在1分钟内填入')
            break
        elif 'captcha_session' in check_captcha_json['data']:
            logger_stream.info('校验码和服务器核对失败，即将重试..')
            captcha_session = check_captcha_json['data']['captcha_session']
        elif 'return_message' in check_captcha_json and check_captcha_json[
            'return_message'] == '短信获取频繁，已被受限，请稍等再试':
            logger_stream.info('触发服务器风控，将在24小时后重试')
            time.sleep(86400)
        else:
            logger_stream.info(
                '超级大错误，你别问我我也不知道，可能服务器发癫可能是其他问题，建议重开程序，可以发送logs文件到issue，程序将退出.')
            exit()

    # 输入短信验证码并校验
    sms_code_input = input("请输入短信验证码：")
    sms_login_url = 'https://daoyu.sdo.com/api/userCommon/validateSmsCodeLogin'
    sms_login_params = {
        'sms_code': sms_code_input,
        'phone': phone_number,
        'device_manuid': manu_id,
        'device_os': 'iOS17.0',
        'idfa': '00000000-0000-0000-0000-000000000000',
        'media_channel': 'AppStore',
        'device_id': device_id,
        'app_version': 'i.9.3.3',
        'src_code': '8',
    }
    sms_login_header = {
        'authority': 'daoyu.sdo.com',
        'method': 'GET',
        'scheme': 'https',
        'content-type': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'user-agent': 'SdAccountKeyM/9.3.3 (iPhone; iOS 17.0; Scale/3.00)',

    }
    sms_login_response = requests.get(sms_login_url, params=sms_login_params, headers=sms_login_header, verify=False)
    sms_login_json = sms_login_response.json()
    if 'USERSESSID' in sms_login_json['data'] and sms_login_json['data']['is_login'] == '1':
        # DY_XXXX
        user_sessid = sms_login_json['data']['USERSESSID']
        nick_name = sms_login_json['data']['nickname']
        show_username = sms_login_json['data']['show_username']
        logger_stream.info(f'你好,{nick_name},目前一切正常...程序将继续执行剩余任务...')
        config = configparser.ConfigParser()
        config.read(f'{get_path()}/config.ini', encoding='utf-8')
        config.set('Normal', 'DaoyuKeyInit', '0')
        config.set('Normal', 'DaoyuKey', user_sessid)
        config.set('Normal', 'ShowUsername', show_username)
        try:
            with open(f'{get_path()}/config.ini', 'w', encoding='utf-8') as configfile:
                config.write(configfile)
        except Exception as e:
            logger_stream.info('写配置项失败,请手动修改config.ini ' + 'DaoyuKey: ' + user_sessid,
                               'ShowUsername: ' + show_username)
            logger_logs.error('write config.ini error: ' + str(e))
        return user_sessid, show_username
    else:
        logger_stream.info('无法解析叨鱼Key，请将日志文件发送给开发者')
        logger_logs.error('sms_login_json: ' + sms_login_json)
        return None


# DaoyuTicket
# step 1/4 Get flowid
def get_flowid(manuid, deviceid, sessionid, show_username):
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
    logger_logs.debug(get_flowid_json)
    if get_flowid_json['return_code'] == 0:
        flowid = get_flowid_json['data']['flowId']
        #        logger_stream.info('获取叨鱼票据中，获取浮动值成功 1/4.')
        logger_logs.info('flowid: ' + flowid)
        return flowid
    else:
        logger_stream.info('无法获取叨鱼票据浮动值，请将日志文件发送给开发者')
        logger_logs.error(get_flowid_json)
        return None


# step 2/4 Get accountID list
def get_account_id_list(flowid, deviceid, manuid, sessionid, show_username):
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
        logger_stream.info(f'获取叨鱼票据中，获取账户信息失败 2/4.')
        logger_logs.info(f'Get accountList error，{get_account_id_list_json}。')
        return None


# step 3/4 Confirm with server
def make_confirm(account_id, flowid, deviceid, manuid, sessionid, show_username):
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
        return True
    else:
        logger_stream.info(f'获取叨鱼票据步骤中，和服务器握手失败 3/4')
        logger_logs.error(f'确认失败，原因：{confirm_message}')
        return False


# step 4/4 Get DaoyuTicket
def get_sub_account_key(flowid, manuid, deviceid, main_key, show_username):
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
        'USERSESSID': main_key,
        'is_login': '1',
        'show_username': show_username,
    }
    get_daoyu_ticket_response = requests.get(get_daoyu_ticket_url, params=get_daoyu_ticket_params,
                                             headers=get_daoyu_ticket_header, cookies=get_daoyu_ticket_cookies,
                                             verify=False)
    get_daoyu_ticket_json = get_daoyu_ticket_response.json()
    if get_daoyu_ticket_json['return_code'] == 0:
        daoyu_ticket = get_daoyu_ticket_json['data']['authorization']
        #        logger_stream.info(f'获取叨鱼票据成功， 4/4.')
        return daoyu_ticket
    else:
        logger_logs.error(f'Get_daoyuTicket error，{get_daoyu_ticket_json}')
        logger_stream.info(f'获取叨鱼票据失败， 4/4.')
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


# Do sign
def do_sign(sub_session_id, account_id):
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
        logger_logs.debug('sign success')
        return 0
    elif sign_json['resultMsg'] == '今日已签到，请勿重复签到':
        logger_logs.debug('already sign')
        return 1
    else:
        return 2


# get balance
def get_balance(session_id):
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
