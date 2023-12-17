import logging
import urllib3
import requests
import configparser
import os
from kuai_log import get_logger
import json
import time


# 获取路径
def get_path():
    return os.path.dirname(os.path.abspath(__file__))


# 手机号打码
def phone_encrypt(self):
    return self.replace(self[1:10], '*********')


# Json检查
def json_check(json_data, target_text):
    try:
        for key, value in json_data.items():
            if isinstance(value, str) and target_text in value:
                return True
    except json.JSONDecodeError:
        pass

    return False


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
    logger_stream.info('读取配置文件成功')
    return host, phone_number, config_server, username, password, soft_id, codetype, device_id, manuid


# 初始化检测
def initialize():
    if os.path.exists(f'{get_path()}/config.ini'):  # 检测配置文件是否存在
        logger_stream('检测到存在配置文件，无需进行初始化...')
        return True
    else:
        url = 'https://pipirapira.com/config/config_2.0.1.ini'
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
            return False


# 对玄心验证码进行解码
def ocr_handler(self):
    """
    :param self: 打开的图片
    :return: 返回解析后的验证码
    """
    host, _, _, username, password, soft_id, codetype, _, _ = config_handler()
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
        logger_logs.info('guid:' + guid + ' scene:' + scene)
        return guid, scene
    else:
        logger_logs.error('Guid or Scene Error', guid_json)
        logger_stream.error('致命错误，获取Guid失败了，请尝试重启程序，或使用程序目录下的/tools/DeviceGen.exe重新为您分配一个设备，'
                            '程序即将停止。')
        exit()


# 进行短信验证码登录，并获取sessid
def get_sessid(manu_id, device_id, guid, phone_number, scene):
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
    sms_login_url = 'https://daoyu.sdo.com/api/userCommon/validateSmsCodeLogin?'
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
        user_sessid = sms_login_json['data']['USERSESSID']
        nick_name = sms_login_json['data']['nickname']
        logger_stream.info(f'你好,{nick_name},目前一切正常...程序将继续执行剩余任务...')
        logger_logs.info(f'Username:{nick_name}, UserSessid: {user_sessid}')
        return nick_name, user_sessid
    else:
        logger_stream.info('无法解析叨鱼Key，请将日志文件发送给开发者')
        logger_logs.error('sms_login_json: ' + sms_login_json)
        exit()


# 获取账户信息
def userinfo_handler(sessid, device_id, manuid, phone_number):
    # 获取绑定的账号信息
    account_info_url = 'https://yaoshi.sdo.com/fk/yaoshi/login?'
    account_info_params = {
        'sessionid': sessid,
        'netflag': 'WIFI',
        'sequence': '54',
        'version': 'i.9.3.3',
        'registerflag': '0',
        'firstflag': '0',
        'txzDeviceId': device_id,
        'deviceModel': manuid,
        'deviceName': 'iPhone',
        'osType': '1',
        'osVersion': '17.0',
        'pushToken': 'v2:63f51e743a0bd2058133df274c4659965eb36df6f793468df4388734a28e9f5c',
        'phone': phone_number,
        'loginType': '2',
        'isHttp': '0'
    }
    account_info_header = {
        'User-Agent': '%E5%8F%A8%E9%B1%BC/1 CFNetwork/1474 Darwin/23.0.0',
        'Host': 'yaoshi.sdo.com',
        'Accept-Encoding': 'gzip, deflate'
    }
    account_info_response = requests.get(account_info_url, params=account_info_params, headers=account_info_header,
                                         verify=False)
    account_info_json = account_info_response.json()
    sndaid_dist_str = account_info_json['data']['SndaIdList']
    sndaid_list_dict = {}
    pairs = sndaid_dist_str.split(',')
    for pair in pairs:
        key, value = pair.split(':')
        sndaid_list_dict[key] = value
    return sndaid_list_dict


# 主进程
def main():
    pass


if __name__ == '__main__':
    # 对logger进行初始化
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    logger_stream = get_logger('INFO', level=logging.INFO, is_add_stream_handler=True)
    logger_logs = get_logger('DEBUG', level=logging.DEBUG, is_add_file_handler=True, is_add_stream_handler=False,
                             log_path=f'{get_path()}/logs/',
                             log_filename='latest.log')
    main()
