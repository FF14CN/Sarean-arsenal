"""
Author: KuliPoi
Contact: me@pipirapira.com
Created: 2023-12-21
File: sqMailDoSign.py
Version: 2.5.0
Description: Do SQMALL AUTO SIGN, FUCK SQ BY THE WAY
"""
from Utility.sqMall import sm_login
from Utility.sqMall.daoyuBuildinMallSign import daoyumall_sign
from Utility.sqMall.daoyuBuildinMallBalance import daoyu_mall_balance
import Utility.Notifications.push as pusher


def main():
    if sm_login.initialize():
        device_id, manuid, main_key, show_username = sm_login.config_handler()
        sm_login.logger_logs.info(f'Get Config File Success,'
                               f'show_username: {show_username}'
                               f'daoyu_key: {sm_login.dykey_encrypt(main_key)}'
                               f'device_id: {device_id}, '
                               f'manuid: {manuid}')
        if main_key != '' and show_username != '':
            sm_login.logger_stream.info('读取到了你手动设置的DaoyuKey和ShowUserName')
        elif main_key == '' or show_username == '':
            sm_login.logger_stream.info('DaoyuKey 或者 showUsername 为空 看Github上的教程 求求你辣')
            exit()
        else:
            sm_login.logger_stream.info('config.ini可能存在问题，发个issue看看，注意不要直接将你的Config文件直接发在issue里')
            exit()
        flowid = sm_login.get_flowid(manuid, device_id, main_key, show_username)
        account_id_list = sm_login.get_account_id_list(flowid, device_id, manuid, main_key, show_username)
        temp_account_sessionid = sm_login.get_temp_sessionid(main_key)
        if account_id_list is not None:
            results = []
            for index, account_id in enumerate(account_id_list):
                if sm_login.make_confirm(account_id["accountId"], flowid, device_id, manuid, main_key, show_username):
                    sub_account_key = sm_login.get_sub_account_key(flowid, manuid, device_id, main_key, show_username)
                    sub_account_session = sm_login.get_sub_account_session(sub_account_key, temp_account_sessionid)
                    sign_msg = daoyumall_sign(sub_account_session, account_id["accountId"])
                    if sign_msg == 0:
                        sm_login.logger_stream.info(
                            f'账号{account_id["displayName"]}签到成功，当前积分余额{daoyu_mall_balance(sub_account_session)}')
                        sub_msg = f'账号{account_id["displayName"]}签到成功，当前积分余额{daoyu_mall_balance(sub_account_session)},'
                        results.append(sub_msg)
                        if index + 1 < len(account_id_list):
                            flowid = sm_login.get_flowid(manuid, device_id, main_key, show_username)
                    elif sign_msg == 1:
                        sm_login.logger_stream.info(
                            f'账号{account_id["displayName"]}已经签到过了，当前积分余额{daoyu_mall_balance(sub_account_session)}')
                        sub_msg = f'账号{account_id["displayName"]}已经签到过了，当前积分余额{daoyu_mall_balance(sub_account_session)},'
                        results.append(sub_msg)
                        if index + 1 < len(account_id_list):
                            flowid = sm_login.get_flowid(manuid, device_id, main_key, show_username)
                    else:
                        sm_login.logger_stream.info(f'账号{account_id["displayName"]}签到失败)')
                        sub_msg = f'账号{account_id["displayName"]}签到失败),'
                        results.append(sub_msg)
                        if index + 1 < len(account_id_list):
                            flowid = sm_login.get_flowid(manuid, device_id, main_key, show_username)
                else:
                    sm_login.logger_stream.info(f'账号{account_id["displayName"]}与服务器握手失败')
            msg = pusher.push('盛趣商城自动签到助手', ''.join(results))
            if msg['status'] == 'success':
                sm_login.logger_stream.info('推送消息成功')
            else:
                sm_login.logger_stream.info('推送消息失败，请检查消息推送服务是否配置成功')
                sm_login.logger_logs.error(msg)

        else:
            sm_login.logger_stream.info('没有发现你的账户，请检查logs文件')


if __name__ == '__main__':
    main()
