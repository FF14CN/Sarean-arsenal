# 此登陆方式不再维护，仅供科研使用
import requests
import json

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
        logger_logs.debug(f'Get Captcha Successful. captcha_session: {captcha_session} captcha_url: + {captcha_url}')
        return captcha_session
    else:
        logger_logs.error(f'Get Captcha Error : {send_sms_captcha_json}')
        logger_stream.error('致命错误，获取Captcha失败了，请将Logs反馈给开发者，程序即将停止。')
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
        with open('Temp/Captcha.jpeg', 'wb') as f:
            f.write(captcha_response.content)
        captcha_img = open('Temp/Captcha.jpeg', 'rb').read()
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
            logger_stream.info('未知错误，程序将退出.')
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
        config.read('config.ini', encoding='utf-8')
        config.set('Normal', 'DaoyuKeyInit', '0')
        config.set('Normal', 'DaoyuKey', user_sessid)
        config.set('Normal', 'ShowUsername', show_username)
        try:
            with open('config.ini', 'w', encoding='utf-8') as configfile:
                config.write(configfile)
        except Exception as e:
            logger_stream.info('写配置项失败,请手动修改config.ini ' + 'DaoyuKey: ' + user_sessid,
                               'ShowUsername: ' + show_username)
            logger_logs.error('write config.ini error: ' + str(e))
        return user_sessid, show_username
    else:
        logger_stream.info('获取DaoyuKey失败，请将Logs反馈给开发者')
        logger_logs.error(f'sms_login_json: {sms_login_json}')
        return None
