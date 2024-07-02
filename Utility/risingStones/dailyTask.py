"""
Author: KuliPoi
Contact: me@pipirapira.com
Update: 2024-07-02
File: DailyTask.py
Version: 1.6.0
Description: Start the game.
"""
from Utility.risingStones import signIn as rs_signin
from Utility.risingStones import rs_login
from Utility.risingStones import getSignReward
from Utility.risingStones import getUserInfo
from Utility.risingStones.rs_login import rs_get_flowid as get_flowid
from Utility.risingStones.rs_login import rs_get_account_id_list as get_account_id_list
from Utility.risingStones.rs_login import rs_make_confirm as make_confirm
from Utility.risingStones.rs_login import rs_get_temp_cookies as get_temp_cookies
from Utility.risingStones.rs_login import rs_get_sub_account_key as get_sub_account_key
from Utility.risingStones.rs_login import rs_dao_login as dao_login
from Utility.risingStones.rs_login import rs_do_login as do_login
from Utility.risingStones.rs_login import rs_bind as rs_bind
from Utility.risingStones.houseStatusChecker import house_status_checker as house_status_checker


def daily_task():
    flowid = get_flowid()
    account_id_list = get_account_id_list(flowid)
    if account_id_list is not None:
        for index, account_id in enumerate(account_id_list):
            display_name = account_id["displayName"]
            rs_login.logger_stream.info(f'当前操作账户 [{index + 1}] [{display_name}]')
            if make_confirm(account_id["accountId"], flowid):
                cookies = get_temp_cookies()
                sub_account_key = get_sub_account_key(flowid)
                daoyu_ticket = dao_login(sub_account_key, cookies)
                login_status, login_cookies = do_login(daoyu_ticket, cookies)
                if rs_login.debug:
                    print(login_cookies)
                if login_status:
                    # bind character
                    bind_cookies = rs_bind(login_cookies, daoyu_ticket)
                    # sign in
                    sign_in_msg = rs_signin.rs_signin(bind_cookies,daoyu_ticket)
                    # Get Reward
                    get_reward_msg = getSignReward.getReward(bind_cookies,daoyu_ticket)
                    # Get Userinfo
                    user_info = getUserInfo.get_rs_userinfo(bind_cookies,daoyu_ticket)
                    # Get HouseInfo
                    house_msg = house_status_checker(user_info)
                    if rs_login.debug:
                        print(f'sign-msg：{sign_in_msg}')
                        print(f'get-reward-msg：{get_reward_msg}')
                        print(f'house-info-msg：{house_msg}')
                    final_msg = f'石之家任务结果, {sign_in_msg}, {get_reward_msg}, {house_msg}'
                    rs_login.logger_stream.info(final_msg)
                    if rs_login.debug:
                        print(final_msg)
                    if index + 1 < len(account_id_list):
                        flowid = get_flowid()
                else:
                    if index + 1 < len(account_id_list):
                        flowid = get_flowid()
            else:
                if index + 1 < len(account_id_list):
                    flowid = get_flowid()


    else:
        print("拉取账号列表失败，请检查config.ini中的参数是否正确设置")



